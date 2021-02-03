from openfisca_core.model_api import *
from openfisca_barcelona.entities import *

class solicitant_TA_01_00_00_valid(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person a valid TA-01-00-00 benefitiary"

    def formula(persona, period, parameters):
        es_empadronat_a_municipi_integrat_atm = (persona("municipi_empadronament", period) == b'barcelona') \
                                 + (persona("municipi_empadronament", period) == b'municipis_atm')
        major_3 = persona("edat", period) >= 4
        menor_17 = persona("edat", period) <= 16

        compleix_criteris = major_3 * menor_17 * es_empadronat_a_municipi_integrat_atm
        return compleix_criteris


class TA_01_00_00(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "T-16"

    def formula(persona, period, parameters):
        es_solicitant_viable_TA_01_00_00 = persona('solicitant_TA_01_00_00_valid', period)
        import_ajuda = parameters(period).benefits.TA010000.import_ajuda
        return es_solicitant_viable_TA_01_00_00 * import_ajuda
