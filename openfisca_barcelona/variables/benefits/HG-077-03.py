import datetime
from numpy import logical_or, logical_not

from datetime import datetime
from openfisca_barcelona.variables.demographics import *
from openfisca_barcelona.variables.housing import *

class data_signatura_contracte_de_lloguer(Variable):
    column = DateCol
    entity = Familia
    definition_period = ETERNITY
    label = u"When the rent contract was signed"

class contracte_posterior_a_1_11_2016(Variable):
    column = BoolCol
    entity = Familia
    definition_period = ETERNITY
    label = u"The rent contract is signed after 2016/11/01"

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

        espanyol_resident_a_catalunya = (persona("nacionalitat", period) == "Espanyola") \
                                        * (persona("ha_residit_a_lextranger_els_ultims_24_mesos", period) == False)

        requeriments_solicitant = \
            ((emigrant_amb_5_anys_de_residencia
                + retornat_espanyol_residint_a_lextranger_36_mesos
                + espanyol_resident_a_catalunya)) \
                * persona("edat", period) > 18 \
                * persona("titular_contracte_de_lloguer", period)

        requeriments_familia = \
                (ingressos_familia_mensual < irsc_per_1_5) \
                * (persona.familia("import_del_deute_amb_el_propietari", period) == 0) \
                * persona.familia("lloguer_domiciliat", period) \
                * persona.familia("contracte_posterior_a_1_11_2016", period) \
                * (persona.familia("relacio_de_parentiu_amb_el_propietari", period) == False) \
                * (persona.familia("contracte_obtingut_a_traves_de_borsa_de_mediacio_o_gestionat_per_entitat_sense_anim_de_lucre", period) == True) \
                * (persona.familia("import_del_lloguer", period) < persona("lloguer_maxim_segons_demarcacio_077", period)) \
                * (ingressos_familia_mensual * 0.3 < persona.familia("import_del_lloguer", period))

        import_ajuda = max(20, min(200, (persona.familia("import_del_lloguer", period) - persona.familia("lloguer_just", period))))

        return requeriments_solicitant * requeriments_familia * import_ajuda
