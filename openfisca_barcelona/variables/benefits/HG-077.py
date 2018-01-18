# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from datetime import datetime
from openfisca_barcelona.variables.demographics import *


class resident_a_catalunya_durant_5_anys(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has legal residence in catalonia for at least 5 years"
    set_input = set_input_dispatch_by_period
    default = False


class victima_de_terrorisme(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is a victim of terrorism"
    set_input = set_input_dispatch_by_period
    default = False


class risc_d_exclusio_social(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is in risk of social exclusion"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona.familia("nivell_de_risc_d_exclusio_social", period) != NIVELL_DE_RISC_D_EXCLUSIO_SOCIAL["No"]


class existeix_un_contracte_de_lloguer(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has a rent contract"
    set_input = set_input_dispatch_by_period
    default = False


class LLOGMAXBCN(Variable):  # Fixme: This should be in parameters
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The house hold rent does not exceed maximum rent amount for Barcelona"
    set_input = set_input_dispatch_by_period
    default = False


class esta_al_corrent_del_pagament_de_lloguer(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The rent payments must be up to date"
    set_input = set_input_dispatch_by_period
    default = False


class lloguer_domiciliat(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The rent payments are made through a bank"
    set_input = set_input_dispatch_by_period
    default = False


class pot_rebre_subvencions(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is not subject to any condition that is forbidden"
    set_input = set_input_dispatch_by_period
    default = False


class al_corrent_de_les_obligacions_tributaries(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period
    default = False


class es_BLJ(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has more than 65 years at 31/12/2012"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return major_de_65_el_2012_12_31(persona('data_naixement', period))


class titular_contracte_de_lloguer(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is the one who appears in rent contract"
    set_input = set_input_dispatch_by_period


class relacio_de_parentiu_amb_el_propietari(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "There is some kind of family relation with the owner"
    set_input = set_input_dispatch_by_period


def major_de_65_el_2012_12_31(data_de_naixement):
    return data_de_naixement < datetime.strptime('1948-1-1', "%Y-%m-%d").date()


class import_del_lloguer(Variable):
    column = FloatCol
    entity = Familia
    definition_period = MONTH
    label = "Rent amount payed every month"
    set_input = set_input_dispatch_by_period


class ha_residit_a_lextranger_els_ultims_24_mesos(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living abroad for the last 24 months"
    set_input = set_input_dispatch_by_period
    default = False

class ha_residit_a_catalunya_els_ultims_24_mesos(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living in Catalonia for the last 24 months"
    set_input = set_input_dispatch_by_period
    default = False

class ha_residit_a_lextranger_36_mesos_continuats(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living abroad for at least 36 months"
    set_input = set_input_dispatch_by_period
    default = False

class ha_residit_a_lextranger_60_mesos_discontinuats(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living abroad for at least 60 months"
    set_input = set_input_dispatch_by_period
    default = False



