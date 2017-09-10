# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_spain.entities import *
import numpy as np

class DISCSUP33(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class ESGSUBSDESOC(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class DEMANDOC12M(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class INGINF530(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('disposable_income', period) < 530

class CAPMEMBREINGSUP530(Variable):
    column = BoolCol
    entity = Household
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(household, period, legislation):
        qq = household.members('INGINF530', period)
        return household.all(qq)


class ACCRESFEIN(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period



class NORAI365(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class NOTRESRAIANT(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class TREBALLACOMPTEPROPI(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class INGCPENITENCIARI(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period



class PRESTSSINCOMPFEINA(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class BENAJVIOGENNOPROGOC(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class GE_051_1_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "GE_051_1 - RAI 1 - Ajuda discapacitats 33% o superior"

    def formula(person, period, legislation):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = person.household('CAPMEMBREINGSUP530', period)
        discapacitat_superior_al_33_percent = person('DISCSUP33', period)
        ESGSUBSDESOC = person('ESGSUBSDESOC', period)
        DEMANDOC12M = person('DEMANDOC12M', period)
        ACCRESFEIN = person('ACCRESFEIN', period)
        NORAI365 = person('NORAI365', period)
        NOTRESRAIANT = person('NOTRESRAIANT', period)
        NOTREBALLACOMPTEPROPI = person('TREBALLACOMPTEPROPI', period) == False
        NOINGCPENITENCIARI = person('INGCPENITENCIARI', period) == False
        NOPRESTSSINCOMPFEINA = person('PRESTSSINCOMPFEINA', period) == False
        NOBENAJVIOGENNOPROGOC = person('BENAJVIOGENNOPROGOC', period) == False
        compleix_els_requeriments = cap_membre_amb_ingressos_superiors_a_530_mensuals * \
                                    discapacitat_superior_al_33_percent * \
                                    ESGSUBSDESOC * DEMANDOC12M * ACCRESFEIN * NORAI365 * NOTRESRAIANT * \
                                    NOTREBALLACOMPTEPROPI * \
                                    NOINGCPENITENCIARI * \
                                    NOPRESTSSINCOMPFEINA * \
                                    NOBENAJVIOGENNOPROGOC

        return where(compleix_els_requeriments, 426, 0)
