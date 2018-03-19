from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *
import numpy as np


class codi_postal_empadronament(Variable):
    column = StrCol
    entity = Persona
    definition_period = MONTH
    label = u"Postal code where person lives"
    set_input = set_input_dispatch_by_period


class codi_postal_habitatge(Variable):
    column = StrCol
    entity = Familia
    definition_period = MONTH
    label = u"Postal code where family lives"
    set_input = set_input_dispatch_by_period


class domicili_a_barcelona_ciutat(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = u"Postal code where family lives"
    set_input = set_input_dispatch_by_period