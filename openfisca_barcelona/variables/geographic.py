from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *
import numpy as np


class codi_postal(Variable):
    column = StrCol
    entity = Persona
    definition_period = MONTH
    label = u"Postal code where person lives"
    set_input = set_input_dispatch_by_period