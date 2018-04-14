# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.demographics import TipusFamiliaMonoparental


class AE_230_01_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):
        es_monoparental = (persona.familia('tipus_familia_monoparental', period)[0] == TipusFamiliaMonoparental.general) \
                          + (persona.familia('tipus_familia_monoparental', period)[0] == TipusFamiliaMonoparental.especial)
        es_monoparental_custodia_total = es_monoparental * (persona('tipus_custodia', period) == 'total')
        es_monoparental_custodia_compartida = es_monoparental * (persona('tipus_custodia', period) == 'compartida')
        import_ajuda = select([es_monoparental_custodia_total,
                               es_monoparental_custodia_compartida,
                                persona.familia('tipus_familia_monoparental', period)[0] == TipusFamiliaMonoparental.no],
                               [900, 450, 0])

        return persona('compleix_criteris_AE230', period) * import_ajuda
