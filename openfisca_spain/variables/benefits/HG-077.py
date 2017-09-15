# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from datetime import datetime
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_spain.entities import *


class resident_a_catalunya_durant_5_anys(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has legal residence in catalonia for at least 5 years"
    set_input = set_input_dispatch_by_period


class victima_de_terrorisme(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is a victim of terrorism"
    set_input = set_input_dispatch_by_period


class ingressos_suficients_per_pagar_el_lloguer(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The familia income is enough to pay rent"
    set_input = set_input_dispatch_by_period


class risc_d_exclusio_social(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is in risk of social exclusion"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona("nivell_de_risc_d_exclusio_social", period) != nivell_de_risc_d_exclusio_social_categories["No"]


class existeix_un_contracte_de_lloguer(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has a rent contract"
    set_input = set_input_dispatch_by_period


class LLOGMAXBCN(Variable):     # Fixme: This should be in parameters
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The house hold rent does not exceed maximum rent amount for Barcelona"
    set_input = set_input_dispatch_by_period


class esta_al_corrent_del_pagament_de_lloguer(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The rent payments must be up to date"
    set_input = set_input_dispatch_by_period


class lloguer_domiciliat(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The rent payments are made through a bank"
    set_input = set_input_dispatch_by_period


class pot_rebre_subvencions(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is not subject to any condition that is forbidden"
    set_input = set_input_dispatch_by_period


class al_corrent_de_les_obligacions_tributaries(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class ESBLJ(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has more than 65 years at 31/12/2012"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return major_de_65_el_2012_12_31(persona('data_naixement',period))


def major_de_65_el_2012_12_31(data_de_naixement):
    return data_de_naixement < datetime.strptime('1948-1-1', "%Y-%m-%d").date()


class import_del_lloguer(Variable):
    column = FloatCol
    entity = Familia
    definition_period = MONTH
    label = "Rent amount payed every month"
    set_input = set_input_dispatch_by_period


class HG_077_mensual(Variable):
    column = FloatCol
    entity = Persona   ## TODO Cambiar a familia
    definition_period = MONTH
    label = "AJUT PER AL PAGAMENT DEL LLOGUER"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        compleix_els_requeriments = \
            ((persona.familia('ingressos_suficients_per_pagar_el_lloguer', period)
              + persona('victima_de_terrorisme', period)) > 0) \
            * persona.familia('LLOGMAXBCN', period) \
            * persona.familia('esta_al_corrent_del_pagament_de_lloguer', period) \
            * persona.familia('lloguer_domiciliat',period) \
            * persona('resident_a_catalunya_durant_5_anys', period) \
            * persona('risc_d_exclusio_social', period) \
            * persona('existeix_un_contracte_de_lloguer', period) \
            * persona('pot_rebre_subvencions', period) \
            * persona('al_corrent_de_les_obligacions_tributaries', period)
        irsc_per_0_94 = 569.12 * 0.94
        lloguer_just = where(persona('ingressos_disponibles', period)/12 > irsc_per_0_94,
                             persona('ingressos_disponibles', period)/12 * 0.3,
                             persona('ingressos_disponibles', period)/12 * 0.2)
        import_ajuda_BLJ = max_(min_(persona.familia('import_del_lloguer', period) - lloguer_just, 2880/12), 0)
        import_ajuda_no_BLJ = max_(min_(persona.familia('import_del_lloguer', period) - lloguer_just, 200), 20)
        BLJStatus = persona.familia.members('ESBLJ', period)
        existeixAlgunBLJ = persona.familia.any(BLJStatus)
        import_ajuda = where(existeixAlgunBLJ, import_ajuda_BLJ, import_ajuda_no_BLJ)
        return where(compleix_els_requeriments, import_ajuda, 0)
