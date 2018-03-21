# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a familia).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from datetime import datetime
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.demographics import TIPUS_FAMILIA_MONOPARENTAL

class AE_230_01_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):

        import_ajuda = select([persona.familia('tipus_familia_monoparental', period)[0] == TIPUS_FAMILIA_MONOPARENTAL['General'],
                                persona.familia('tipus_familia_monoparental', period)[0] == TIPUS_FAMILIA_MONOPARENTAL['Especial']],
                               [900, 900])

        return persona('compleix_criteris_AE230', period) * import_ajuda
