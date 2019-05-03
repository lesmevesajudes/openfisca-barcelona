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
        
        ingressos_bruts_familia = persona.familia('familia_ingressos_bruts', period.last_year) 
        nr_membres = persona.familia_fins_a_segon_grau.nb_persons()
        llindar_ingressos_minims = parameters(period).benefits.GA234.llindars_ingressos['A'][clauNombreDeMebres(nr_membres)]
        llindar_ingressos = parameters(period).benefits.GA234.llindars_ingressos['B'][clauNombreDeMebres(nr_membres)]
        compleix_ingressos_minims = ingressos_bruts_familia > llindar_ingressos_minims
        compleix_ingressos_maxims = ingressos_bruts_familia <= llindar_ingressos
        
        compleix_els_requeriments = \
            requeriments_generals \
            * compleix_ingressos_minims \
            * compleix_ingressos_maxims

        return compleix_els_requeriments
