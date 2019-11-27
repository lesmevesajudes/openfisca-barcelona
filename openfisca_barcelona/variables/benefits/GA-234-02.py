# -*- coding: utf-8 -*-
# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres >= 4],
                  ['1', '2', '3', '4'])

class GA_234_02(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "GA_234_02 - Ajuda Vincles (B)"

    def formula(persona, period, parameters):
        requeriments_generals = persona('GA_234', period)
        te_dispositiu_propi = persona("te_dispositiu_inteligent_amb_connexio_a_internet", period)


        compleix_els_requeriments = \
            requeriments_generals \
            * te_dispositiu_propi

        return compleix_els_requeriments
