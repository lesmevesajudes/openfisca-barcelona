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
        tipus_monoparental = persona.familia('tipus_familia_monoparental', period)
        es_monoparental = tipus_monoparental != tipus_monoparental.possible_values.nop
        tipus_custodia = persona('tipus_custodia', period)
        es_monoparental_custodia_total = es_monoparental * (tipus_custodia == tipus_custodia.possible_values.total)
        es_monoparental_custodia_compartida = es_monoparental * (tipus_custodia == tipus_custodia.possible_values.compartida)

        import_ajuda = select([es_monoparental_custodia_total,
                               es_monoparental_custodia_compartida,
                               tipus_monoparental == tipus_monoparental.possible_values.nop],
                               [900, 450, 0])

        return persona('compleix_criteris_AE230', period) * import_ajuda
