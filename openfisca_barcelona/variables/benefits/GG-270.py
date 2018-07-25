import numpy

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


def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres == 4, membres > 4],
                  ['1', '2', '3', '4', '5_o_mes'])

class solicitant_GG_270_valid(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person a valid GG-270 benefitiary"

    def formula(persona, period, parameters):
        discapacitats_a_carrec = persona.familia_fins_a_segon_grau.any(persona("es_discapacitat", period))
        en_els_ultims_12_mesos_no_ha_fet_baixa_voluntaria_de_la_feina = \
            persona("en_els_ultims_12_mesos_ha_fet_baixa_voluntaria_de_la_feina", period) == False
        situacio_laboral = persona('situacio_laboral', period)
        es_contracte_jornada_parcial = situacio_laboral == situacio_laboral.possible_values.treball_compte_daltri_jornada_parcial
        es_divorciada_de_familia_reagrupada = persona("es_divorciada_de_familia_reagrupada", period)
        es_empadronat_a_catalunya = persona("municipi_empadronament", period) != "no_empadronat_a_cat"
        es_orfe_de_progenitors = persona("es_orfe_dels_dos_progenitors", period)
        tipus_monoparental = persona.familia('tipus_familia_monoparental', period)
        es_monoparental = tipus_monoparental != tipus_monoparental.possible_values.nop
        es_victima_violencia_de_genere = persona("es_victima_de_violencia_masclista", period)
        ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos = \
            persona("ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos", period)
        inscrit_com_a_demandant_docupacio = persona('inscrit_com_a_demandant_docupacio', period)
        ingressos_mensuals = persona("ingressos_bruts_ultims_sis_mesos", period) / 6
        nr_membres = persona.familia_fins_a_segon_grau.nb_persons()
        llindar_ingressos = parameters(period).benefits.GG270.llindars_ingressos[clauNombreDeMebres(nr_membres)]
        compleix_nivell_ingressos = ingressos_mensuals < llindar_ingressos
        major_18 = persona("edat", period) >= 18
        major_23 = persona("edat", period) >= 23
        no_beneficiari_de_prestacio_residencial = persona("beneficiari_de_prestacio_residencial", period) == False
        no_ingressat_en_centre_penitenciari = persona('ingressat_en_centre_penitenciari', period) == False
        porta_dos_anys_o_mes_empadronat_a_catalunya = persona("porta_dos_anys_o_mes_empadronat_a_catalunya", period)

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
                            * (inscrit_com_a_demandant_docupacio + (es_monoparental * es_contracte_jornada_parcial)) \
                            * no_ingressat_en_centre_penitenciari

        return compleix_criteris


class import_GG_270(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = "GG-270 amount for a given person"

    def formula(persona, period, parameters):
        nr_membres = persona.familia.nb_persons()
        llindar_ingressos = parameters(period).benefits.GG270.llindars_ingressos[clauNombreDeMebres(nr_membres)]
        tipus_monoparental = persona.familia('tipus_familia_monoparental', period)
        es_monoparental = tipus_monoparental != tipus_monoparental.possible_values.nop
        ingressos_mensuals = persona("ingressos_bruts_ultims_sis_mesos", period) / 6
        import_ajuda = round_(llindar_ingressos - ingressos_mensuals, decimals=0) + (es_monoparental * 75)
        return import_ajuda * persona('solicitant_GG_270_valid', period)


class GG_270_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "RENDA GARANTIDA CIUTADANA"

    def formula(persona, period, parameters):
        es_solicitant_viable_GG_270 = persona('solicitant_GG_270_valid', period)
        import_ajuda_maxim_familia = persona.familia_fins_a_segon_grau.max(persona.familia_fins_a_segon_grau.members('import_GG_270', period))
        import_ajuda_aquesta_persona = persona('import_GG_270', period)

        return es_solicitant_viable_GG_270 \
               * (import_ajuda_maxim_familia == import_ajuda_aquesta_persona)\
               * import_ajuda_aquesta_persona
