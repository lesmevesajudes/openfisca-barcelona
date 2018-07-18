from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.HA import clauIRSCPonderat, clauMultiplicadors


class desDeQuanTeniuDeutesDeLloguer(Enum):
    no_en_tinc = "no_en_tinc"
    mes_dun_any = "mes_dun_any"
    menys_dun_any = "menys_dun_any"


class des_de_quan_teniu_deutes_de_lloguer(Variable):
    value_type = Enum
    possible_values = desDeQuanTeniuDeutesDeLloguer
    default_value = desDeQuanTeniuDeutesDeLloguer.no_en_tinc
    entity = UnitatDeConvivencia
    label = u"labor situation"
    definition_period = MONTH


class lloguer_inferior_al_maxim_per_demarcacio_HA004(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        demarcacio_de_lhabitatge = unitatDeConvivencia("demarcacio_de_lhabitatge", period)
        lloguer_maxim_per_demarcacio = legislation(period).benefits.HA.import_lloguer_maxim["HA004"][demarcacio_de_lhabitatge]
        return import_del_lloguer < lloguer_maxim_per_demarcacio


class pot_ser_solicitant_HA004(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        tipus_document_identitat = persona("tipus_document_identitat", period)
        has_DNI = tipus_document_identitat == tipus_document_identitat.possible_values.DNI
        has_NIE = tipus_document_identitat == tipus_document_identitat.possible_values.NIE
        empadronat_a_catalunya = (persona("municipi_empadronament", period) == "barcelona") + (persona("municipi_empadronament", period) == "altres")
        temps_empadronat_a_lhabitatge = persona("temps_empadronat_habitatge_actual", period)
        empadronat_a_lhabitatge = temps_empadronat_a_lhabitatge != temps_empadronat_a_lhabitatge.possible_values.no_empadronat
        titular_contracte_de_lloguer = persona("titular_contracte_de_lloguer", period)
        return (has_DNI + has_NIE) \
               * empadronat_a_catalunya \
               * empadronat_a_lhabitatge \
               * titular_contracte_de_lloguer




class HA_004(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "AJUTS LLOGUER ESPECIAL URGENCIA"

    def formula(unitatDeConvivencia, period, legislation):
        nr_membres = unitatDeConvivencia.nb_persons()
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period)
        existeix_algun_discapacitat = unitatDeConvivencia.any(discapacitats)
        zona_de_lhabitatge = unitatDeConvivencia("zona_de_lhabitatge", period)
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HA004", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts", period.last_year)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 12
        nivell_ingressos_maxim = \
            legislation(period).benefits.HA.irsc_ponderat[zona_de_lhabitatge][clauIRSCPonderat(nr_membres)] \
            * legislation(period).benefits.HA.multiplicadors[clauMultiplicadors(nr_membres, existeix_algun_discapacitat)]
        ingressos_bruts_dins_barems = ingressos_familia_mensuals < nivell_ingressos_maxim
        fa_menys_dun_any_que_existeix_el_deute_de_lloguer = unitatDeConvivencia("des_de_quan_teniu_deutes_de_lloguer", period) == desDeQuanTeniuDeutesDeLloguer.menys_dun_any
        ha_pagat_almenys_3_quotes_del_lloguer = unitatDeConvivencia("ha_pagat_almenys_3_quotes_del_lloguer", period)
        lloguer_inferior_al_maxim_per_demarcacio = unitatDeConvivencia("lloguer_inferior_al_maxim_per_demarcacio_HA004", period)
        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False
        import_ajuda = min(3000, unitatDeConvivencia("import_deute_en_el_pagament_del_lloguer", period))

        return existeix_solicitant_viable \
               * ingressos_bruts_dins_barems \
               * fa_menys_dun_any_que_existeix_el_deute_de_lloguer \
               * ha_pagat_almenys_3_quotes_del_lloguer \
               * lloguer_inferior_al_maxim_per_demarcacio\
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari \
               * import_ajuda
