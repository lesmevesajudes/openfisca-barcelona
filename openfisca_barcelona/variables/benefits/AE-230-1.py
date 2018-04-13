# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.demographics import TIPUS_FAMILIA_MONOPARENTAL


class AE_230_01_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):
        es_monoparental = (persona.familia('tipus_familia_monoparental', period)[0] == TIPUS_FAMILIA_MONOPARENTAL['General']) \
                          + (persona.familia('tipus_familia_monoparental', period)[0] == TIPUS_FAMILIA_MONOPARENTAL['Especial'])
        es_monoparental_custodia_total = es_monoparental * (persona('tipus_custodia', period) == 'total')
        es_monoparental_custodia_compartida = es_monoparental * (persona('tipus_custodia', period) == 'compartida')
        import_ajuda = select([es_monoparental_custodia_total,
                               es_monoparental_custodia_compartida,
                                persona.familia('tipus_familia_monoparental', period)[0] == TIPUS_FAMILIA_MONOPARENTAL['No']],
                               [900, 450, 0])

        return persona('compleix_criteris_AE230', period) * import_ajuda
