# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a familia).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *
import numpy as np


class edat(Variable):
    value_type = int
    entity = Persona
    definition_period = MONTH
    label = u"Person's age (in years)"

    # A person's age is computed according to its birth date.
    def formula(persona, period, legislation):
        data_naixement = persona('data_naixement', period)
        return (np.datetime64(period.date) - data_naixement).astype('timedelta64[Y]')


# This variable is a pure input: it doesn't have a formula
class data_naixement(Variable):
    value_type = date  # By default, is no value is set for a simulation, we consider the
                                                # people involved in a simulation to be born on the 1st of Jan 1970.
    entity = Persona
    label = u"Birth date"
    definition_period = ETERNITY  # This     variable cannot change over time.


class data_alta_padro(Variable):
    value_type = date
    entity = Persona
    label = u"Inscription to the cityzenship register"
    definition_period = MONTH


class SituacionsLaborals(Enum):
    treball_compte_daltri_jornada_complerta = "treball_compte_daltri_jornada_complerta"
    treball_compte_daltri_jornada_parcial = "treball_compte_daltri_jornada_parcial"
    treball_compte_propi = "treball_compte_propi"
    aturat = "Aturat"
    estudiant = "estudiant"
    jubilat = "jubilat"

class situacio_laboral(Variable):
    value_type = Enum
    possible_values = SituacionsLaborals
    default_value = SituacionsLaborals.aturat
    entity = Persona
    label = u"labor situation"
    definition_period = MONTH


class beneficiari_fons_infancia_2017(Variable):
    value_type = bool
    entity = Persona
    label = u"Has fons_infancia_2017 benefit"
    definition_period = MONTH

class TipusDocumentIdentitat(Enum):
    DNI = "DNI"
    NIE = "NIE"
    passaport = "passaport"
    altres = "altres"
    especial = "especial"


class tipus_document_identitat(Variable):
    value_type = Enum
    possible_values = TipusDocumentIdentitat
    entity = Persona
    label = u"ID document type"
    definition_period = MONTH
    default_value = TipusDocumentIdentitat.altres


class relacio_habitatge(Variable):
    value_type = str
    entity = Familia
    label = u"Family - property relation"
    definition_period = MONTH


class NivellDeRiscExclusioSocial(Enum):
    nop = "no existeix"
    existeix = "existeix"
    greu = "greu"


class nivell_de_risc_d_exclusio_social(Variable):
    value_type = Enum
    possible_values = NivellDeRiscExclusioSocial
    default_value = NivellDeRiscExclusioSocial.nop
    entity = Familia
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Level of social exclusion risk"


class TipusFamiliaNombrosa(Enum):
    nop = "no"
    general = "general"
    especial = "especial"


class tipus_familia_nombrosa(Variable):
    value_type = Enum
    possible_values = TipusFamiliaNombrosa
    default_value = TipusFamiliaNombrosa.nop
    entity = Familia
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Type of large family certification"


class TipusFamiliaMonoparental(Enum):
    __order__ = "nop general especial"
    nop = "no"
    general = "general"
    especial = "especial"


class tipus_familia_monoparental(Variable):
    value_type = Enum
    possible_values = TipusFamiliaMonoparental
    default_value = TipusFamiliaMonoparental.nop
    entity = Familia
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Type of monoparental family certification"


class nacionalitat(Variable):
    value_type = str
    entity = Persona
    definition_period = MONTH
    label = u"Person nationality"


class TipusCustodia(Enum):
    cap = "cap"
    total = "total"
    compartida = "compartida"


class tipus_custodia(Variable):
    value_type = Enum
    possible_values = TipusCustodia
    default_value = TipusCustodia.cap
    entity = Familia
    definition_period = MONTH
    label = "The type of relation child between child and it's maintainers"
    set_input = set_input_dispatch_by_period

class Sexe(Enum):
    home = "home"
    dona = "dona"

class sexe(Variable):
    value_type = Enum
    possible_values = Sexe
    default_value = Sexe.dona
    entity = Persona
    definition_period = MONTH
    label = "Gender"
    set_input = set_input_dispatch_by_period
