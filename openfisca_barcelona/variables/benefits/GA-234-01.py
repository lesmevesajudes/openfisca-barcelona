# -*- coding: utf-8 -*-
# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres >= 4],
                  ['1', '2', '3', '4'])

class GA_234_01(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "GA_234_01 - Ajuda Vincles (A)"

    def formula(persona, period, parameters):
        requeriments_generals = persona('GA_234', period)
        no_te_dispositiu_propi = persona("te_dispositiu_inteligent_amb_connexio_a_internet", period) == False
        edat_major_74 = persona("edat", period) > 74
        edat_menor_75 = persona("edat", period) < 75

        ingressos_bruts_familia = persona.familia('familia_ingressos_bruts', period.last_year)
        nr_membres = persona.familia_fins_a_segon_grau.nb_persons()
        viu_sola = nr_membres == 1
        llindar_ingressos_menor_75_anys = parameters(period).benefits.GA234.llindars_ingressos['menys_de_75'][clauNombreDeMebres(nr_membres)]
        llindar_ingressos_75_anys_o_mes = parameters(period).benefits.GA234.llindars_ingressos['mes_de_74']
        compleix_nivell_ingressos_menor_75_anys = ingressos_bruts_familia <= llindar_ingressos_menor_75_anys
        compleix_nivell_ingressos_75_anys_o_mes = ingressos_bruts_familia <= llindar_ingressos_75_anys_o_mes
        compleix_requisits_75_anys_o_mes = edat_major_74 * viu_sola * compleix_nivell_ingressos_75_anys_o_mes
        compleix_requisits_menor_75_anys = edat_menor_75 * compleix_nivell_ingressos_menor_75_anys
        compleix_els_requeriments = \
            requeriments_generals \
            * no_te_dispositiu_propi \
            * (compleix_requisits_menor_75_anys + compleix_requisits_75_anys_o_mes)

        return compleix_els_requeriments
