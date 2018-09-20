from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.HA import clauIRSCPonderat, clauMultiplicadors


class quota_hipoteca_inferior_al_maxim_per_demarcacio_HA003(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_de_la_hipoteca = unitatDeConvivencia("import_de_la_hipoteca", period)
        demarcacio_de_lhabitatge = unitatDeConvivencia("demarcacio_de_lhabitatge", period)
        import_de_la_hipoteca_maxim_per_demarcacio = legislation(period).benefits.HA.import_quota_hipoteca_maxim["HA003"][demarcacio_de_lhabitatge]
        return import_de_la_hipoteca < import_de_la_hipoteca_maxim_per_demarcacio


class pot_ser_solicitant_HA003(Variable):
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
        titular_hipoteca = persona("titular_hipoteca", period)

        return (has_DNI + has_NIE) \
               * empadronat_a_catalunya \
               * empadronat_a_lhabitatge \
               * titular_hipoteca


class HA_003(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "AJUTS ESPECIAL URGENCIA AMORTITZACIO HIPOTECARIA"

    def formula(unitatDeConvivencia, period, legislation):
        nr_membres = unitatDeConvivencia.nb_persons()
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period)
        existeix_algun_discapacitat = unitatDeConvivencia.any(discapacitats)
        zona_de_lhabitatge = unitatDeConvivencia("zona_de_lhabitatge", period)
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HA003", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts_ultims_sis_mesos", period)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 6 / nr_membres
        nivell_ingressos_maxim = \
            legislation(period).benefits.HA.irsc_ponderat[zona_de_lhabitatge][clauIRSCPonderat(nr_membres)] \
            * legislation(period).benefits.HA.multiplicadors[clauMultiplicadors(nr_membres, existeix_algun_discapacitat)]
        ingressos_bruts_dins_barems = ingressos_familia_mensuals <= nivell_ingressos_maxim
        no_fa_mes_de_12_mesos_que_existeix_el_deute_de_hipoteca = unitatDeConvivencia("fa_mes_de_12_mesos_que_existeix_el_deute_de_hipoteca", period) == False
        ha_pagat_12_mesos_daquesta_hipoteca = unitatDeConvivencia("ha_pagat_12_mesos_daquesta_hipoteca", period)
        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False
        quota_hipoteca_inferior_al_maxim_per_demarcacio_HA003 = unitatDeConvivencia("quota_hipoteca_inferior_al_maxim_per_demarcacio_HA003", period)
        import_ajuda = min(3000, unitatDeConvivencia("import_deute_en_el_pagament_hipoteca", period))

        return existeix_solicitant_viable \
               * ingressos_bruts_dins_barems \
               * no_fa_mes_de_12_mesos_que_existeix_el_deute_de_hipoteca \
               * ha_pagat_12_mesos_daquesta_hipoteca \
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari \
               * quota_hipoteca_inferior_al_maxim_per_demarcacio_HA003 \
               * import_ajuda
