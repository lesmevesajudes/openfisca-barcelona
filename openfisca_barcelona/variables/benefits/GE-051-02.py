from numpy.ma import logical_not
from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class major_de_45_anys(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user is older than 45 years"
    set_input = set_input_dispatch_by_period
    default_value = False

    def formula(persona, period, parameters):
        return persona('edat', period) >= 45


class aturat(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has no job"
    set_input = set_input_dispatch_by_period
    default_value = False


class ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has been working abroad for at least 6 months and has come back to country in the last 12"
    set_input = set_input_dispatch_by_period
    default_value = False


class GE_051_02_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "GE_051_02 - RAI 2 - Per emigrants retornats major de 45 anys"

    def formula(persona, period, parameters):
        requeriments_generals = persona('GE_051_mensual', period)
        major_de_45_anys = persona('major_de_45_anys', period)
        ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos = persona('ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos', period)
        inscrit_com_a_demandant_docupacio = persona('inscrit_com_a_demandant_docupacio', period)

        compleix_els_requeriments = \
            requeriments_generals \
            * major_de_45_anys \
            * ha_treballat_a_l_estranger_6_mesos_i_ha_retornat_en_els_ultims_12_mesos \
            * inscrit_com_a_demandant_docupacio

        import_ajuda = parameters(period).benefits.GE051.import_ajuda

        return where(compleix_els_requeriments, import_ajuda, 0)
