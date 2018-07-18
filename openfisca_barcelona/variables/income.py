# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *


class ingressos_bruts(Variable):
    value_type = float
    entity = Persona
    definition_period = YEAR
    label = "Total amount earned in a year"
    set_input = set_input_divide_by_period


class ingressos_bruts_ultims_sis_mesos(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = "income in the last six months"
    default_value = False

class ingressos_per_pnc(Variable):
    value_type = float
    entity = Persona
    definition_period = YEAR
    label = "Total amount earned in a year by pnc"
    set_input = set_input_divide_by_period


class familia_ingressos_bruts(Variable):
    value_type = float
    unit = 'currency'
    entity = Familia
    definition_period = YEAR
    label = "Total yearly income"
    set_input = set_input_divide_by_period

    def formula(familia, period):
        ingressos_membres_de_la_familia = familia.members('ingressos_bruts', period, options=[DIVIDE])
        total_ingressos_familia = familia.sum(ingressos_membres_de_la_familia)
        return total_ingressos_familia
