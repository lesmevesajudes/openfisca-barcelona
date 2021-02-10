from openfisca_core.model_api import *
from openfisca_barcelona.entities import *

class percep_ajut_serveis_socials_municipals(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user is receiving a benefit from municipality below 950€"
    set_input = set_input_dispatch_by_period
    default_value = False

class percep_prestacio_menys_de_950(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user is receiving a benefit below 950€"
    set_input = set_input_dispatch_by_period
    default_value = False

class solicitant_TA_02_00_00_valid(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person a valid TA-02-00-00 benefitiary"

    def formula(persona, period, parameters):
        situacio_laboral = persona('situacio_laboral', period)
        aturat = situacio_laboral == situacio_laboral.possible_values.aturat
        demandant_ocupacio_llarga_durada = (persona("inscrit_com_a_demandant_docupacio_mes_de_12_mesos", period) == True)
        es_empadronat_a_municipi_integrat_atm = (persona("municipi_empadronament", period) == b'barcelona') + (persona("municipi_empadronament", period) == b'municipis_atm')
        percep_ajut_serveis_socials_municipals = (persona("percep_ajut_serveis_socials_municipals", period) == True)
        no_gaudeix_altres_prestacions = (persona("gaudeix_de_prestacio_contributiva_o_subsidi_desocupacio", period) == False)
        percep_prestacio_menys_de_950 = (persona("percep_prestacio_menys_de_950", period) == True)

        compleix_criteris = aturat * es_empadronat_a_municipi_integrat_atm * (\
                            percep_prestacio_menys_de_950 \
                            + (percep_prestacio_menys_de_950 + no_gaudeix_altres_prestacions) * demandant_ocupacio_llarga_durada \
                            + (percep_ajut_serveis_socials_municipals * no_gaudeix_altres_prestacions) \
                        )

        return compleix_criteris

class TA_02_00_00(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "T-Usual"

    def formula(persona, period, parameters):
        es_solicitant_viable_TA_02_00_00 = persona('solicitant_TA_02_00_00_valid', period)
        import_ajuda = parameters(period).benefits.TA020000.import_ajuda
        return es_solicitant_viable_TA_02_00_00 * import_ajuda
