from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.H import clauIRSCPonderat, clauMultiplicadors, demarcacioDeLHabitatge, clauNombreDeMebres, clauDependencia

class quota_hipoteca_inferior_al_maxim_per_demarcacio_HG_077_03(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_de_la_hipoteca = unitatDeConvivencia("import_de_la_hipoteca", period)
        demarcacio_de_lhabitatge = unitatDeConvivencia("demarcacio_de_lhabitatge", period)
        import_de_la_hipoteca_maxim_per_demarcacio = legislation(period).benefits.H.import_quota_hipoteca_maxim["HG_077_03"][demarcacio_de_lhabitatge]
        return import_de_la_hipoteca <= import_de_la_hipoteca_maxim_per_demarcacio


class pot_ser_solicitant_HG_077_03(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        tipus_document_identitat = persona("tipus_document_identitat", period)
        has_DNI = tipus_document_identitat == tipus_document_identitat.possible_values.DNI
        has_NIE = tipus_document_identitat == tipus_document_identitat.possible_values.NIE
        temps_empadronat_a_lhabitatge = persona("temps_empadronat_habitatge_actual", period)
        empadronat_a_lhabitatge = temps_empadronat_a_lhabitatge != temps_empadronat_a_lhabitatge.possible_values.no_empadronat
        titular_hipoteca = persona("titular_hipoteca", period)

        return (has_DNI + has_NIE) \
               * empadronat_a_lhabitatge \
               * titular_hipoteca


class HG_077_03(Variable):
    value_type = bool
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "AJUTS ESPECIAL URGENCIA AMORTITZACIO HIPOTECARIA"

    def formula(unitatDeConvivencia, period, legislation):
        nr_membres = unitatDeConvivencia.nb_persons()
        resident_a_barcelona_ciutat = \
            unitatDeConvivencia("demarcacio_de_lhabitatge", period) == demarcacioDeLHabitatge.barcelona_ciutat
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period)
        existeix_algun_discapacitat = unitatDeConvivencia.any(discapacitats)
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HG_077_03", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts_ultims_sis_mesos", period)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 6 / nr_membres

        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period) > 33
        dependencies = unitatDeConvivencia.members("grau_dependencia", period) == 3
        existeix_discapacitat_o_dependencia = unitatDeConvivencia.any(discapacitats) + unitatDeConvivencia.any(dependencies)
        nivell_ingressos_maxim = \
            legislation(period).benefits.HG07704.ingressos_maxims[clauDependencia(existeix_discapacitat_o_dependencia)][clauNombreDeMebres(nr_membres)]
        ingressos_bruts_dins_barems = ingressos_familia_mensuals <= nivell_ingressos_maxim

        ha_pagat_12_mesos_daquesta_hipoteca = unitatDeConvivencia("ha_pagat_12_mesos_daquesta_hipoteca", period)
        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False
        quota_hipoteca_inferior_al_maxim_per_demarcacio_HG_077_03 = unitatDeConvivencia("quota_hipoteca_inferior_al_maxim_per_demarcacio_HG_077_03", period)

        return existeix_solicitant_viable \
               *resident_a_barcelona_ciutat \
               * ingressos_bruts_dins_barems \
               * ha_pagat_12_mesos_daquesta_hipoteca \
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari \
               * quota_hipoteca_inferior_al_maxim_per_demarcacio_HG_077_03
