from openfisca_core.model_api import *
from openfisca_spain.entities import *


class es_orfe_dels_dos_progenitors(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if both adults are dead"
    default = False


class es_victima_de_violencia_masclista(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person is a victim of male violence"
    default = False


class es_empadronat_a_catalunya(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person is registered in Catalonia"
    default = False


class te_permis_de_residencia(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person has a residence permit"
    default = False


class es_divorciada_de_familia_reagrupada(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person is divorced from a regrouped immigrant family"
    default = False


class ha_residit_a_catalunya_durant_24_mesos(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person has lived efectively in Catalonia for the last 24 months"
    default = False


class es_beneficiari_d_una_prestacio_residencial(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person is benefitiary of a residential benefit"
    default = False


class en_els_ultims_12_mesos_ha_fet_baixa_voluntaria_de_la_feina(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person has left voluntarily her last job"
    default = False


class es_discapacitat(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if person is disabled"

    def formula(persona, period, legislation):
        return persona("grau_discapacitat", period) > 0

class nivell_de_renda_inferior_rgc(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "True if income is less than IRSC"

    def formula(persona, period, legislation):
        return persona("ingressos_disponibles", period) < 530 #Fixme: Stub, as I can not understand documentation


class GG_270_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "RENDA GARANTIDA CIUTADANA"

    def formula(persona, period, legislation):
        major_23 = persona("edat", period) >= 23
        major_18 = persona("edat", period) >= 18
        discapacitats_a_carrec = persona.familia.any(persona("es_discapacitat", period))
        es_orfe_de_progenitors = persona("es_orfe_dels_dos_progenitors", period)
        es_victima_violencia_masclista = persona("es_victima_de_violencia_masclista", period)
        es_empadronat_a_catalunya = persona("es_empadronat_a_catalunya", period)
        te_permis_de_residencia = persona("te_permis_de_residencia", period)
        es_divorciada_de_familia_reagrupada = persona("es_divorciada_de_familia_reagrupada", period)
        ha_residit_efectivament_a_cat_durant_24m = persona("ha_residit_a_catalunya_durant_24_mesos", period)
        compleix_nivell_ingressos = persona("nivell_de_renda_inferior_rgc", period)
        te_prestacio_servei_residencial = persona("es_beneficiari_d_una_prestacio_residencial", period)
        es_intern_penitenciari = persona("ingressat_en_centre_penitenciari", period)
        va_fer_baixa_voluntaria_ultima_feina = \
            persona("en_els_ultims_12_mesos_ha_fet_baixa_voluntaria_de_la_feina", period)

        return \
            (
                (major_23
                 + (major_18
                    * discapacitats_a_carrec
                    * es_orfe_de_progenitors
                    * es_victima_violencia_masclista
                    )
                 )
                * (
                    (es_empadronat_a_catalunya
                    * te_permis_de_residencia
                     )
                    + es_divorciada_de_familia_reagrupada
                )
                * ha_residit_efectivament_a_cat_durant_24m
                * compleix_nivell_ingressos
                * (te_prestacio_servei_residencial == False)
                * (es_intern_penitenciari == False)
                * (va_fer_baixa_voluntaria_ultima_feina == False)
            ) * 100  # Fixme: Stub
