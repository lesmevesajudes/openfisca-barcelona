from openfisca_core.model_api import *
from openfisca_barcelona.entities import *
from openfisca_barcelona.variables.benefits.HA import clauIRSCPonderat, clauMultiplicadors


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
        titular_contracte_de_lloguer = persona("titular_contracte_de_lloguer", period)
        return (has_DNI + has_NIE) \
               * empadronat_a_barcelona \
               * empadronat_a_lhabitatge \
               * titular_contracte_de_lloguer


class HA_001(Variable):
    value_type = float
    unit = 'currency'
    entity = UnitatDeConvivencia
    definition_period = MONTH
    label = u"AJUTS LLOGUER ESPECIAL URGENCIA PER A PERSONES BENEFICIARIES DE PRESTACIONS DERIVADES DE LA MEDIACIO A BARCELONA"

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
            legislation(period).benefits.HA.irsc_ponderat[zona_de_lhabitatge][clauIRSCPonderat(nr_membres)] \
            * legislation(period).benefits.HA.multiplicadors[
                clauMultiplicadors(nr_membres, existeix_algun_discapacitat)]
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
