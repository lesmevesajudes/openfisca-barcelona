from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class ha_participat_en_un_proces_de_mediacio(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "True if person is a victim of male violence"
    default_value = False


class HA_001(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "RENDA GARANTIDA CIUTADANA"

    def formula(persona, period, legislation):
        ha_participat_en_un_proces_de_mediacio = persona("ha_participat_en_un_proces_de_mediacio", period)
        tipus_document_identitat = persona("tipus_document_identitat", period)
        return ha_participat_en_un_proces_de_mediacio * tipus_document_identitat
