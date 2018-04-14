# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *


class grau_discapacitat(Variable):
    value_type = int
    entity = Persona
    definition_period = MONTH
    label = "User's grade of disability"
    set_input = set_input_dispatch_by_period
    default_value = 0


class ha_esgotat_prestacio_de_desocupacio(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user is not receiving any benefit for not having a job"
    set_input = set_input_dispatch_by_period
    default_value = False


class demandant_d_ocupacio_durant_12_mesos(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has been searching for a job at least 12 months"
    set_input = set_input_dispatch_by_period
    default_value = False


class inscrit_com_a_demandant_docupacio(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has been searching for a job at least 12 months"
    set_input = set_input_dispatch_by_period
    default_value = False

class percep_prestacions_incompatibles_amb_la_feina(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has some benefit that does not let her work"
    set_input = set_input_dispatch_by_period
    default_value = False


class durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "During the previous month the user has applied for a job"
    set_input = set_input_dispatch_by_period
    default_value = False


class beneficiari_ajuts_per_violencia_de_genere(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has a violence of genre  benefit"
    set_input = set_input_dispatch_by_period
    default_value = False


class GE_051_01_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "GE_051_1 - RAI 1 - Ajuda discapacitats 33% o superior"

    def formula(persona, period, parameters):
        requeriments_generals = persona('GE_051_mensual', period)
        discapacitat_superior_al_33_percent = persona('grau_discapacitat', period) > 33
        no_beneficiari_ajuts_per_violencia_de_genere = \
            persona('beneficiari_ajuts_per_violencia_de_genere', period) == False
        ha_esgotat_prestacio_de_desocupacio = persona('ha_esgotat_prestacio_de_desocupacio', period)
        demandant_d_ocupacio_durant_12_mesos = persona('demandant_d_ocupacio_durant_12_mesos', period)
        durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina = \
            persona('durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina', period)

        compleix_els_requeriments = \
            requeriments_generals \
            * discapacitat_superior_al_33_percent \
            * no_beneficiari_ajuts_per_violencia_de_genere \
            * ha_esgotat_prestacio_de_desocupacio \
            * demandant_d_ocupacio_durant_12_mesos \
            * durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina

        import_ajuda = parameters(period).benefits.GE051.import_ajuda

        return where(compleix_els_requeriments, import_ajuda, 0)
