# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

class GA_246(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "GE_246 - Targeta Rosa"

    def formula(persona, period, parameters):
        discapacitat_superior_al_33_percent = persona('grau_discapacitat', period) >= 33
        major_60 = persona("edat", period) >= 60
        es_empadronat_a_barcelona = persona('municipi_empadronament', period) == 'barcelona'

        return \
            (discapacitat_superior_al_33_percent + major_60) * \
            es_empadronat_a_barcelona