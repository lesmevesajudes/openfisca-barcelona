from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.H import clauIRSCPonderat, clauMultiplicadors, demarcacioDeLHabitatge, clauNombreDeMebres, clauDependencia


class lloguer_inferior_al_maxim_HG_077_02(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        demarcacio_de_lhabitatge = unitatDeConvivencia("demarcacio_de_lhabitatge", period)
        lloguer_maxim = legislation(period).benefits.HG07704.import_lloguer_maxim[demarcacio_de_lhabitatge]
        return import_del_lloguer <= lloguer_maxim * import_del_lloguer > 0 


class pot_ser_solicitant_HG_077_02(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        tipus_document_identitat = persona("tipus_document_identitat", period)
        has_DNI = tipus_document_identitat == tipus_document_identitat.possible_values.DNI
        has_NIE = tipus_document_identitat == tipus_document_identitat.possible_values.NIE
        empadronat_a_catalunya = (persona("municipi_empadronament", period) == b'barcelona') \
        + (persona("municipi_empadronament", period) == b'altres') \
        + (persona("municipi_empadronament", period) == b'municipis_atm')
        titular_contracte_de_lloguer = persona("titular_contracte_de_lloguer", period)

        return (has_DNI + has_NIE) \
               * empadronat_a_catalunya \
               * titular_contracte_de_lloguer


class pot_ser_solicitant_HG_077_02_i_victima_violencia_masclista(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit and is victim of sexist violence"
    default_value = False

    def formula(persona, period, legislation):
        es_possible_solicitant = persona("pot_ser_solicitant_HG_077_02", period)
        es_victima_violencia_masclista = persona('victima_violencia_de_genere', period)

        return es_possible_solicitant *  es_victima_violencia_masclista


class HG_077_02(Variable):
    value_type = bool
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "AJUTS PER PERDUA D HABITATGE PER DESNONAMENT O EXECUCIO HIPOTECARIA"

    def formula(unitatDeConvivencia, period, legislation):
        nr_membres = unitatDeConvivencia.nb_persons()
        resident_a_barcelona_ciutat = \
            unitatDeConvivencia("demarcacio_de_lhabitatge", period) == demarcacioDeLHabitatge.barcelona_ciutat
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HG_077_02", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts_ultims_sis_mesos", period)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 6 / nr_membres

        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period) > 33
        dependencies = unitatDeConvivencia.members("grau_dependencia", period) == 3
        existeix_discapacitat_o_dependencia = unitatDeConvivencia.any(discapacitats) + unitatDeConvivencia.any(dependencies)
        nivell_ingressos_maxim = \
            legislation(period).benefits.HG07704.ingressos_maxims[clauDependencia(existeix_discapacitat_o_dependencia)][clauNombreDeMebres(nr_membres)]
        ingressos_bruts_dins_barems = ingressos_familia_mensuals <= nivell_ingressos_maxim

        ha_perdut_lhabitatge_en_els_ultims_2_anys = unitatDeConvivencia("ha_perdut_lhabitatge_en_els_ultims_2_anys", period)
        es_desnonament = unitatDeConvivencia('ha_rebut_una_notificacio_de_desnonament', period)

        es_solicitant_i_victima_violencia_masclista = unitatDeConvivencia.members("pot_ser_solicitant_HG_077_02_i_victima_violencia_masclista", period)
        existeix_solicitant_i_victima_violencia_masclista = unitatDeConvivencia.any(es_solicitant_i_victima_violencia_masclista)

        lloguer_inferior_al_maxim = unitatDeConvivencia("lloguer_inferior_al_maxim_HG_077_02", period)
        ha_pagat_almenys_3_quotes_del_lloguer = unitatDeConvivencia("ha_pagat_almenys_3_quotes_del_lloguer", period)
        no_deute_lloguer = \
            unitatDeConvivencia("existeix_deute_en_el_pagament_del_lloguer", period) == False

        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False


        return (ha_perdut_lhabitatge_en_els_ultims_2_anys + existeix_solicitant_i_victima_violencia_masclista) \
               * existeix_solicitant_viable \
               * ha_pagat_almenys_3_quotes_del_lloguer \
               * no_deute_lloguer \
               * ingressos_bruts_dins_barems \
               * lloguer_inferior_al_maxim\
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari
