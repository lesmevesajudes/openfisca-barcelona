from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class tempsEmpadronatHabitatgeActual(Enum):
    no_empadronat = "no_empadronat"
    menys_nou_mesos = "menys_9_mesos"
    nou_mesos_o_mes = "9_mesos_o_mes"


class temps_empadronat_habitatge_actual(Variable):
    value_type = Enum
    possible_values = tempsEmpadronatHabitatgeActual
    default_value = tempsEmpadronatHabitatgeActual.no_empadronat
    entity = Persona
    label = u"labor situation"
    definition_period = MONTH


class ha_rebut_oferta_per_accedir_a_habitatge_i_lha_rebutjada(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "The user has received an offer for a house and has declined"
    default_value = False


class es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "The house is property of agencia de l'habitatge"
    default_value = False


class existeix_deute_en_el_pagament_de_la_hipoteca(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "A debt in the mortage exists"
    default_value = False


class existeix_deute_en_el_pagament_del_lloguer(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "A debt in the rent exists"
    default_value = False


class fa_mes_de_12_mesos_que_existeix_el_deute_de_hipoteca(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "The debt has existed for more than 12 months"
    default_value = False


class ha_pagat_almenys_3_quotes_del_lloguer(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "A debt in the rent exists"
    default_value = False


class ha_perdut_lhabitatge_en_els_ultims_2_anys(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "The user has been evicted in the last 2 years"
    default_value = False


class ha_pagat_12_mesos_daquesta_hipoteca(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "A debt in the rent exists"
    default_value = False


class tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person living in the house has a property"
    default_value = False


class relacio_de_parentiu_amb_el_propietari(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Some person has a familiar relation to the owner"
    default_value = False


class ha_participat_en_un_proces_de_mediacio(Variable):
    value_type = bool
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "The user has participated in a mediation process between owner and administration"
    default_value = False


class import_del_lloguer(Variable):
    value_type = float
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "rent amount"
    default_value = 0


class import_de_la_hipoteca(Variable):
    value_type = float
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "Mortage amount"
    default_value = 0


class ZonaDeLHabitatge(Enum):
    zona_a = "zona_a"
    zona_b = "zona_b"
    zona_c = "zona_c"
    zona_d = "zona_d"
    desconegut = "desconegut"


class zona_de_lhabitatge(Variable):
    value_type = Enum
    possible_values = ZonaDeLHabitatge
    default_value = ZonaDeLHabitatge.desconegut
    entity = UnitatDeConvivencia
    label = u"Zone of the house"
    definition_period = MONTH


class pot_ser_solicitant_HA001(Variable):
    value_type = bool
    entity = Persona
    definition_period = MONTH
    label = "Is this person suitable to apply for this benefit"
    default_value = False

    def formula(persona, period, legislation):
        tipus_document_identitat = persona("tipus_document_identitat", period)
        has_DNI = tipus_document_identitat == tipus_document_identitat.possible_values.DNI
        has_NIE = tipus_document_identitat == tipus_document_identitat.possible_values.NIE
        empadronat_a_barcelona = persona("municipi_empadronament", period) == "barcelona"
        temps_empadronat_a_lhabitatge = persona("temps_empadronat_habitatge_actual", period)
        empadronat_a_lhabitatge = temps_empadronat_a_lhabitatge != temps_empadronat_a_lhabitatge.possible_values.no_empadronat

        return (has_DNI + has_NIE) \
               * empadronat_a_barcelona \
               * empadronat_a_lhabitatge


def clauIRSCPonderat(membres):
    return select([membres == 1, membres == 2, membres == 3, membres > 3],
                  ['un', 'dos', 'tres', 'quatreomes'])


def clauMultiplicadors(membres, existeixDiscapacitat):
    return select([existeixDiscapacitat, membres == 1, membres >= 2],
                  ['discapacitats', 'un', 'dosomes']
                  )


class HA_001(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = "RENDA GARANTIDA CIUTADANA"

    def formula(unitatDeConvivencia, period, legislation):
        nr_membres = unitatDeConvivencia.nb_persons()
        discapacitats = unitatDeConvivencia.members("grau_discapacitat", period)
        existeix_algun_discapacitat = unitatDeConvivencia.any(discapacitats)
        ha_participat_en_un_proces_de_mediacio = unitatDeConvivencia("ha_participat_en_un_proces_de_mediacio", period)
        zona_de_lhabitatge = unitatDeConvivencia("zona_de_lhabitatge", period)
        poden_solicitar = unitatDeConvivencia.members("pot_ser_solicitant_HA001", period)
        existeix_solicitant_viable = unitatDeConvivencia.any(poden_solicitar)
        import_del_lloguer = unitatDeConvivencia("import_del_lloguer", period)
        import_del_lloguer_inferior_a_900_eur = import_del_lloguer < 900
        ingressos_bruts = unitatDeConvivencia.members("ingressos_bruts", period.last_year)
        ingressos_familia_mensuals = unitatDeConvivencia.sum(ingressos_bruts) / 12
        ingressos_familia_mes_ajuda_superen_import_lloguer = (ingressos_familia_mensuals + 300) > import_del_lloguer
        nivell_ingressos_maxim = \
            legislation(period).benefits.HA001.irsc_ponderat[zona_de_lhabitatge][clauIRSCPonderat(nr_membres)] \
            * legislation(period).benefits.HA001.multiplicadors[clauMultiplicadors(nr_membres, existeix_algun_discapacitat)]
        ingressos_bruts_dins_barems = ingressos_familia_mensuals < nivell_ingressos_maxim
        import_de_lloguer_supera_el_30_perc_dingressos = import_del_lloguer > (ingressos_familia_mensuals * 0.3)
        no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge = \
            unitatDeConvivencia("es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge", period) == False
        no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit = \
            unitatDeConvivencia("tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit", period) == False
        no_relacio_de_parentiu_amb_el_propietari = \
            unitatDeConvivencia("relacio_de_parentiu_amb_el_propietari", period) == False

        return ha_participat_en_un_proces_de_mediacio \
               * existeix_solicitant_viable \
               * ingressos_bruts_dins_barems \
               * import_del_lloguer_inferior_a_900_eur \
               * ingressos_familia_mes_ajuda_superen_import_lloguer \
               * import_de_lloguer_supera_el_30_perc_dingressos \
               * no_es_ocupant_dun_habitatge_gestionat_per_lagencia_de_lhabitatge \
               * no_tinc_alguna_propietat_a_part_habitatge_habitual_i_disposo_dusdefruit \
               * no_relacio_de_parentiu_amb_el_propietari
