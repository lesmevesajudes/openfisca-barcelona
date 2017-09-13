from openfisca_core.model_api import *
from openfisca_spain.entities import *


class VICVILGEN(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class GE_051_03_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "RAI 3 - Per victimes de violencia de genere o domestica"

    def formula(person, period, legislation):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = person.household('CAPMEMBREINGSUP530', period)
        VICVILGEN = person('VICVILGEN', period)
        DESOCUP = person('DESOCUP', period)
        NORAI12M = person('NORAI12M', period)
        NOTRESRAIANT = person('NOTRESRAIANT', period)
        NOTREBALLACOMPTEPROPI = person('TREBALLACOMPTEPROPI', period) == False
        NOINGCPENITENCIARI = person('INGCPENITENCIARI', period) == False
        NOPRESTSSINCOMPFEINA = person('PRESTSSINCOMPFEINA', period) == False
        BENAJVIOGENNOPROGOC = person('BENAJVIOGENNOPROGOC', period) == False

        compleix_els_requeriments = cap_membre_amb_ingressos_superiors_a_530_mensuals * \
                                    VICVILGEN * \
                                    DESOCUP * \
                                    NORAI12M * \
                                    NOTRESRAIANT * \
                                    NOTREBALLACOMPTEPROPI * \
                                    NOINGCPENITENCIARI * \
                                    NOPRESTSSINCOMPFEINA * \
                                    BENAJVIOGENNOPROGOC

        return where(compleix_els_requeriments, 426, 0)
