from openfisca_core.model_api import *
from openfisca_barcelona.entities import *

def clau_nivell_de_renda(grau_discapacitat):
    return select([grau_discapacitat >= 60, grau_discapacitat < 60],
                  ['membre_discapacitat_superior_60', 'altres'])


class es_escolaritzat_entre_P3_i_4rt_ESO(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The child goes to school"
    set_input = set_input_dispatch_by_period
    default_value = False

class en_acolliment(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The child is in protection regime"
    set_input = set_input_dispatch_by_period
    default_value = False

class renda_maxima_familia_ordinari(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim
        grau_discapacitat = persona('grau_discapacitat', period)
        es_discapacitat = clau_nivell_de_renda(grau_discapacitat)
        per_primer_adult = persona.familia.nb_persons(Familia.PRIMER_ADULT) * renda_maxima['primer_adult']['altres']
        per_segon_adult = persona.familia.nb_persons(Familia.SEGON_ADULT) * renda_maxima['segon_adult']['altres']

        per_altres_adults = persona.familia.nb_persons(Familia.ALTRES_FAMILIARS) \
                            * renda_maxima['altres_familiars']['altres']
        per_menors = persona.familia.nb_persons(Familia.MENOR) * renda_maxima['menors']['altres']
        return per_primer_adult + per_segon_adult + per_altres_adults + per_menors

class renda_maxima_familia_extraordinari(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim
        grau_discapacitat = persona('grau_discapacitat', period)
        es_discapacitat = clau_nivell_de_renda(grau_discapacitat)
        per_primer_adult = persona.familia.nb_persons(Familia.PRIMER_ADULT) * renda_maxima['primer_adult'][es_discapacitat]
        per_segon_adult = persona.familia.nb_persons(Familia.SEGON_ADULT) * renda_maxima['segon_adult'][es_discapacitat]

        per_altres_adults = persona.familia.nb_persons(Familia.ALTRES_FAMILIARS) \
                            * renda_maxima['altres_familiars'][es_discapacitat]
        per_menors = persona.familia.nb_persons(Familia.MENOR) * renda_maxima['menors'][es_discapacitat]
        return per_primer_adult + per_segon_adult + per_altres_adults + per_menors

class EG_233_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "EG_233 - AJUTS INDIVIDUALS DE MENJADOR CIUTAT BARCELONA"

    def formula(persona, period, parameters):

        es_escolaritzat_entre_P3_i_4rt_ESO = persona('es_escolaritzat_entre_P3_i_4rt_ESO', period)
        es_un_menor = persona.has_role(Familia.MENOR)
        tipus_custodia = persona.familia('tipus_custodia', period)
        en_guardia_i_custodia = tipus_custodia != tipus_custodia.possible_values.cap
        compleix_els_requeriments = en_guardia_i_custodia * \
                                    es_escolaritzat_entre_P3_i_4rt_ESO * \
                                    es_un_menor

        ingressos_familia = persona.familia.sum(persona.familia.members('ingressos_bruts', period.last_year)) \
                            - persona.familia.sum(persona.familia.members('ingressos_bruts', period.last_year), Familia.ALTRES_PERSONES)
        compleix_ajut_ordinari = ingressos_familia < persona('renda_maxima_familia_ordinari', period)

        compleix_ajut_extraordinari = \
            (ingressos_familia < persona('renda_maxima_familia_extraordinari', period))
        import_ajut_extraordinari = parameters(period).benefits.EG233.ajut_extraordinari_import
        import_ajut_ordinari = parameters(period).benefits.EG233.ajut_ordinari_import

        import_EG_233 = select([compleix_ajut_extraordinari, compleix_ajut_ordinari],
                               [import_ajut_extraordinari, import_ajut_ordinari])

        return compleix_els_requeriments * import_EG_233
