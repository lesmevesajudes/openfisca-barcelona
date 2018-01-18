# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a familia).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *


class ciutat_empadronament(Variable):
    column = StrCol
    entity = Persona
    definition_period = MONTH
    label = u"City Where the user is censed"
    set_input = set_input_dispatch_by_period


class empadronat_a_la_ciutat_de_barcelona(Variable):
    column = StrCol
    entity = Persona
    definition_period = MONTH
    label = u"The user is censed in Barcelona city"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        return persona("ciutat_empadronament", period) == "Barcelona"