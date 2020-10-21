# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

class GE_051_04_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "GE_051_0 - RAI 0 - Persones aturades de llarga durada"

    def formula(persona, period, parameters):
        requeriments_generals = persona('GE_051_mensual', period)
        major_de_45_anys = persona('major_de_45_anys', period)
        ha_esgotat_prestacio_de_desocupacio = persona('ha_esgotat_prestacio_de_desocupacio', period)
        inscrit_com_a_demandant_docupacio_mes_de_12_mesos = persona('inscrit_com_a_demandant_docupacio_mes_de_12_mesos', period)

        compleix_els_requeriments = \
            requeriments_generals \
            * major_de_45_anys \
            * ha_esgotat_prestacio_de_desocupacio \
            * inscrit_com_a_demandant_docupacio_mes_de_12_mesos

        import_ajuda = parameters(period).benefits.GE051.import_ajuda

        return where(compleix_els_requeriments, import_ajuda, 0)
