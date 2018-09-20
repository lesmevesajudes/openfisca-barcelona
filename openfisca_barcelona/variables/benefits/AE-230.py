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
    value_type = bool
    entity = Familia
    definition_period = MONTH
    label = "The user is a Social services user"
    set_input = set_input_dispatch_by_period
    default_value = False


class data_obertura_expedient_serveis_socials(Variable):
    value_type = date
    entity = Familia
    definition_period = MONTH
    label = "Date in which the user file opened"
    set_input = set_input_dispatch_by_period


class ordre_del_menor(Variable):
    value_type = int
    entity = Persona
    definition_period = ETERNITY
    label = "Ordinal number of this person within a family"


class data_obertura_expedient_anterior_a_2016_12_31(Variable):
    value_type = bool
    entity = Familia
    definition_period = ETERNITY
    label = u"The social services expedient if filed after 2016/12/31"

    def formula(familia, period, parameters):
        return familia("data_obertura_expedient_serveis_socials", period) < datetime.strptime('2016-12-31', "%Y-%m-%d").date()


class data_alta_padro_valida_AE_230(Variable):
    value_type = bool
    entity = Persona
    definition_period = ETERNITY
    label = u"The social services expedient if filed after 2016/12/31"

    def formula(persona, period, parameters):
        return (
                (persona("edat", period) <= 2)
                + (
                        (persona("edat", period) > 2)
                        * (persona("anys_empadronat_a_barcelona", period) >= 2)))


class solicitant_AE_230_valid(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH

    def formula(persona, period, parameters):
        return persona('data_alta_padro_valida_AE_230', period) * persona.has_role(Familia.SUSTENTADOR_I_CUSTODIA)

def clau_ordre_del_menor(membres):
    return select([membres == 0, membres == 1, membres >= 2],
                  ['primer', 'segon', 'tercer_o_mes']
                  )


def clau_custodia(tipus_custodia):
    return select([tipus_custodia == tipus_custodia.possible_values.compartida, tipus_custodia != tipus_custodia.possible_values.compartida],
                  ['compartida', 'total']
                  )


class compleix_criteris_AE230(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):
        te_menys_de_16_anys = persona('edat', period) < 16
        ingressos_inferiors_varem = persona.familia('familia_ingressos_bruts', period.last_year) <= \
                                    varem_irsc_016(persona.familia.nb_persons())
        es_usuari_serveis_socials = persona.familia('es_usuari_serveis_socials', period)
        es_empadronat_a_barcelona = persona('municipi_empadronament', period) == 'barcelona'
        anys_empadronament_valid = persona('data_alta_padro_valida_AE_230', period)
        existeix_algun_solicitant_AE_230 = persona.familia.any(persona.familia.members('solicitant_AE_230_valid', period))

        return te_menys_de_16_anys \
               * ingressos_inferiors_varem \
               * es_empadronat_a_barcelona \
               * anys_empadronament_valid \
               * es_usuari_serveis_socials \
               * existeix_algun_solicitant_AE_230


class AE_230_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):
        tipus_custodia = persona.familia('tipus_custodia', period)
        import_ajuda = parameters(period).benefits.AE230.import_ajuda[clau_custodia(tipus_custodia)][clau_ordre_del_menor(persona("ordre_del_menor", period))]
        return persona('compleix_criteris_AE230', period) * import_ajuda
