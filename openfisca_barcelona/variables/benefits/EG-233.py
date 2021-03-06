from openfisca_core.model_api import *
from openfisca_barcelona.entities import *

class es_escolaritzat_entre_P3_i_4rt_ESO(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The child goes to school"
    set_input = set_input_dispatch_by_period
    default_value = False


class ordinari_nivell_renda_altres_familiars_membre_discapacitat_60(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim['altres_familiars']['membre_discapacitat_superior_60']
        return persona('ingressos_bruts', period) <= renda_maxima


class ordinari_nivell_renda_altres_familiars_no_discapacitat(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim['altres_familiars']['altres']
        return persona('ingressos_bruts', period) <= renda_maxima


class ordinari_nivell_renda_menors_membre_discapacitat_60(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim['menors']['membre_discapacitat_superior_60']
        return persona('ingressos_bruts', period) <= renda_maxima


class ordinari_nivell_renda_menors_no_discapacitat(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim['menors']['altres']
        return persona('ingressos_bruts', period) <= renda_maxima

class extraordinari_nivell_renda_altres_familiars_membre_discapacitat_60(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim['altres_familiars']['membre_discapacitat_superior_60']
        return persona('ingressos_bruts', period) <= renda_maxima


class extraordinari_nivell_renda_altres_familiars_no_discapacitat(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim['altres_familiars']['altres']
        return persona('ingressos_bruts', period) <= renda_maxima


class extraordinari_nivell_renda_menors_membre_discapacitat_60(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim['menors']['membre_discapacitat_superior_60']
        return persona('ingressos_bruts', period) <= renda_maxima


class extraordinari_nivell_renda_menors_no_discapacitat(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        renda_maxima = parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim['menors']['altres']
        return persona('ingressos_bruts', period) <= renda_maxima


class nivell_de_renda_inferior_a_1450_08(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_bruts', period) <= 1450.08


class nivell_de_renda_inferior_a_1740_12(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_bruts', period) <= 1740.12


class en_acolliment(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The child is in protection regime"
    set_input = set_input_dispatch_by_period
    default_value = False


class punts_assignats_per_grau_de_discapacitat(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = "Punts assignats a cada membre segons el grau de discapacitat"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        grau_discapacitat = persona("grau_discapacitat", period)
        return select([grau_discapacitat <= 33, grau_discapacitat > 33], [1.5, 3])


class puntuacio_de_la_familia_segons_eg_233(Variable):
    value_type = float
    entity = Familia
    definition_period = MONTH
    label = "Puntuacio que te la familia per a clacular si es susceptible de rebre ajut extraordinari"
    set_input = set_input_dispatch_by_period

    def formula(familia, period, legislation):
        tipus_familia_nombrosa = familia("tipus_familia_nombrosa", period)
        puntuacio_familia_nombrosa = select([
            tipus_familia_nombrosa == tipus_familia_nombrosa.possible_values.general,
            tipus_familia_nombrosa == tipus_familia_nombrosa.possible_values.especial],
            [1.5, 3])
        tipus_familia_monoparental = familia("tipus_familia_monoparental", period)
        puntuacio_familia_monoparental = select([
            tipus_familia_monoparental == tipus_familia_monoparental.possible_values.general,
            tipus_familia_monoparental == tipus_familia_monoparental.possible_values.especial],
            [1.5, 3])
        risc_exclusio_social = familia("nivell_de_risc_d_exclusio_social", period)
        puntuacio_risc_exclusio_social = select([
            risc_exclusio_social == risc_exclusio_social.possible_values.existeix,
            risc_exclusio_social == risc_exclusio_social.possible_values.greu],
            [10, 15])
        punts_per_grau_discapacitat_membres = familia.members("punts_assignats_per_grau_de_discapacitat", period)
        punts_grau_discapacitat = familia.sum(punts_per_grau_discapacitat_membres)

        en_acolliment_membres = familia.members("punts_assignats_per_grau_de_discapacitat", period)
        punts_en_acolliment = familia.sum(en_acolliment_membres) * 3

        return puntuacio_familia_nombrosa + puntuacio_familia_monoparental + puntuacio_risc_exclusio_social + \
               punts_grau_discapacitat + punts_en_acolliment


class volum_del_negoci_familiar(Variable):
    value_type = float
    unit = 'currency'
    entity = Familia
    definition_period = YEAR
    label = "Household total income due family business"
    set_input = set_input_divide_by_period


class rendiments_del_patrimoni(Variable):
    value_type = float
    unit = 'currency'
    entity = Familia
    definition_period = YEAR
    label = "Household total income due properties"
    set_input = set_input_dispatch_by_period


class valor_cadastral_finques_rustiques(Variable):
    value_type = float
    unit = 'currency'
    entity = Familia
    definition_period = YEAR
    label = "Household total valuation of rustic properties"
    set_input = set_input_dispatch_by_period


class valor_cadastral_finques_urbanes(Variable):
    value_type = float
    unit = 'currency'
    entity = Familia
    definition_period = YEAR
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period

class beneficiari_fons_infancia(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "This person was beneficiary of last year's 0-16 benefit"
    set_input = set_input_dispatch_by_period
    default_value = False


def clau_nivell_de_renda(grau_discapacitat):
    return select([grau_discapacitat >= 60, grau_discapacitat < 60],
                  ['membre_discapacitat_superior_60', 'altres'])


class renda_maxima_familia(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        grau_discapacitat = persona('grau_discapacitat', period)
        renda_maxima = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim
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
        compleix_ajut_ordinari = ingressos_familia < persona('renda_maxima_familia', period)

        puntuacio_familiar = persona.familia("puntuacio_de_la_familia_segons_eg_233", period)
        volum_de_negoci = persona.familia("volum_del_negoci_familiar", period.last_year)
        rendiments_patrimonials = persona.familia("rendiments_del_patrimoni", period.last_year)
        valor_cadastral_finques_rustiques = persona.familia("valor_cadastral_finques_rustiques", period.last_year)
        valor_cadastral_finques_urbanes = persona.familia("valor_cadastral_finques_urbanes", period.last_year)

        puntuacio_familiar_minima = parameters(period).benefits.EG233.ajut_extraordinari_puntuacio_minima
        volum_de_negoci_maxim = parameters(period).benefits.EG233.ajut_extraordinari_volum_de_negoci_maxim
        rendiments_patrimonials_maxim = \
            parameters(period).benefits.EG233.ajut_extraordinari_rendiments_patrimonials_maxim
        valor_cadastral_finques_rustiques_maxim = \
            parameters(period).benefits.EG233.ajut_extraordinari_valor_cadastral_finques_rustiques_maxim
        valor_cadastral_finques_urbanes_maxim = \
            parameters(period).benefits.EG233.ajut_extraordinari_valor_cadastral_finques_urbanes_maxim

        compleix_ajut_extraordinari = \
            (ingressos_familia < (persona('renda_maxima_familia', period) * 0.6)) \
            * (puntuacio_familiar >= puntuacio_familiar_minima) \
            * (volum_de_negoci < volum_de_negoci_maxim) \
            * (rendiments_patrimonials <= rendiments_patrimonials_maxim) \
            * (valor_cadastral_finques_rustiques <= valor_cadastral_finques_rustiques_maxim) \
            * (valor_cadastral_finques_urbanes <= valor_cadastral_finques_urbanes_maxim) \
            + persona("beneficiari_fons_infancia", period.this_year)
        import_ajut_extraordinari = parameters(period).benefits.EG233.ajut_extraordinari_import
        import_ajut_ordinari = parameters(period).benefits.EG233.ajut_ordinari_import

        import_EG_233 = select([compleix_ajut_extraordinari, compleix_ajut_ordinari],
                               [import_ajut_extraordinari, import_ajut_ordinari])

        return compleix_els_requeriments * import_EG_233
