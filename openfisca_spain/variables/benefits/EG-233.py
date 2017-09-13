from openfisca_core.model_api import *
from openfisca_spain.entities import *


class GUARICUS(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class ESCOLARITZAT(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class MENJADOR(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class BECAMENJADOR(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

class NR_INF_2416_80(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('disposable_income', period) * 12 < 2416.80   #FIXME: I should not be * define a concept for
                                                                    # yearly total income


class NR_INF_2900_20(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('disposable_income', period) * 12 < 2900.20


class NR_INF_1450_08(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('disposable_income', period) * 12 < 1450.08


class NR_INF_1740_12(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('disposable_income', period) * 12 < 1740.12


class EG_233_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "EG_233 - AJUTS INDIVIDUALS DE MENJADOR CIUTAT BARCELONA"

    def formula(person, period, legislation):

        ESCOLARITZAT = person('ESCOLARITZAT', period)
        MENJADOR = person('MENJADOR', period)
        NOBECAMENJADOR = person('BECAMENJADOR', period) == False
        ESCHILD = person.has_role(Household.CHILD)
        CUSTODIA = person.household.first_parent('GUARICUS', period)
        compleix_els_requeriments = CUSTODIA * \
                                    ESCOLARITZAT * \
                                    MENJADOR * \
                                    NOBECAMENJADOR * \
                                    ESCHILD
        nr_adult_demandant = person.household.first_parent('disposable_income', period) * 12
        nr_adult_secundari = person.household.second_parent('disposable_income', period) * 12

        other_adult_satisfy_ordinari_nr = person.household.all(person.household.members('NR_INF_2416_80', period), role=Household.OTHER_ADULT)

        children_satisfy_ordinari_nr = person.household.all(person.household.members('NR_INF_2900_20', period), role=Household.CHILD)

        compleix_ajut_ordinari = (nr_adult_demandant < 9667.30) *\
                                 (nr_adult_secundari < 4833.60) *\
                                 other_adult_satisfy_ordinari_nr * children_satisfy_ordinari_nr

        other_adult_satisfy_extraordinari_nr = person.household.all(person.household.members('NR_INF_1450_08', period), role=Household.OTHER_ADULT)

        children_satisfy_extraordinari_nr = person.household.all(person.household.members('NR_INF_1740_12', period), role=Household.CHILD)

        compleix_ajut_extraordinari = (nr_adult_demandant < 5800.38) * \
                                 (nr_adult_secundari < 2900.16) * \
                                 other_adult_satisfy_extraordinari_nr * children_satisfy_extraordinari_nr

        import_EG_233 = select([compleix_ajut_extraordinari, compleix_ajut_ordinari], [6, 3])

        print compleix_els_requeriments, compleix_ajut_ordinari, compleix_ajut_extraordinari, import_EG_233
        return compleix_els_requeriments * import_EG_233
