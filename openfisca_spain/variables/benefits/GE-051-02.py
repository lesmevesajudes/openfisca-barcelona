from openfisca_core.model_api import *
from openfisca_spain.entities import *


class major_de_45_anys(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is older than 45 years"
    set_input = set_input_dispatch_by_period


class desocupat(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has no job"
    set_input = set_input_dispatch_by_period


class ha_treballat_a_l_estranger_6_mesos(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has been working abroad for at least 6 months"
    set_input = set_input_dispatch_by_period


class GE_051_02_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "GE_051_02 - RAI 2 - Per emigrants retornats major de 45 anys"

    def formula(persona, period, legislation):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = persona.familia('cap_familiar_te_renda_disponible_superior_a_530', period)
        major_de_45_anys = persona('major_de_45_anys', period)
        desocupat = persona('desocupat', period)
        ha_treballat_a_l_estranger_6_mesos = persona('ha_treballat_a_l_estranger_6_mesos', period)
        no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos = persona('no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos', period)
        no_se_li_ha_concedit_tres_ajudes_rai_anteiors = persona('no_se_li_ha_concedit_tres_ajudes_rai_anteiors', period)
        no_treballa_per_compte_propi = persona('treballa_per_compte_propi', period) == False
        no_ingressat_en_centre_penitenciari = persona('ingressat_en_centre_penitenciari', period) == False
        no_percep_prestacins_incompatibles_amb_la_feina = persona('percep_prestacions_incompatibles_amb_la_feina', period) == False

        compleix_els_requeriments = \
            cap_membre_amb_ingressos_superiors_a_530_mensuals \
            * major_de_45_anys \
            * desocupat \
            * ha_treballat_a_l_estranger_6_mesos \
            * no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos \
            * no_se_li_ha_concedit_tres_ajudes_rai_anteiors \
            * no_treballa_per_compte_propi \
            * no_ingressat_en_centre_penitenciari \
            * no_percep_prestacins_incompatibles_amb_la_feina

        return where(compleix_els_requeriments, 426, 0)
