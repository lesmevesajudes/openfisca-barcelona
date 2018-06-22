from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class es_orfe_dels_dos_progenitors(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "True if both adults are dead"
    default_value = False


class es_victima_de_violencia_masclista(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "True if person is a victim of male violence"
    default_value = False


class es_divorciada_de_familia_reagrupada(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "True if person is divorced from a regrouped immigrant family"
    default_value = False


class en_els_ultims_12_mesos_ha_fet_baixa_voluntaria_de_la_feina(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "True if person has left voluntarily her last job"
    default_value = False

class beneficiari_de_prestacio_residencial(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Person has a residential benefit"
    default_value = False


class es_discapacitat(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "True if person is disabled"

    def formula(persona, period, legislation):
        return persona("grau_discapacitat", period) > 0

class nivell_de_renda_inferior_rgc(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "True if income is less than IRSC"

    def formula(persona, period, legislation):
        return persona("ingressos_bruts", period.last_year) / 12 < 530 #TODO Stub, as I can not understand documentation


class GG_270_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "RENDA GARANTIDA CIUTADANA"

    def formula(persona, period, legislation):
        compleix_nivell_ingressos = persona("nivell_de_renda_inferior_rgc", period)
        no_beneficiari_de_prestacio_residencial = persona("beneficiari_de_prestacio_residencial", period) == False
        discapacitats_a_carrec = persona.familia.any(persona("es_discapacitat", period))
        en_els_ultims_12_mesos_no_ha_fet_baixa_voluntaria_de_la_feina = \
            persona("en_els_ultims_12_mesos_ha_fet_baixa_voluntaria_de_la_feina", period) == False
        es_divorciada_de_familia_reagrupada = persona("es_divorciada_de_familia_reagrupada", period)
        es_empadronat_a_catalunya = persona("municipi_empadronament", period) != "no_empadronat_a_cat"
        es_orfe_de_progenitors = persona("es_orfe_dels_dos_progenitors", period)
        es_victima_violencia_de_genere = persona("es_victima_de_violencia_masclista", period)
        ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos = \
            persona("ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos", period)
        major_18 = persona("edat", period) >= 18
        major_23 = persona("edat", period) >= 23
        porta_dos_anys_o_mes_empadronat_a_catalunya = persona("porta_dos_anys_o_mes_empadronat_a_catalunya", period)
        no_ingressat_en_centre_penitenciari = persona('ingressat_en_centre_penitenciari', period) == False

        # TODO Revisar el cas de menors discapacitats a carrec
        compleix_criteris = (es_empadronat_a_catalunya
                             + es_divorciada_de_familia_reagrupada
                             + ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos) \
                            * porta_dos_anys_o_mes_empadronat_a_catalunya \
                            * (major_23
                               + (major_18
                                  * (es_orfe_de_progenitors + es_victima_violencia_de_genere + discapacitats_a_carrec))) \
                            * en_els_ultims_12_mesos_no_ha_fet_baixa_voluntaria_de_la_feina \
                            * no_beneficiari_de_prestacio_residencial \
                            * compleix_nivell_ingressos \
                            * no_ingressat_en_centre_penitenciari

        print (compleix_criteris)
        return compleix_criteris * 100  # Fixme: Stub
