# -*- coding: utf-8 -*-
# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres >= 4],
                  ['1', '2', '3', '4'])

class GA_246_02(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "GA_246_02 - Targeta Rosa (Reduïda)"

    def formula(persona, period, parameters):
        requeriments_generals = persona('GA_246', period)
        
        ingressos_bruts_familia = persona.familia('familia_ingressos_bruts', period.last_year) 
        nr_membres = persona.familia_fins_a_segon_grau.nb_persons()
        llindar_ingressos_reduida = parameters(period).benefits.GA246.llindars_ingressos['reduida'][clauNombreDeMebres(nr_membres)]
        llindar_ingressos_gratuita = parameters(period).benefits.GA246.llindars_ingressos['gratuita'][clauNombreDeMebres(nr_membres)]
        compleix_nivell_ingressos = (ingressos_bruts_familia > llindar_ingressos_gratuita) * (ingressos_bruts_familia <= llindar_ingressos_reduida) 
        
        compleix_els_requeriments = \
            requeriments_generals \
            * compleix_nivell_ingressos

        return compleix_els_requeriments
