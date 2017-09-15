# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a familia).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_spain.entities import *


class familia_disposable_income(Variable):
    column = IntCol(val_type="monetary")
    entity = Familia
    definition_period = MONTH
    label = "Total yearly income"
    set_input = set_input_divide_by_period

    def formula(familia, period):
        ingressos_membres_de_la_familia = familia.members('ingressos_disponibles', period)
        total_ingressos_familia = familia.sum(ingressos_membres_de_la_familia)
        return total_ingressos_familia


def varem_irsc_016(nr_members):
        return select(
            [nr_members == 2,
             nr_members == 3,
             nr_members == 4,
             nr_members == 5,
             nr_members == 6,
             nr_members == 7,
             nr_members == 8,
             nr_members == 9,
             nr_members == 10,
             nr_members == 11,
             nr_members > 11],
            [11951.60,
             14939.49,
             17927.39,
             20915.29,
             23903.29,
             26891.09,
             29878.99,
             32866.89,
             35854.79,
             38842.68,
             41830.58])


class es_usuari_serveis_socials(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is a Social services user"
    set_input = set_input_dispatch_by_period


class AE_230_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, legislation):
        te_menys_de_16_anys = persona('edat', period) < 16
        ingressos_inferiors_varem = persona.familia('familia_disposable_income', period) < \
                           varem_irsc_016(persona.familia.nb_persons())
        es_usuari_serveis_socials = persona('es_usuari_serveis_socials', period)
        es_empadronat_a_barcelona = persona('ciutat_empadronament', period) == "Barcelona"
        return te_menys_de_16_anys \
               * ingressos_inferiors_varem \
               * es_empadronat_a_barcelona \
               * es_usuari_serveis_socials \
               * 100
