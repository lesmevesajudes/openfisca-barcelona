import datetime
from numpy import logical_or

from datetime import datetime
from openfisca_barcelona.variables.demographics import *
from openfisca_barcelona.variables.housing import *


class contracte_posterior_a_1_11_2016(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = u"The rent contract is signed after 2016/11/01"
    set_input = set_input_dispatch_by_period

    def formula(familia, period, parameters):
        return familia("data_signatura_contracte_de_lloguer", period) > datetime.strptime('1916-11-1', "%Y-%m-%d").date()

class contracte_obtingut_a_traves_de_borsa_de_mediacio_o_gestionat_per_entitat_sense_anim_de_lucre(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = u"The rent contract has been obtainet through mediaton or the owner of the flat is a benefit association"
    set_input = set_input_dispatch_by_period


class HG_077_03_mensual(Variable):
    column = FloatCol
    entity = Persona  # S'atorga a la persona que fa el contracte de lloguer
    definition_period = MONTH
    label = "AJUT PER AL PAGAMENT DEL LLOGUER BORSA"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        irsc = parameters(period).benefits.HG077.IRSC
        irsc_per_1_5 = irsc * 1.5

        ingressos_familia_mensual = persona.familia("familia_ingressos_disponibles", period) / 12

        retornat_espanyol_residint_a_lextranger_36_mesos = ((persona("nacionalitat", period) == "Espanyola")
              * (persona("ha_residit_a_lextranger_36_mesos_continuats", period)
                    + persona("ha_residit_a_lextranger_60_mesos_discontinuats", period))
              * persona("ha_residit_a_lextranger_els_ultims_24_mesos", period))

        emigrant_amb_5_anys_de_residencia = ((persona("nacionalitat", period) != "Espanyola")
                * persona("resident_a_catalunya_durant_5_anys", period)
                * persona("ha_residit_a_catalunya_els_ultims_24_mesos", period))

        requeriments_solicitant = \
                logical_or(emigrant_amb_5_anys_de_residencia, retornat_espanyol_residint_a_lextranger_36_mesos) \
                * persona("edat", period) > 18 \
                * persona("titular_contracte_de_lloguer", period) \
                * persona("risc_d_exclusio_social", period)

        requeriments_familia = \
                (ingressos_familia_mensual < irsc_per_1_5) \
                * persona.familia("esta_al_corrent_del_pagament_de_lloguer", period) \
                * persona.familia("lloguer_domiciliat", period) \
                * persona.familia("contracte_posterior_a_1_11_2016", period) \
                * (persona.familia("contracte_obtingut_a_traves_de_borsa_de_mediacio_o_gestionat_per_entitat_sense_anim_de_lucre", period) == False) \
                * (persona.familia("import_del_lloguer", period) < persona("lloguer_maxim_segons_demarcacio_077", period))

        import_ajuda = 200

        return requeriments_solicitant * requeriments_familia * import_ajuda
