from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.H import clauIRSCPonderat, clauMultiplicadors

class ha_rebut_una_notificacio_de_desnonament(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False

class HG_077_04_01(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "COMPLEMENT AJUTS LLOGUER ESPECIAL URGENCIA"

    def formula(unitatDeConvivencia, period, legislation):
        return unitatDeConvivencia('HG_077_04', period) \
               * unitatDeConvivencia('ha_rebut_una_notificacio_de_desnonament', period)
