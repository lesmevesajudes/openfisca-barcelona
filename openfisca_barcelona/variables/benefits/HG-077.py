# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from datetime import datetime
from openfisca_barcelona.variables.demographics import *


class resident_a_catalunya_durant_5_anys(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has legal residence in catalonia for at least 5 years"
    set_input = set_input_dispatch_by_period
    default = False


class victima_de_terrorisme(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is a victim of terrorism"
    set_input = set_input_dispatch_by_period
    default = False


class risc_d_exclusio_social(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is in risk of social exclusion"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return persona.familia("nivell_de_risc_d_exclusio_social", period) != NIVELL_DE_RISC_D_EXCLUSIO_SOCIAL["No"]


class existeix_un_contracte_de_lloguer(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has a rent contract"
    set_input = set_input_dispatch_by_period
    default = False


class LLOGMAXBCN(Variable):  # Fixme: This should be in parameters
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The house hold rent does not exceed maximum rent amount for Barcelona"
    set_input = set_input_dispatch_by_period
    default = False


class esta_al_corrent_del_pagament_de_lloguer(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The rent payments must be up to date"
    set_input = set_input_dispatch_by_period
    default = False


class lloguer_domiciliat(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "The rent payments are made through a bank"
    set_input = set_input_dispatch_by_period
    default = False


class pot_rebre_subvencions(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is not subject to any condition that is forbidden"
    set_input = set_input_dispatch_by_period
    default = False


class al_corrent_de_les_obligacions_tributaries(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period
    default = False


class es_BLJ(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has more than 65 years at 31/12/2012"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return major_de_65_el_2012_12_31(persona('data_naixement', period))


class titular_contracte_de_lloguer(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is the one who appears in rent contract"
    set_input = set_input_dispatch_by_period


class relacio_de_parentiu_amb_el_propietari(Variable):
    column = BoolCol
    entity = Familia
    definition_period = MONTH
    label = "There is some kind of family relation with the owner"
    set_input = set_input_dispatch_by_period


def major_de_65_el_2012_12_31(data_de_naixement):
    return data_de_naixement < datetime.strptime('1948-1-1', "%Y-%m-%d").date()


class import_del_lloguer(Variable):
    column = FloatCol
    entity = Familia
    definition_period = MONTH
    label = "Rent amount payed every month"
    set_input = set_input_dispatch_by_period


class ha_residit_a_lextranger_els_ultims_24_mesos(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living abroad for the last 24 months"
    set_input = set_input_dispatch_by_period
    default = False

class ha_residit_a_catalunya_els_ultims_24_mesos(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living in Catalonia for the last 24 months"
    set_input = set_input_dispatch_by_period
    default = False

class ha_residit_a_lextranger_36_mesos_continuats(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living abroad for at least 36 months"
    set_input = set_input_dispatch_by_period
    default = False

class ha_residit_a_lextranger_60_mesos_discontinuats(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The person has been living abroad for at least 60 months"
    set_input = set_input_dispatch_by_period
    default = False


class demarcacio_077(Variable):
    column = StrCol
    entity = Persona
    definition_period = MONTH
    label = u"The province where this person lives"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, params):
        print persona("codi_postal_empadronament", period)
        codi_postal_empadronament = int(persona("codi_postal_empadronament", period)[0])
        print codi_postal_empadronament
        # http://www.solosequenosenada.com/2010/09/16/listado-de-todos-los-codigos-postales-de-espana/
        codis_postals_barcelona_ciutat = np.array([8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010, 8011, 8012,
                                            8013, 8014, 8015, 8016, 8017, 8018, 8019, 8020, 8021, 8022, 8023, 8024,
                                            8025, 8026, 8027, 8028, 8029, 8030, 8031, 8032, 8033, 8034, 8035, 8036,
                                            8037, 8038, 8039, 8040, 8041, 8042, 8075, 8196, 8830, 8903, 8904, 8930,
                                            8960])
        es_barcelona_ciutat = np.argmax(codis_postals_barcelona_ciutat == codi_postal_empadronament)

        es_barcelona_provincia = (not es_barcelona_ciutat) & (8000 < codi_postal_empadronament < 9000)
        es_girona = 17000 < codi_postal_empadronament < 18000
        es_tarragona = 43000 < codi_postal_empadronament < 44000
        es_lleida = 25000 < codi_postal_empadronament < 26000
        es_terres_de_lebre = False         # TODO https://ca.wikipedia.org/wiki/Terres_de_l%27Ebre

        return select(
            [es_barcelona_ciutat, es_barcelona_provincia, es_girona, es_terres_de_lebre, es_tarragona, es_lleida ],
            ["barcelona_ciutat", "barcelona", "girona",  "terres_de_lebre", "tarragona", "lleida"]
        )


class lloguer_maxim_segons_demarcacio_077(Variable):
    column = IntCol
    entity = Persona
    definition_period = MONTH
    label = u"Maximal rent amount by demarcation"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, params):
        demarcacio = persona("demarcacio_077", period)
        return select(
            [demarcacio == "barcelona_ciutat",
             demarcacio == "barcelona",
             demarcacio == "girona",
             demarcacio == "tarragona",
             demarcacio == "lleida",
             demarcacio == "terres_de_lebre"],
            [
                750,
                600,
                450,
                450,
                400,
                350
            ]
        )
