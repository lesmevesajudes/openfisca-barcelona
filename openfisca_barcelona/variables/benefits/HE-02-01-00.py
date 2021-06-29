from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.H import clauIRSCPonderat, clauMultiplicadors, demarcacioDeLHabitatge

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres >= 4],
                  ['1', '2', '3', '4_o_mes'])

class lloguer_inferior_al_maxim_per_barcelona_HE_02_01_00(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "place rental below maximum allowed"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period)
        persona_amb_discapacitat = unitatDeConvivencia.any(discapacitats)
        discapacitat_amb_lloguer_inferor_al_maxim = persona_amb_discapacitat * (import_del_lloguer <= 900)
        lloger_inferior_a_limit_barcelona = (import_del_lloguer <= 800)
        return discapacitat_amb_lloguer_inferor_al_maxim + lloger_inferior_a_limit_barcelona

class ingressos_no_inferiors_a_lloguer_HE_02_01_00(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "income beyond minimum allowed"
    default_value = False

    def formula(unitatDeConvivencia, period, parameters):
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts", period.last_year)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 12

        return import_del_lloguer <= ingressos_familia_mensuals


class pot_ser_solicitant_HE_02_01_00(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        major_65 = persona("edat", period) > 64
        empadronat_a_barcelona = (persona("municipi_empadronament", period) == b'barcelona')
        temps_empadronat_a_lhabitatge = persona("temps_empadronat_habitatge_actual", period)
        empadronat_a_lhabitatge = temps_empadronat_a_lhabitatge != temps_empadronat_a_lhabitatge.possible_values.no_empadronat
        titular_contracte_de_lloguer = persona("titular_contracte_de_lloguer", period)

        return major_65 \
               * empadronat_a_barcelona \
               * empadronat_a_lhabitatge \
               * titular_contracte_de_lloguer

class HE_02_01_00(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = u"SUBVENCIONS PAGAMENT LLOGUER GENT GRAN"

    def formula(unitatDeConvivencia, period, parameters):
        nr_membres = unitatDeConvivencia.nb_persons()
        pot_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HE_02_01_00", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(pot_solicitar)
        no_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False
        no_deute_lloguer = \
            unitatDeConvivencia("existeix_deute_en_el_pagament_del_lloguer", period) == False
        ha_pagat_almenys_3_quotes_del_lloguer = \
            unitatDeConvivencia("ha_pagat_almenys_3_quotes_del_lloguer", period) == True
        lloguer_inferior_al_maxim = unitatDeConvivencia("lloguer_inferior_al_maxim_per_barcelona_HE_02_01_00", period)
        resident_a_barcelona_ciutat = \
            unitatDeConvivencia("demarcacio_de_lhabitatge", period) == demarcacioDeLHabitatge.barcelona_ciutat
        ingressos_no_inferiors_a_lloguer = unitatDeConvivencia("ingressos_no_inferiors_a_lloguer_HE_02_01_00", period)

        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts", period.last_year)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 12
        numero_persones = clauNombreDeMebres(nr_membres)
        nivell_ingressos_maxim = \
            parameters(period).benefits.HE02.maxim_ingressos[numero_persones]
        ingressos_compleix_maxim = ingressos_familia_mensuals <= nivell_ingressos_maxim


        return existeix_solicitant_viable \
               * lloguer_inferior_al_maxim \
               * (no_deute_lloguer + ha_pagat_almenys_3_quotes_del_lloguer) \
               * no_relacio_de_parentiu_amb_el_propietari \
               * no_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * resident_a_barcelona_ciutat \
               * ingressos_no_inferiors_a_lloguer \
               * ingressos_compleix_maxim
