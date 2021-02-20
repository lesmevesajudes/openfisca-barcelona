from numpy.ma import logical_not
from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class renda_mensual_disponible_inferior_a_75_percent_SMI(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Available income is under 75 percent of IMS"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        llindar_ingressos = parameters(period).benefits.GE051.llindars_ingressos
        return persona('ingressos_bruts', period.last_year)/12 <= llindar_ingressos


class cap_familiar_te_renda_disponible_superior_a_75_percent_SMI(Variable):
    value_type = bool
    entity = Familia
    definition_period = MONTH
    label = "No one is making more than 75 percent of IMS"
    set_input = set_input_dispatch_by_period

    def formula(familia, period, legislation):
        members_renda_disponible_inferior_a_75_percent_SMI = familia.members('renda_mensual_disponible_inferior_a_75_percent_SMI', period)
        return familia.all(members_renda_disponible_inferior_a_75_percent_SMI)

class ha_estat_beneficiari_de_la_rai_en_els_ultims_12_mesos(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has been benefited with a rai in the last 12 months"
    set_input = set_input_dispatch_by_period
    default_value = False


class ha_estat_beneficiari_de_les_tres_rai_anteriors(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has a violence of genre  benefit"
    set_input = set_input_dispatch_by_period
    default_value = False


class treballa_per_compte_propi(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user is self-employed"
    set_input = set_input_dispatch_by_period
    default_value = False


class ingressat_en_centre_penitenciari(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user is in prison"
    set_input = set_input_dispatch_by_period
    default_value = False


class ha_treballat_a_l_estranger_6_mesos(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has worked abroad for 6 months"
    set_input = set_input_dispatch_by_period
    default_value = False


class ingressat_en_centre_penitenciari_pot_treballar(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user is in prison but can work"
    set_input = set_input_dispatch_by_period
    default_value = False


class victima_violencia_domestica(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The user has some benefit incompatible with having a job"
    set_input = set_input_dispatch_by_period
    default_value = False

class GE_051_mensual(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "GE_051_1 - RAI 1 - Ajuda discapacitats 33% o superior"

    def formula(persona, period, parameters):
        cap_membre_amb_ingressos_superiors_a_75_percent_SMI = \
            persona.familia('cap_familiar_te_renda_disponible_superior_a_75_percent_SMI', period)
        situacio_laboral = persona('situacio_laboral', period)
        aturat = situacio_laboral == situacio_laboral.possible_values.aturat
        no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos = \
            (persona('ha_estat_beneficiari_de_la_rai_en_els_ultims_12_mesos', period)) == False
        no_se_li_ha_concedit_tres_ajudes_rai_anteriors = \
            (persona('ha_estat_beneficiari_de_les_tres_rai_anteriors', period)) == False
        no_treballa_per_compte_propi = persona('treballa_per_compte_propi', period) == False
        no_ingressat_en_centre_penitenciari = persona('ingressat_en_centre_penitenciari', period) == False
        no_percep_prestacions_incompatibles_amb_la_feina = \
            persona('percep_prestacions_incompatibles_amb_la_feina', period) == False
        menor_de_65_anys = persona('edat', period) < 65

        return \
            cap_membre_amb_ingressos_superiors_a_75_percent_SMI \
            * aturat \
            * menor_de_65_anys \
            * no_treballa_per_compte_propi \
            * no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos \
            * no_se_li_ha_concedit_tres_ajudes_rai_anteriors \
            * no_ingressat_en_centre_penitenciari \
            * no_percep_prestacions_incompatibles_amb_la_feina
