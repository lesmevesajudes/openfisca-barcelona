# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a household).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_spain.entities import *


class household_disposable_income(Variable):
    column = IntCol(val_type="monetary")
    entity = Household
    definition_period = MONTH
    label = "Total yearly income"
    set_input = set_input_divide_by_period

    def formula(household, period):
        salaries = household.members('disposable_income', period)
        sum_salaries = household.sum(salaries)
        return sum_salaries


def varem_irsc_016(nr_members):
        return select(
            [nr_members == 2,
             nr_members == 3,
             nr_members == 4,
             nr_members == 5,
             nr_members == 6,
             nr_members == 7,
             nr_members == 8,
             nr_members == 9,
             nr_members == 10,
             nr_members == 11,
             nr_members > 11],
            [11951.60,
             14939.49,
             17927.39,
             20915.29,
             23903.29,
             26891.09,
             29878.99,
             32866.89,
             35854.79,
             38842.68,
             41830.58])


class usuari_serveis_socials(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is a Social services user"
    set_input = set_input_dispatch_by_period


class AE_230_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(person, period, legislation):
        age_requirement = person('age', period) < 16
        income_condition = person.household('household_disposable_income', period) < \
                           varem_irsc_016(person.household.nb_persons())
        usuari_serveis_socials_condition = person('usuari_serveis_socials', period)
        empadronat_a_barcelona_condition = person('ciutat_empadronament', period) == "Barcelona"
        return age_requirement \
               * income_condition \
               * empadronat_a_barcelona_condition \
               * usuari_serveis_socials_condition \
               * 100
