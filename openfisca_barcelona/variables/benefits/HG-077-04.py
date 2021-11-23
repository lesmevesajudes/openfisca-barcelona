from openfisca_core.model_api import *
from openfisca_barcelona.entities import *

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres >= 4],
                  ['un', 'dos', 'tres', 'quatreomes'])

def clauDependencia(valor):
    return select([valor == 0, valor > 0],
                  ['sense_discapacitat_dependencia', 'amb_discapacitat_dependencia'])

class lloguer_inferior_al_maxim_per_demarcacio_HG_077_04(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        demarcacio_de_lhabitatge = unitatDeConvivencia("demarcacio_de_lhabitatge", period)
        lloguer_maxim_per_demarcacio = legislation(period).benefits.HG07704.import_lloguer_maxim[demarcacio_de_lhabitatge]
        return import_del_lloguer <= lloguer_maxim_per_demarcacio


class pot_ser_solicitant_HG_077_04(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        empadronat_a_catalunya = (persona("municipi_empadronament", period) == b'barcelona') \
        + (persona("municipi_empadronament", period) == b'altres') \
        + (persona("municipi_empadronament", period) == b'municipis_atm')
        temps_empadronat_a_lhabitatge = persona("temps_empadronat_habitatge_actual", period)
        empadronat_a_lhabitatge = temps_empadronat_a_lhabitatge != temps_empadronat_a_lhabitatge.possible_values.no_empadronat
        titular_contracte_de_lloguer = persona("titular_contracte_de_lloguer", period)

        return empadronat_a_catalunya \
               * empadronat_a_lhabitatge \
               * titular_contracte_de_lloguer


class HG_077_04(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "AJUTS LLOGUER ESPECIAL URGENCIA"

    def formula(unitatDeConvivencia, period, legislation):
        nr_membres = unitatDeConvivencia.nb_persons()
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period) > 33
        dependencies = unitatDeConvivencia.members("grau_dependencia", period) == 3
        existeix_discapacitat_o_dependencia = unitatDeConvivencia.any(discapacitats) + unitatDeConvivencia.any(dependencies)
        zona_de_lhabitatge = unitatDeConvivencia("zona_de_lhabitatge", period)
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HG_077_04", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts", period.last_year)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 12
        nivell_ingressos_maxim = \
            legislation(period).benefits.HG07704.ingressos_maxims[clauDependencia(existeix_discapacitat_o_dependencia)][clauNombreDeMebres(nr_membres)]
        ingressos_bruts_dins_barems = ingressos_familia_mensuals <= nivell_ingressos_maxim
        deute_lloguer = \
            unitatDeConvivencia("existeix_deute_en_el_pagament_del_lloguer", period) == True
        ha_pagat_almenys_3_quotes_del_lloguer = unitatDeConvivencia("ha_pagat_almenys_3_quotes_del_lloguer", period)
        lloguer_inferior_al_maxim_per_demarcacio = unitatDeConvivencia("lloguer_inferior_al_maxim_per_demarcacio_HG_077_04", period)
        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False
        import_ajuda = min(4500, unitatDeConvivencia("import_deute_en_el_pagament_del_lloguer", period))

        return existeix_solicitant_viable \
               * ingressos_bruts_dins_barems \
               * deute_lloguer \
               * ha_pagat_almenys_3_quotes_del_lloguer \
               * lloguer_inferior_al_maxim_per_demarcacio\
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari \
               * import_ajuda
