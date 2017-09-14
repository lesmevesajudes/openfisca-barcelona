from openfisca_core.model_api import *
from openfisca_spain.entities import *


class ORFEDOSPROJENITORS(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if both parents are dead"


class VICTIMAVIOLENCIAMASCLISTA(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person is a victim of genre violence"


class EMPCAT(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person is registered in Catalonia"


class PERMISRESID(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person has a residence permit"


class PERMISREAGRUPFAMIDIVORCIADA(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person is divorced from a regrouped immigrant family"


class RESEFECTCAT24M(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person has lived efectively in Catalonia for the last 24 months"


class PRESTACIORESIDENCIAL(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person is benefitiary of a residential benefit"


class BAIXAVOL12M(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person is left voluntarily her last job"


class ESDISCAPACITAT(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if person is disabled"

    def formula(person, period, legislation):
        return person("grau_discapacitat", period) > 0

class NRINFIMPRGC(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "True if income is less than IRSC"

    def formula(person, period, legislation):
        return person("ingressos_disponibles", period) < 530 #Fixme: Stub, as I can not understand documentation


class GG_270_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "RENDA GARANTIDA CIUTADANA"

    def formula(person, period, legislation):
        major_23 = person("age", period) >= 23
        major_18 = person("age", period) >= 18
        discapacitats_a_carrec = person.household.any(person("ESDISCAPACITAT", period))
        es_orfe_de_progenitors = person("ORFEDOSPROJENITORS", period)
        es_victima_violencia_masclista = person("VICTIMAVIOLENCIAMASCLISTA", period)
        es_empadronat_a_catalunya = person("EMPCAT", period)
        te_permis_de_residencia = person("PERMISRESID", period)
        es_divorciada_de_familia_reagrupada = person("PERMISREAGRUPFAMIDIVORCIADA", period)
        ha_residit_efectivament_a_cat_durant_24m = person("RESEFECTCAT24M", period)
        compleix_nivell_ingressos = person("NRINFIMPRGC", period)
        te_prestacio_servei_residencial = person("PRESTACIORESIDENCIAL", period)
        es_intern_penitenciari = person("INGCPENITENCIARI", period)
        va_fer_baixa_voluntaria_ultima_feina = person("BAIXAVOL12M", period)

        return ((major_23
                 + (major_18
                    * discapacitats_a_carrec
                    * es_orfe_de_progenitors
                    * es_victima_violencia_masclista))
                * ((es_empadronat_a_catalunya
                    * te_permis_de_residencia)
                + es_divorciada_de_familia_reagrupada)
                * ha_residit_efectivament_a_cat_durant_24m
                * compleix_nivell_ingressos
                * (te_prestacio_servei_residencial == False)
                * (es_intern_penitenciari == False)
                * (va_fer_baixa_voluntaria_ultima_feina == False)) \
                * 100  # Fixme: Stub
