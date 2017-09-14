from openfisca_core.model_api import *
from openfisca_spain.entities import *


class victima_violencia_de_genere(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class GE_051_03_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "RAI 3 - Per victimes de violencia de genere o domestica"

    def formula(person, period, legislation):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = \
            person.household('cap_familiar_te_renda_disponible_superior_a_530', period)
        victima_violencia_de_genere = person('victima_violencia_de_genere', period)
        desocupat = person('desocupat', period)
        no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos = \
            person('no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos', period)
        no_se_li_ha_concedit_tres_ajudes_rai_anteiors = \
            person('no_se_li_ha_concedit_tres_ajudes_rai_anteiors', period)
        no_treballa_per_compte_propi = person('treballa_per_compte_propi', period) == False
        no_ingressat_en_centre_penitenciari = person('ingressat_en_centre_penitenciari', period) == False
        no_percep_prestacins_incompatibles_amb_la_feina = \
            person('percep_prestacins_incompatibles_amb_la_feina', period) == False
        beneficiari_ajuts_per_violencia_de_genere = \
            person('beneficiari_ajuts_per_violencia_de_genere', period) == False

        compleix_els_requeriments = \
            cap_membre_amb_ingressos_superiors_a_530_mensuals \
            * victima_violencia_de_genere \
            * desocupat \
            * no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos \
            * no_se_li_ha_concedit_tres_ajudes_rai_anteiors \
            * no_treballa_per_compte_propi \
            * no_ingressat_en_centre_penitenciari \
            * no_percep_prestacins_incompatibles_amb_la_feina \
            * beneficiari_ajuts_per_violencia_de_genere

        return where(compleix_els_requeriments, 426, 0)
