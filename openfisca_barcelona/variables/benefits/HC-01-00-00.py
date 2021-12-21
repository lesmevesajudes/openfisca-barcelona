from openfisca_core.model_api import *
from openfisca_barcelona.entities import *

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres >= 4],
                  ['un', 'dos', 'tres', 'quatreomes'])

def clauDependencia(valor):
    return select([valor == 0, valor > 0],
                  ['sense_discapacitat_dependencia', 'amb_discapacitat_dependencia'])

class ates_pel_servei_de_mediacio_de_barcelona(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Barcelona mediation service is giving support"
    default_value = False

class lloguer_inferior_al_maxim_HC_01_00_00(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        return import_del_lloguer <= 970


class pot_ser_solicitant_HC_01_00_00(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        empadronat_a_barcelona = (persona("municipi_empadronament", period) == b'barcelona')
        temps_empadronat_a_lhabitatge = persona("temps_empadronat_habitatge_actual", period)
        empadronat_a_lhabitatge = temps_empadronat_a_lhabitatge != temps_empadronat_a_lhabitatge.possible_values.no_empadronat
        titular_contracte_de_lloguer = persona("titular_contracte_de_lloguer", period)

        return empadronat_a_barcelona \
               * empadronat_a_lhabitatge \
               * titular_contracte_de_lloguer


class HC_01_00_00(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "AJUTS LLOGUER DERIVADES DE LA MEDIACIO"

    def formula(unitatDeConvivencia, period, legislation):
        nr_membres = unitatDeConvivencia.nb_persons()
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period) > 33
        dependencies = unitatDeConvivencia.members("grau_dependencia", period) == 3
        existeix_discapacitat_o_dependencia = unitatDeConvivencia.any(discapacitats) + unitatDeConvivencia.any(dependencies)
        zona_de_lhabitatge = unitatDeConvivencia("zona_de_lhabitatge", period)
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HC_01_00_00", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts", period.last_year)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 12
        nivell_ingressos_maxim = \
            legislation(period).benefits.HC.ingressos_maxims[clauDependencia(existeix_discapacitat_o_dependencia)][clauNombreDeMebres(nr_membres)]
        ingressos_bruts_dins_barems = ingressos_familia_mensuals <= nivell_ingressos_maxim
        deute_lloguer = \
            unitatDeConvivencia("existeix_deute_en_el_pagament_del_lloguer", period) == True
        ates_pel_servei_de_mediacio = unitatDeConvivencia("ates_pel_servei_de_mediacio_de_barcelona", period)
        lloguer_inferior_al_maxim = unitatDeConvivencia("lloguer_inferior_al_maxim_HC_01_00_00", period)
        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False

        return existeix_solicitant_viable \
               * ingressos_bruts_dins_barems \
               * deute_lloguer \
               * ates_pel_servei_de_mediacio \
               * lloguer_inferior_al_maxim\
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari
