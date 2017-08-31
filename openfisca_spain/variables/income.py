# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a household).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_spain.entities import *


# This variable is a pure input: it doesn't have a formula
class salary(Variable):
    column = FloatCol
    entity = Person
    definition_period = MONTH
    label = "Salary"


class disposable_income(Variable):
    column = FloatCol
    entity = Person
    definition_period = MONTH
    label = "Actual amount available to the person at the end of the month"
    set_input = set_input_divide_by_period