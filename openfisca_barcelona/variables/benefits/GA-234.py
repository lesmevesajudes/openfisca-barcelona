# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

class sentirse_sol(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user feels lonely"
    set_input = set_input_dispatch_by_period
    default_value = False

class te_dispositiu_inteligent_amb_connexio_a_internet(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has an smartphone or tablet"
    set_input = set_input_dispatch_by_period
    default_value = False

class GA_234(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "GA_234 - Ajuda Vincles"

    def formula(persona, period, parameters):
        major_65 = persona("edat", period) >= 65
        es_empadronat_a_barcelona = persona('municipi_empadronament', period) == b'barcelona'
        se_sent_sol = persona('sentirse_sol', period)
        return \
            major_65 * \
            es_empadronat_a_barcelona * \
            se_sent_sol
