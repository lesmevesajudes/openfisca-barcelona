from openfisca_barcelona.variables.demographics import *


class TipusCustodia(Enum):
    cap = "cap"
    total = "total"
    compartida = "compartida"


class tipus_custodia(Variable):
    value_type = Enum
    possible_values = TipusCustodia
    default_value = TipusCustodia.cap
    entity = Persona
    definition_period = MONTH
    label = "The type of relation child between child and it's maintainers"
    set_input = set_input_dispatch_by_period


class es_escolaritzat_entre_P3_i_4rt_ESO(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The child goes to school"
    set_input = set_input_dispatch_by_period
    default = False


class nivell_de_renda_inferior_a_2416_80(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_bruts', period) < 2416.80


class nivell_de_renda_inferior_a_2900_20(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_bruts', period) < 2900.20


class nivell_de_renda_inferior_a_1450_08(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_bruts', period) < 1450.08


class nivell_de_renda_inferior_a_1740_12(Variable):
    value_type = bool
    entity = Persona
    definition_period = YEAR
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_bruts', period) < 1740.12


class en_acolliment(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "The child is in protection regime"
    set_input = set_input_dispatch_by_period
    default = False


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
            tipus_familia_nombrosa == TipusFamiliaNombrosa.general,
            tipus_familia_nombrosa == TipusFamiliaNombrosa.especial],
            [1.5, 3])
        tipus_familia_monoparental = familia("tipus_familia_monoparental", period)
        puntuacio_familia_monoparental = select([
            tipus_familia_monoparental == TipusFamiliaMonoparental.general,
            tipus_familia_monoparental == TipusFamiliaMonoparental.especial],
            [1.5, 3])
        tipus_risc_exclusio_social = familia("nivell_de_risc_d_exclusio_social", period)
        puntuacio_risc_exclusio_social = select([
            tipus_risc_exclusio_social == NivellDeRiscExclusioSocial.existeix,
            tipus_risc_exclusio_social == NivellDeRiscExclusioSocial.greu],
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


class compleix_criteris_de_nivell_de_renda_per_l_ajut_extraordinari(Variable):
    value_type = bool
    entity = Familia
    definition_period = MONTH
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period

    def formula(familia, period, parameters):
        nivell_renda_primer_adult = familia.primer_adult('ingressos_bruts', period.last_year)
        nivell_renda_segon_adult = familia.segon_adult('ingressos_bruts', period.last_year)

        nivell_renda_maxim_primer_adult = \
            parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim_primer_adult
        nivell_renda_maxim_segon_adult = parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim_segon_adult

        els_adults_satisfant_criteris_de_nivell_de_renda = \
            (nivell_renda_primer_adult < nivell_renda_maxim_primer_adult) \
            * (nivell_renda_segon_adult < nivell_renda_maxim_segon_adult)

        els_altres_adults_compleixen_criteris_de_nivell_de_renda = \
            familia.all(familia.members('nivell_de_renda_inferior_a_1450_08', period.last_year),
                                role=Familia.ALTRE_ADULT)
        els_menors_compleixen_els_criteris_de_nivell_de_renda = \
            familia.all(familia.members('nivell_de_renda_inferior_a_1740_12', period.last_year), role=Familia.MENOR)

        return \
            els_adults_satisfant_criteris_de_nivell_de_renda \
            * els_altres_adults_compleixen_criteris_de_nivell_de_renda\
            * els_menors_compleixen_els_criteris_de_nivell_de_renda


class compleix_criteris_de_nivell_de_renda_per_l_ajut_ordinari(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        nivell_renda_primer_adult = persona.familia.primer_adult('ingressos_bruts', period.last_year)
        nivell_renda_segon_adult = persona.familia.segon_adult('ingressos_bruts', period.last_year)
        print (nivell_renda_segon_adult)
        nivell_renda_maxim_primer_adult = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim_primer_adult
        nivell_renda_maxim_segon_adult = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim_segon_adult

        els_adults_satisfant_criteris_de_nivell_de_renda = (nivell_renda_primer_adult < nivell_renda_maxim_primer_adult) \
                                                           * (nivell_renda_segon_adult < nivell_renda_maxim_segon_adult)

        els_altres_adults_compleixen_criteris_de_nivell_de_renda = persona.familia.all(
            persona.familia.members('nivell_de_renda_inferior_a_2416_80', period.last_year), role=Familia.ALTRE_ADULT)

        els_menors_compleixen_els_criteris_de_nivell_de_renda = \
            persona.familia.all(persona.familia.members('nivell_de_renda_inferior_a_2900_20', period.last_year), role=Familia.MENOR)

        return els_adults_satisfant_criteris_de_nivell_de_renda \
               * els_altres_adults_compleixen_criteris_de_nivell_de_renda \
               * els_menors_compleixen_els_criteris_de_nivell_de_renda


class EG_233_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "EG_233 - AJUTS INDIVIDUALS DE MENJADOR CIUTAT BARCELONA"

    def formula(persona, period, parameters):

        es_escolaritzat_entre_P3_i_4rt_ESO = persona('es_escolaritzat_entre_P3_i_4rt_ESO', period)
        es_un_menor = persona.has_role(Familia.MENOR)
        en_guardia_i_custodia = persona('tipus_custodia', period) != "cap"
        compleix_els_requeriments = en_guardia_i_custodia * \
                                    es_escolaritzat_entre_P3_i_4rt_ESO * \
                                    es_un_menor

        compleix_ajut_ordinari = persona("compleix_criteris_de_nivell_de_renda_per_l_ajut_ordinari", period)

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
            persona.familia("compleix_criteris_de_nivell_de_renda_per_l_ajut_extraordinari", period) \
            * (puntuacio_familiar >= puntuacio_familiar_minima) \
            * (volum_de_negoci < volum_de_negoci_maxim) \
            * (rendiments_patrimonials < rendiments_patrimonials_maxim) \
            * (valor_cadastral_finques_rustiques < valor_cadastral_finques_rustiques_maxim) \
            * (valor_cadastral_finques_urbanes < valor_cadastral_finques_urbanes_maxim)

        import_ajut_extraordinari = parameters(period).benefits.EG233.ajut_extraordinari_import
        import_ajut_ordinari = parameters(period).benefits.EG233.ajut_ordinari_import

        print (compleix_ajut_ordinari)
        import_EG_233 = select([compleix_ajut_extraordinari, compleix_ajut_ordinari],
                               [import_ajut_extraordinari, import_ajut_ordinari])

        return compleix_els_requeriments * import_EG_233
