# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a familia).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from datetime import datetime
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *


def varem_irsc_016(nr_members):
        return select(                  # Fixme: Find the formula!
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
    entity = Familia
    definition_period = MONTH
    label = "The user is a Social services user"
    set_input = set_input_dispatch_by_period
    default = False


class data_obertura_expedient_serveis_socials(Variable):
    column = DateCol
    entity = Familia
    definition_period = MONTH
    label = "Date in which the user file opened"
    set_input = set_input_dispatch_by_period
    default = False


class data_obertura_expedient_anterior_a_2016_12_31(Variable):
    column = BoolCol
    entity = Familia
    definition_period = ETERNITY
    label = u"The social services expedient if filed after 2016/12/31"

    def formula(familia, period, parameters):
        return familia("data_obertura_expedient_serveis_socials", period) < datetime.strptime('2016-12-31', "%Y-%m-%d").date()


class data_alta_padro_anterior_a_2016_1_1(Variable):
    column = BoolCol
    entity = Persona
    definition_period = ETERNITY
    label = u"The social services expedient if filed after 2016/12/31"

    def formula(persona, period, parameters):
        return persona("data_alta_padro", period) < datetime.strptime('2016-01-01', "%Y-%m-%d").date()


class AE_230_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):
        te_menys_de_16_anys = persona('edat', period) < 16
        ingressos_inferiors_varem = persona.familia('familia_ingressos_bruts', period) < \
                           varem_irsc_016(persona.familia.nb_persons())
        es_usuari_serveis_socials = persona.familia('es_usuari_serveis_socials', period)
        expedient_a_serveis_socials_obert_abans_2016_12_31 = persona.familia('data_obertura_expedient_anterior_a_2016_12_31', period)
        es_empadronat_a_barcelona = persona.familia('domicili_a_barcelona_ciutat', period).all()
        alta_padro_posterior_2016_01_01 = persona('data_alta_padro_anterior_a_2016_1_1', period)
        import_ajuda = parameters(period).benefits.AE230.import_ajuda

        return where(te_menys_de_16_anys
                     * ingressos_inferiors_varem
                     * es_empadronat_a_barcelona
                     * alta_padro_posterior_2016_01_01
                     * es_usuari_serveis_socials
                     * expedient_a_serveis_socials_obert_abans_2016_12_31,
               import_ajuda, 0)
