from numpy import round

from openfisca_barcelona.variables.demographics import *
from openfisca_barcelona.variables.housing import *


class HG_077_04_mensual(Variable):
    column = FloatCol
    entity = Persona  # S'atorga a la persona que fa el contracte de lloguer
    definition_period = MONTH
    label = "AJUT PER AL PAGAMENT DEL LLOGUER RENOVABLES"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        irsc = parameters(period).benefits.HG077.IRSC
        irsc_per_1_5 = irsc * 1.5

        ingressos_familia_mensual = persona.familia("familia_ingressos_disponibles", period) / 12

        requeriments_solicitant = \
            ((persona("nacionalitat", period) == "Espanyola")
             * persona("resident_a_catalunya_durant_5_anys", period)
             * persona("ha_residit_a_catalunya_els_ultims_24_mesos", period)) \
            * persona("es_BLJ", period) \
            * persona("titular_contracte_de_lloguer", period) \
            * persona("risc_d_exclusio_social", period)

        requeriments_familia = \
            (ingressos_familia_mensual < irsc_per_1_5) \
            * persona.familia("esta_al_corrent_del_pagament_de_lloguer", period) \
            * persona.familia("lloguer_domiciliat", period) \
            * (persona.familia("import_del_lloguer", period) < parameters(
                period).benefits.HG077.lloguer_maxim_ciutat_barcelona) \
            * (persona.familia("lloguer_domiciliat", period)) \
            * (persona.familia("relacio_de_parentiu_amb_el_propietari", period).any() == False)

        import_ajuda = round(min(
            200,
            max(20, persona.familia("import_del_lloguer", period) - ingressos_familia_mensual * 0.30)))

        return requeriments_solicitant * requeriments_familia * import_ajuda
