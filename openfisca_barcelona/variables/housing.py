# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a familia).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *


class ciutat_empadronament(Variable):
    value_type = str
    entity = Persona
    definition_period = MONTH
    label = u"City Where the user is censed"
    set_input = set_input_dispatch_by_period


class empadronat_a_la_ciutat_de_barcelona(Variable):
    value_type = str
    entity = Persona
    definition_period = MONTH
    label = u"The user is censed in Barcelona city"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        return persona("ciutat_empadronament", period) == "Barcelona"


class anys_empadronat_a_barcelona(Variable):
    value_type = int
    entity = Persona
    definition_period = MONTH
    label = u"how many years have this person been living in barcelona"

class titular_contracte_de_lloguer(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = u"is the user who rents the house"