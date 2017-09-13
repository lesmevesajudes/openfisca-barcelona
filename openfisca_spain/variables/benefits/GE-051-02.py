from openfisca_core.model_api import *
from openfisca_spain.entities import *


class MAJ45ANYS(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class DESOCUP(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class TREBALLEXTR6M(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class GE_051_02_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "GE_051_02 - RAI 2 - Per emigrants retornats major de 45 anys"

    def formula(person, period, legislation):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = person.household('CAPMEMBREINGSUP530', period)
        MAJ45ANYS = person('MAJ45ANYS', period)
        DESOCUP = person('DESOCUP', period)
        TREBALLEXTR6M = person('TREBALLEXTR6M', period)
        NORAI12M = person('NORAI12M', period)
        NOTRESRAIANT = person('NOTRESRAIANT', period)
        NOTREBALLACOMPTEPROPI = person('TREBALLACOMPTEPROPI', period) == False
        NOINGCPENITENCIARI = person('INGCPENITENCIARI', period) == False
        NOPRESTSSINCOMPFEINA = person('PRESTSSINCOMPFEINA', period) == False

        compleix_els_requeriments = cap_membre_amb_ingressos_superiors_a_530_mensuals * \
                                    MAJ45ANYS * \
                                    DESOCUP * \
                                    TREBALLEXTR6M * \
                                    NORAI12M * \
                                    NOTRESRAIANT * \
                                    NOTREBALLACOMPTEPROPI * \
                                    NOINGCPENITENCIARI * \
                                    NOPRESTSSINCOMPFEINA

        return where(compleix_els_requeriments, 426, 0)
