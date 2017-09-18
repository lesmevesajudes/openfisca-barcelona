from openfisca_core.model_api import *
from openfisca_spain.entities import *


class victima_violencia_de_genere(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is a victim of genre violence"
    set_input = set_input_dispatch_by_period


class GE_051_03_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "RAI 3 - Per victimes de violencia de genere o domestica"

    def formula(persona, period, parameters):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = \
            persona.familia('cap_familiar_te_renda_disponible_superior_a_530', period)
        victima_violencia_de_genere = persona('victima_violencia_de_genere', period)
        desocupat = persona('desocupat', period)
        no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos = \
            persona('no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos', period)
        no_se_li_ha_concedit_tres_ajudes_rai_anteriors = \
            persona('no_se_li_ha_concedit_tres_ajudes_rai_anteriors', period)
        no_treballa_per_compte_propi = persona('treballa_per_compte_propi', period) == False
        no_ingressat_en_centre_penitenciari = persona('ingressat_en_centre_penitenciari', period) == False
        no_percep_prestacins_incompatibles_amb_la_feina = \
            persona('percep_prestacions_incompatibles_amb_la_feina', period) == False
        beneficiari_ajuts_per_violencia_de_genere = \
            persona('beneficiari_ajuts_per_violencia_de_genere', period) == False

        compleix_els_requeriments = \
            cap_membre_amb_ingressos_superiors_a_530_mensuals \
            * victima_violencia_de_genere \
            * desocupat \
            * no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos \
            * no_se_li_ha_concedit_tres_ajudes_rai_anteriors \
            * no_treballa_per_compte_propi \
            * no_ingressat_en_centre_penitenciari \
            * no_percep_prestacins_incompatibles_amb_la_feina \
            * beneficiari_ajuts_per_violencia_de_genere

        import_ajuda = parameters(period).benefits.GE051.import_ajuda
        return where(compleix_els_requeriments, import_ajuda, 0)
