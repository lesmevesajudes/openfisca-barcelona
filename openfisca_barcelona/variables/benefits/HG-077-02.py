from numpy import round

from openfisca_barcelona.variables.demographics import *
from openfisca_barcelona.variables.housing import *


class data_signatura_contracte_de_lloguer(Variable):
    column = DateCol(default=date(1970, 1, 1))  # By default, is no value is set for a simulation, we consider the
    # people involved in a simulation to be born on the 1st of Jan 1970.
    entity = Familia
    label = u"rent contract date"
    definition_period = ETERNITY  # This variable cannot change over time.


class mesos_des_de_la_signatura_del_contracte_de_lloguer(Variable):
    column = IntCol
    entity = Familia
    definition_period = MONTH
    label = u"Months since the rent contract was signed"

    # A person's age is computed according to its birth date.
    def formula(familia, period, legislation):
        data_signatura_contracte_de_lloguer = familia('data_signatura_contracte_de_lloguer', period)
        return (np.datetime64(period.date) - data_signatura_contracte_de_lloguer).astype('timedelta64[m]')


class deute_amb_el_propietari_de_lhabitatge_habitual(Variable):
    column = IntCol
    entity = Familia
    definition_period = MONTH
    label = u"Amount owed to owner"


class HG_077_02_mensual(Variable):
    column = FloatCol
    entity = Persona  # S'atorga a la persona que fa el contracte de lloguer
    definition_period = MONTH
    label = u"AJUT PER AL PAGAMENT DEL LLOGUER ESPECIAL URGENCIA"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, parameters):
        irsc = parameters(period).benefits.HG077.IRSC

        ingressos_familia_mensual = persona.familia("familia_ingressos_disponibles", period) / 12

        requeriments_solicitant = persona("titular_contracte_de_lloguer", period)

        requeriments_familia = (persona.familia("relacio_de_parentiu_amb_el_propietari", period).any() == False) \
                                * (ingressos_familia_mensual * 0.3 < persona.familia("import_del_lloguer", period)) \
                                * (persona.familia("import_del_lloguer", period) < parameters(period).benefits.HG077.lloguer_maxim_ciutat_barcelona) \
                                * (persona.familia("mesos_des_de_la_signatura_del_contracte_de_lloguer", period) > 12) \
                                * (persona.familia("deute_amb_el_propietari_de_lhabitatge_habitual", period) > 0) \
                                * (persona.familia("deute_amb_el_propietari_de_lhabitatge_habitual", period) < 3000)

        import_ajuda = min(
            3000,
            persona.familia("deute_amb_el_propietari_de_lhabitatge_habitual", period))

        return requeriments_solicitant * requeriments_familia * import_ajuda
