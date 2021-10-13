from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.H import demarcacioDeLHabitatge

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres >= 4],
                  ['un', 'dos', 'tres', 'quatreomes'])

def clauDependencia(valor):
    return select([valor == 0, valor > 0],
                  ['sense_discapacitat_dependencia', 'amb_discapacitat_dependencia'])

class esta_o_ha_estat_en_erto(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has been in erto situation"
    set_input = set_input_dispatch_by_period
    default_value = False

class grau_dependencia(Variable):
    value_type = int
    entity = Persona
    definition_period = MONTH
    label = "User's grade of dependency"
    set_input = set_input_dispatch_by_period
    default_value = 0

class quota_lloguer_inferior_al_maxim_HG_02_00_00(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Monthly fee udner the maximum allowed"
    default_value = False

    def formula(unitatDeConvivencia, period, legislation):
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        return import_del_lloguer <= 800

class pot_ser_solicitant_HG_02_00_00(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        empadronat_a_barcelona = (persona("municipi_empadronament", period) == b'barcelona')
        situacio_laboral = persona('situacio_laboral', period)
        aturat = situacio_laboral == situacio_laboral.possible_values.aturat
        amb_erto = persona('esta_o_ha_estat_en_erto', period)
        return empadronat_a_barcelona * (aturat + amb_erto)

class HG_02_00_00(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "AJUTS ESPECIAL URGENCIA DEUTE LLOGUER COVID19"

    def formula(unitatDeConvivencia, period, parameters):
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HG_02_00_00", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)

        nr_membres = unitatDeConvivencia.nb_persons()
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period) > 33
        dependencies = unitatDeConvivencia.members("grau_dependencia", period) == 3
        existeix_discapacitat_o_dependencia = unitatDeConvivencia.any(discapacitats) + unitatDeConvivencia.any(dependencies)
        ingressos_maxims = parameters(period).benefits.HG02.ingressos_maxims
        nivell_ingressos_maxim = \
            parameters(period).benefits.HG02.ingressos_maxims[clauDependencia(existeix_discapacitat_o_dependencia)][clauNombreDeMebres(nr_membres)]
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts", period.last_year)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 12
        ingressos_bruts_dins_barems = ingressos_familia_mensuals <= nivell_ingressos_maxim

        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False
        quota_lloguer_inferior_al_maxim_HG_02_00_00 = unitatDeConvivencia("quota_lloguer_inferior_al_maxim_HG_02_00_00", period)
        demarcacio_de_lhabitatge = unitatDeConvivencia("demarcacio_de_lhabitatge", period)
        resident_a_barcelona_ciutat = \
            unitatDeConvivencia("demarcacio_de_lhabitatge", period) == demarcacioDeLHabitatge.barcelona_ciutat

        return existeix_solicitant_viable \
               * ingressos_bruts_dins_barems \
               * resident_a_barcelona_ciutat \
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari \
               * quota_lloguer_inferior_al_maxim_HG_02_00_00
