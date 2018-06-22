from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class ha_participat_en_un_proces_de_mediacio(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "True if person is a victim of male violence"
    default_value = False


class HA_001(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "RENDA GARANTIDA CIUTADANA"

    def formula(unitatDeConvivencia, period, legislation):
        ha_participat_en_un_proces_de_mediacio = unitatDeConvivencia("ha_participat_en_un_proces_de_mediacio", period)
        return ha_participat_en_un_proces_de_mediacio
