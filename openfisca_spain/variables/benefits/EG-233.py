from openfisca_core.model_api import *
from openfisca_spain.entities import *


class GUARICUS(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class ESCOLARITZAT(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class MENJADOR(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class BECAMENJADOR(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period


class NR_INF_2416_80(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('ingressos_disponibles', period) * 12 < 2416.80   #FIXME: I should not be * define a concept for
                                                                    # yearly total income


class NR_INF_2900_20(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('ingressos_disponibles', period) * 12 < 2900.20


class NR_INF_1450_08(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('ingressos_disponibles', period) * 12 < 1450.08


class NR_INF_1740_12(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        return person('ingressos_disponibles', period) * 12 < 1740.12


FAMNOMBROSA_CATEGORIA = Enum([
    u'No',
    u'General',
    u'Especial'])


class FAMNOMBROSA(Variable):
    column = EnumCol(
        enum=FAMNOMBROSA_CATEGORIA,
        default=0  # No
    )
    entity = Household
    definition_period = MONTH
    label = u"Tipus de familia nombrosa"


FAMMONOPARENTAL_CATEGORIA = Enum([
    u'No',
    u'General',
    u'Especial'
])


class FAMMONOPARENTAL(Variable):
    column = EnumCol(
        enum=FAMMONOPARENTAL_CATEGORIA,
        default=0  # No
    )
    entity = Household
    definition_period = MONTH
    label = u"Tipus de familia monoparental"


RISCEXCLUSIOSOCIAL_CATEGORIA = Enum([
    u'No',
    u'Existeix',
    u'Greu'
])

class RISCEXCLUSIOSOCIAL(Variable):
    column = EnumCol(
        enum=RISCEXCLUSIOSOCIAL_CATEGORIA,
        default=0  # No
    )
    entity = Household
    definition_period = MONTH
    label = u"Nivell de risc d'exclusio social"


class ENACOLLIMENT(Variable):
    column = BoolCol
    entity = Person
    definition_period = MONTH
    label = "L'infant es troba en regim d'acolliment"
    set_input = set_input_dispatch_by_period


class PUNTSGRAUDISCAPACITAT(Variable):
    column = FloatCol
    entity = Person
    definition_period = MONTH
    label = "Punts assignats a cada membre segons el grau de discapacitat"
    set_input = set_input_dispatch_by_period

    def formula(person, period, legislation):
        grau_discapacitat = person("GRAUDISCAPACITAT", period)
        return select([grau_discapacitat <= 33, grau_discapacitat > 33], [1.5, 3])

class PUNTUACIO_FAMILIAR_EG_233(Variable):
    column = FloatCol
    entity = Household
    definition_period = MONTH
    label = "Puntuacio que te la familia per a clacular si es susceptible de rebre ajut extraordinari"
    set_input = set_input_dispatch_by_period

    def formula(household, period, legislation):
        tipus_familia_nombrosa = household("FAMNOMBROSA", period)
        puntuacio_familia_nombrosa = select([tipus_familia_nombrosa == FAMNOMBROSA_CATEGORIA['General'],
                                             tipus_familia_nombrosa == FAMNOMBROSA_CATEGORIA['Especial']],
                                            [1.5, 3])
        tipus_familia_monoparental = household("FAMMONOPARENTAL", period)
        puntuacio_familia_monoparental = select([tipus_familia_monoparental == FAMMONOPARENTAL_CATEGORIA['General'],
                                                  tipus_familia_monoparental == FAMMONOPARENTAL_CATEGORIA['Especial']],
                                                 [1.5, 3])
        tipus_risc_exclusio_social = household("RISCEXCLUSIOSOCIAL", period)
        puntuacio_risc_exclusio_social = select([tipus_risc_exclusio_social == RISCEXCLUSIOSOCIAL_CATEGORIA["Existeix"],
                                                 tipus_risc_exclusio_social == RISCEXCLUSIOSOCIAL_CATEGORIA["Greu"]],
                                                [10, 15])
        punts_per_grau_discapacitat_membres = household.members("PUNTSGRAUDISCAPACITAT", period)
        punts_grau_discapacitat = household.sum(punts_per_grau_discapacitat_membres)

        en_acolliment_membres = household.members("PUNTSGRAUDISCAPACITAT", period)
        punts_en_acolliment = household.sum(en_acolliment_membres) * 3

        return puntuacio_familia_nombrosa + puntuacio_familia_monoparental + puntuacio_risc_exclusio_social + \
               punts_grau_discapacitat + punts_en_acolliment


class VOLUMNEGOCI(Variable):
    column = IntCol(val_type="monetary")
    entity = Household
    definition_period = YEAR
    label = "Household total income due family business"
    set_input = set_input_divide_by_period

class RENDIMENTSPATRIMONIALS(Variable):
    column = IntCol(val_type="monetary")
    entity = Household
    definition_period = YEAR
    label = "Household total income due properties"
    set_input = set_input_dispatch_by_period

class VALORCADASTRALRUSTICEXTRES(Variable):
    column = IntCol(val_type="monetary")
    entity = Household
    definition_period = YEAR
    label = "Household total valuation of rustic properties"
    set_input = set_input_dispatch_by_period

class VALORCADASTRALURBA(Variable):
    column = IntCol(val_type="monetary")
    entity = Household
    definition_period = YEAR
    label = "Household total valuation of urban properties"
    set_input = set_input_dispatch_by_period

class EG_233_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Person
    definition_period = MONTH
    label = "EG_233 - AJUTS INDIVIDUALS DE MENJADOR CIUTAT BARCELONA"

    def formula(person, period, legislation):

        ESCOLARITZAT = person('ESCOLARITZAT', period)
        MENJADOR = person('MENJADOR', period)
        NOBECAMENJADOR = person('BECAMENJADOR', period) == False
        ESCHILD = person.has_role(Household.CHILD)
        CUSTODIA = person.household.first_parent('GUARICUS', period)
        compleix_els_requeriments = CUSTODIA * \
                                    ESCOLARITZAT * \
                                    MENJADOR * \
                                    NOBECAMENJADOR * \
                                    ESCHILD

        compleix_ajut_ordinari = determine_ajut_ordinari_nr_compliance(person, period, legislation)

        puntuacio_familiar = person.household("PUNTUACIO_FAMILIAR_EG_233", period)
        volum_de_negoci = person.household("VOLUMNEGOCI", period.last_year)
        rendiments_patrimonials = person.household("RENDIMENTSPATRIMONIALS", period.last_year)
        valoracio_cadastral_propietats_rustiques = person.household("VALORCADASTRALRUSTICEXTRES", period.this_year)
        valor_cadastral_propietats_urbanes = person.household("VALORCADASTRALURBA", period.this_year)

        print volum_de_negoci, rendiments_patrimonials, valoracio_cadastral_propietats_rustiques, valor_cadastral_propietats_urbanes
        print(puntuacio_familiar >= 15), (volum_de_negoci < 155000), (rendiments_patrimonials < 1700), (valoracio_cadastral_propietats_rustiques < 131390), (valor_cadastral_propietats_urbanes < 42900)

        compleix_ajut_extraordinari = determine_ajut_extraordinari_nr_compliance(person, period, legislation) \
                                      * (puntuacio_familiar >= 15) \
                                      * (volum_de_negoci < 155000) \
                                      * (rendiments_patrimonials < 1700) \
                                      * (valoracio_cadastral_propietats_rustiques < 131390) \
                                      * (valor_cadastral_propietats_urbanes < 42900)

        import_EG_233 = select([compleix_ajut_extraordinari, compleix_ajut_ordinari], [6, 3])

        return compleix_els_requeriments * import_EG_233


def determine_ajut_extraordinari_nr_compliance(person, period, legislation):
    nr_adult_demandant = person.household.first_parent('ingressos_disponibles', period) * 12
    nr_adult_secundari = person.household.second_parent('ingressos_disponibles', period) * 12
    other_adult_satisfy_extraordinari_nr = person.household.all(person.household.members('NR_INF_1450_08', period),
                                                                role=Household.OTHER_ADULT)

    children_satisfy_extraordinari_nr = person.household.all(person.household.members('NR_INF_1740_12', period),
                                                             role=Household.CHILD)

    adults_satisfy_extraordinary_nr = (nr_adult_demandant < 5800.38) * (nr_adult_secundari < 2900.16)
    return adults_satisfy_extraordinary_nr * other_adult_satisfy_extraordinari_nr * children_satisfy_extraordinari_nr


def determine_ajut_ordinari_nr_compliance(person, period, legislation):
    nr_adult_demandant = person.household.first_parent('ingressos_disponibles', period) * 12
    nr_adult_secundari = person.household.second_parent('ingressos_disponibles', period) * 12

    other_adult_satisfy_ordinari_nr = person.household.all(person.household.members('NR_INF_2416_80', period),
                                                           role=Household.OTHER_ADULT)

    children_satisfy_ordinari_nr = person.household.all(person.household.members('NR_INF_2900_20', period),
                                                        role=Household.CHILD)

    adults_satisfy_ordinari_nr = (nr_adult_demandant < 9667.30) * (nr_adult_secundari < 4833.60)
    return adults_satisfy_ordinari_nr * other_adult_satisfy_ordinari_nr * children_satisfy_ordinari_nr
