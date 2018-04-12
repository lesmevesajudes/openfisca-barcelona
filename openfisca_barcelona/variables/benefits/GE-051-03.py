from numpy.ma import logical_not
from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class victima_violencia_de_genere(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is a victim of genre violence"
    set_input = set_input_dispatch_by_period
    default = False


class GE_051_03_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "RAI 3 - Per victimes de violencia de genere o domestica"

    def formula(persona, period, parameters):
        requeriments_generals = persona('GE_051_mensual', period)
        victima_violencia_de_genere = persona('victima_violencia_de_genere', period)
        inscrit_com_a_demandant_docupacio = persona('inscrit_com_a_demandant_docupacio', period)
        beneficiari_ajuts_per_violencia_de_genere = \
            persona('beneficiari_ajuts_per_violencia_de_genere', period) == False

        compleix_els_requeriments = \
            requeriments_generals \
            * victima_violencia_de_genere \
            * inscrit_com_a_demandant_docupacio \
            * beneficiari_ajuts_per_violencia_de_genere

        import_ajuda = parameters(period).benefits.GE051.import_ajuda
        return where(compleix_els_requeriments, import_ajuda, 0)
