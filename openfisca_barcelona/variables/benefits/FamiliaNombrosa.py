from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class es_menor_de_25(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH

    def formula(person, period, parameters):
        return (person('edat', period) < 25) * person.has_role(Familia.ALTRES_FAMILIARS)


class es_familia_nombrosa(Variable):
    value_type = bool
    entity = Familia
    definition_period = MONTH
    label = "Familia nombrosa is a benefit for families with more than 3 child under 25 or more than 2 in case there is a disabled person in the family"

    def formula(familia, period, parameters):
        nb_menors = familia.nb_persons(Familia.MENOR)
        nb_altres_familiars_menors_25 = familia.sum(familia.members('es_menor_de_25', period))
        nb_menors_de_25 = nb_menors + nb_altres_familiars_menors_25
        discapacitats = familia.members("grau_discapacitat", period)
        existeix_algun_discapacitat = familia.any(discapacitats)
        return (existeix_algun_discapacitat * (nb_menors_de_25 >= 2)) + (nb_menors_de_25 >= 3)