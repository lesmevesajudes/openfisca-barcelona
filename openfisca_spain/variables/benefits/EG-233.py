from openfisca_spain.variables.demographics import *

class en_guardia_i_custodia(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is responsible for the child"
    set_input = set_input_dispatch_by_period
    default = False


class es_escolaritzat(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The child goes to school"
    set_input = set_input_dispatch_by_period
    default = False


class utilitza_el_servei_de_menjador(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The child uses school's lunch service"
    set_input = set_input_dispatch_by_period
    default = False


class te_beca_menjador(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The child has free lunch benefit"
    set_input = set_input_dispatch_by_period
    default = False


class nivell_de_renda_inferior_a_2416_80(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_disponibles', period) * 12 < 2416.80   #FIXME: I should not be * define a concept for
                                                                    # yearly total income


class nivell_de_renda_inferior_a_2900_20(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_disponibles', period) * 12 < 2900.20


class nivell_de_renda_inferior_a_1450_08(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_disponibles', period) * 12 < 1450.08


class nivell_de_renda_inferior_a_1740_12(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona('ingressos_disponibles', period) * 12 < 1740.12


class en_acolliment(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The child is in protection regime"
    set_input = set_input_dispatch_by_period
    default = False


class punts_assignats_per_grau_de_discapacitat(Variable):
    column = FloatCol
    entity = Persona
    definition_period = MONTH
    label = "Punts assignats a cada membre segons el grau de discapacitat"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        grau_discapacitat = persona("grau_discapacitat", period)
        return select([grau_discapacitat <= 33, grau_discapacitat > 33], [1.5, 3])


class puntuacio_de_la_familia_segons_eg_233(Variable):
    column = FloatCol
    entity = Familia
    definition_period = MONTH
    label = "Puntuacio que te la familia per a clacular si es susceptible de rebre ajut extraordinari"
    set_input = set_input_dispatch_by_period

    def formula(familia, period, legislation):
        tipus_familia_nombrosa = familia("tipus_familia_nombrosa", period)
        puntuacio_familia_nombrosa = select([
            tipus_familia_nombrosa == TIPUS_FAMILIA_NOMBROSA['General'],
            tipus_familia_nombrosa == TIPUS_FAMILIA_NOMBROSA['Especial']],
            [1.5, 3])
        tipus_familia_monoparental = familia("tipus_familia_monoparental", period)
        puntuacio_familia_monoparental = select([
            tipus_familia_monoparental == TIPUS_FAMILIA_MONOPARENTAL['General'],
            tipus_familia_monoparental == TIPUS_FAMILIA_MONOPARENTAL['Especial']],
            [1.5, 3])
        tipus_risc_exclusio_social = familia("nivell_de_risc_d_exclusio_social", period)
        puntuacio_risc_exclusio_social = select([
            tipus_risc_exclusio_social == NIVELL_DE_RISC_D_EXCLUSIO_SOCIAL["Existeix"],
            tipus_risc_exclusio_social == NIVELL_DE_RISC_D_EXCLUSIO_SOCIAL["Greu"]],
            [10, 15])
        punts_per_grau_discapacitat_membres = familia.members("punts_assignats_per_grau_de_discapacitat", period)
        punts_grau_discapacitat = familia.sum(punts_per_grau_discapacitat_membres)

        en_acolliment_membres = familia.members("punts_assignats_per_grau_de_discapacitat", period)
        punts_en_acolliment = familia.sum(en_acolliment_membres) * 3

        return puntuacio_familia_nombrosa + puntuacio_familia_monoparental + puntuacio_risc_exclusio_social + \
               punts_grau_discapacitat + punts_en_acolliment


class volum_del_negoci_familiar(Variable):
    column = IntCol(val_type="monetary")
    entity = Familia
    definition_period = YEAR
    label = "Household total income due family business"
    set_input = set_input_divide_by_period


class rendiments_del_patrimoni(Variable):
    column = IntCol(val_type="monetary")
    entity = Familia
    definition_period = YEAR
    label = "Household total income due properties"
    set_input = set_input_dispatch_by_period


class valor_cadastral_finques_rustiques(Variable):
    column = IntCol(val_type="monetary")
    entity = Familia
    definition_period = YEAR
    label = "Household total valuation of rustic properties"
    set_input = set_input_dispatch_by_period


class valor_cadastral_finques_urbanes(Variable):
    column = IntCol(val_type="monetary")
    entity = Familia
    definition_period = YEAR
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period


def compleix_criteris_de_nivell_de_renda_per_l_ajut_extraordinari(persona, period, parameters):
    nivell_renda_primer_adult = persona.familia.primer_adult('ingressos_disponibles', period) * 12
    nivell_renda_segon_adult = persona.familia.segon_adult('ingressos_disponibles', period) * 12

    nivell_renda_maxim_primer_adult = \
        parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim_primer_adult
    nivell_renda_maxim_segon_adult = parameters(period).benefits.EG233.ajut_extraordinari_nivell_renda_maxim_segon_adult

    els_adults_satisfant_criteris_de_nivell_de_renda = \
        (nivell_renda_primer_adult < nivell_renda_maxim_primer_adult) \
        * (nivell_renda_segon_adult < nivell_renda_maxim_segon_adult)

    els_altres_adults_compleixen_criteris_de_nivell_de_renda = \
        persona.familia.all(persona.familia.members('nivell_de_renda_inferior_a_1450_08', period),
                            role=Familia.ALTRE_ADULT)

    els_menors_compleixen_els_criteris_de_nivell_de_renda = \
        persona.familia.all(persona.familia.members('nivell_de_renda_inferior_a_1740_12', period), role=Familia.MENOR)


    return \
        els_adults_satisfant_criteris_de_nivell_de_renda \
        * els_altres_adults_compleixen_criteris_de_nivell_de_renda\
        * els_menors_compleixen_els_criteris_de_nivell_de_renda


def compleix_criteris_de_nivell_de_renda_per_l_ajut_ordinari(persona, period, parameters):
    nivell_renda_primer_adult = persona.familia.primer_adult('ingressos_disponibles', period) * 12
    nivell_renda_segon_adult = persona.familia.segon_adult('ingressos_disponibles', period) * 12

    nivell_renda_maxim_primer_adult = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim_primer_adult
    nivell_renda_maxim_segon_adult = parameters(period).benefits.EG233.ajut_ordinari_nivell_renda_maxim_segon_adult

    els_adults_satisfant_criteris_de_nivell_de_renda = (nivell_renda_primer_adult < nivell_renda_maxim_primer_adult) \
                                                       * (nivell_renda_segon_adult < nivell_renda_maxim_segon_adult)

    els_altres_adults_compleixen_criteris_de_nivell_de_renda = persona.familia.all(
        persona.familia.members('nivell_de_renda_inferior_a_2416_80', period), role=Familia.ALTRE_ADULT)

    els_menors_compleixen_els_criteris_de_nivell_de_renda = \
        persona.familia.all(persona.familia.members('nivell_de_renda_inferior_a_2900_20', period), role=Familia.MENOR)

    return els_adults_satisfant_criteris_de_nivell_de_renda \
           * els_altres_adults_compleixen_criteris_de_nivell_de_renda \
           * els_menors_compleixen_els_criteris_de_nivell_de_renda


class EG_233_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "EG_233 - AJUTS INDIVIDUALS DE MENJADOR CIUTAT BARCELONA"

    def formula(persona, period, parameters):

        es_escolaritzat = persona('es_escolaritzat', period)
        utilitza_el_servei_de_menjador = persona('utilitza_el_servei_de_menjador', period)
        no_te_beca_menjador = persona('te_beca_menjador', period) == False
        es_un_menor = persona.has_role(Familia.MENOR)
        en_guardia_i_custodia = persona('en_guardia_i_custodia', period)   # Fixme: Need to understand the
                                                                                    # semantics of this concept.
                                                                                    # Somebody is in "guardia i
                                                                                    # custodia" somebody has "guardia y
                                                                                    # custodia" over somebody else...
        compleix_els_requeriments = en_guardia_i_custodia * \
                                    es_escolaritzat * \
                                    utilitza_el_servei_de_menjador * \
                                    no_te_beca_menjador * \
                                    es_un_menor

        compleix_ajut_ordinari = compleix_criteris_de_nivell_de_renda_per_l_ajut_ordinari(persona, period, parameters)

        puntuacio_familiar = persona.familia("puntuacio_de_la_familia_segons_eg_233", period)
        volum_de_negoci = persona.familia("volum_del_negoci_familiar", period.last_year)
        rendiments_patrimonials = persona.familia("rendiments_del_patrimoni", period.last_year)
        valor_cadastral_finques_rustiques = persona.familia("valor_cadastral_finques_rustiques", period.this_year)
        valor_cadastral_finques_urbanes = persona.familia("valor_cadastral_finques_urbanes", period.this_year)

        puntuacio_familiar_minima = parameters(period).benefits.EG233.ajut_extraordinari_puntuacio_minima
        volum_de_negoci_maxim = parameters(period).benefits.EG233.ajut_extraordinari_volum_de_negoci_maxim
        rendiments_patrimonials_maxim = \
            parameters(period).benefits.EG233.ajut_extraordinari_rendiments_patrimonials_maxim
        valor_cadastral_finques_rustiques_maxim = \
            parameters(period).benefits.EG233.ajut_extraordinari_valor_cadastral_finques_rustiques_maxim
        valor_cadastral_finques_urbanes_maxim = \
            parameters(period).benefits.EG233.ajut_extraordinari_valor_cadastral_finques_urbanes_maxim

        compleix_ajut_extraordinari = \
            compleix_criteris_de_nivell_de_renda_per_l_ajut_extraordinari(persona, period, parameters) \
            * (puntuacio_familiar >= puntuacio_familiar_minima) \
            * (volum_de_negoci < volum_de_negoci_maxim) \
            * (rendiments_patrimonials < rendiments_patrimonials_maxim) \
            * (valor_cadastral_finques_rustiques < valor_cadastral_finques_rustiques_maxim) \
            * (valor_cadastral_finques_urbanes < valor_cadastral_finques_urbanes_maxim)

        import_ajut_extraordinari = parameters(period).benefits.EG233.ajut_extraordinari_import
        import_ajut_ordinari = parameters(period).benefits.EG233.ajut_ordinari_import

        import_EG_233 = select([compleix_ajut_extraordinari, compleix_ajut_ordinari],
                               [import_ajut_extraordinari, import_ajut_ordinari])

        return compleix_els_requeriments * import_EG_233
