# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_spain.entities import *

class grau_discapacitat(Variable):
    column = IntCol
    entity = Person
    definition_period = MONTH
    label = "Person grade of disability"
    set_input = set_input_dispatch_by_period


class ha_esgotat_prestacio_de_desocupatacio(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is not receiving any benefit for not having a job"
    set_input = set_input_dispatch_by_period


class demandant_d_ocupacio_durant_12_mesos(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user has been searching for a job at least 12 months"
    set_input = set_input_dispatch_by_period


class durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "During the previous month the user has applied for a job"
    set_input = set_input_dispatch_by_period


class beneficiari_ajuts_per_violencia_de_genere(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user has a violence of genre  benefit"
    set_input = set_input_dispatch_by_period


class GE_051_01_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "GE_051_1 - RAI 1 - Ajuda discapacitats 33% o superior"

    def formula(person, period, legislation):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = \
            person.household('cap_familiar_te_renda_disponible_superior_a_530', period)
        discapacitat_superior_al_33_percent = person('grau_discapacitat', period) > 33
        ha_esgotat_prestacio_de_desocupatacio = person('ha_esgotat_prestacio_de_desocupatacio', period)
        demandant_d_ocupacio_durant_12_mesos = person('demandant_d_ocupacio_durant_12_mesos', period)
        durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina = \
            person('durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina', period)
        no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos = \
            person('no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos', period)
        no_se_li_ha_concedit_tres_ajudes_rai_anteiors = person('no_se_li_ha_concedit_tres_ajudes_rai_anteiors', period)
        no_treballa_per_compte_propi = person('treballa_per_compte_propi', period) == False
        no_ingressat_en_centre_penitenciari = person('ingressat_en_centre_penitenciari', period) == False
        no_percep_prestacins_incompatibles_amb_la_feina = \
            person('percep_prestacins_incompatibles_amb_la_feina', period) == False
        no_beneficiari_ajuts_per_violencia_de_genere = \
            person('beneficiari_ajuts_per_violencia_de_genere', period) == False

        compleix_els_requeriments = \
            cap_membre_amb_ingressos_superiors_a_530_mensuals \
            * discapacitat_superior_al_33_percent \
            * ha_esgotat_prestacio_de_desocupatacio \
            * demandant_d_ocupacio_durant_12_mesos \
            * durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina \
            * no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos \
            * no_se_li_ha_concedit_tres_ajudes_rai_anteiors \
            * no_treballa_per_compte_propi \
            * no_ingressat_en_centre_penitenciari \
            * no_percep_prestacins_incompatibles_amb_la_feina \
            * no_beneficiari_ajuts_per_violencia_de_genere

        return where(compleix_els_requeriments, 426, 0)
