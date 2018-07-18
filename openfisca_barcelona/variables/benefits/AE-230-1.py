# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class AE_230_01_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):
        is_adult = persona.has_role(Familia.ADULT)
        tipus_monoparental = persona.familia('tipus_familia_monoparental', period)
        es_monoparental = tipus_monoparental != tipus_monoparental.possible_values.nop
        tipus_custodia = persona.familia('tipus_custodia', period)
        es_monoparental_custodia_total = es_monoparental * (tipus_custodia == tipus_custodia.possible_values.total)
        es_monoparental_custodia_compartida = es_monoparental * (tipus_custodia == tipus_custodia.possible_values.compartida)
        compleix_criteris_AE230 = persona.familia.members('compleix_criteris_AE230', period)
        algun_membre_compleix_criteris_AE230 = persona.familia.any(compleix_criteris_AE230)
        import_ajuda = select([es_monoparental_custodia_total,
                               es_monoparental_custodia_compartida,
                               tipus_monoparental == tipus_monoparental.possible_values.nop],
                               [900, 450, 0])

        return algun_membre_compleix_criteris_AE230 * is_adult * import_ajuda
