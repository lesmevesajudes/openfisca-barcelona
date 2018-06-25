from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *
import numpy as np


class codi_postal_empadronament(Variable):
    value_type = str
    entity = Persona
    definition_period = MONTH
    label = u"Postal code where person lives"
    set_input = set_input_dispatch_by_period


class codi_postal_habitatge(Variable):
    value_type = str
    max_length = 5
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = u"Postal code where family lives"
    set_input = set_input_dispatch_by_period


class municipi_empadronament(Variable):
    value_type = str
    max_length = 20
    entity = Persona
    definition_period = MONTH
    label = u"City or town where family lives"
    set_input = set_input_dispatch_by_period


class domicili_a_barcelona_ciutat(Variable):
    value_type = bool
    entity = Familia
    definition_period = MONTH
    label = u"Postal code where family lives"
    set_input = set_input_dispatch_by_period


class porta_dos_anys_o_mes_empadronat_a_catalunya(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = u"Has this person been living in Catalunya for more than 2 years"
    set_input = set_input_dispatch_by_period
    default_value = False