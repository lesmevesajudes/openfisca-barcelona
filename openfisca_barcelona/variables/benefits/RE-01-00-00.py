# -*- coding: utf-8 -*-
# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from numpy.ma import logical_not
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

def clauNombreDeMebres(membres):
    return select([membres == 1, membres == 2, membres == 3, membres == 4, membres >= 5],
                  ['un', 'dos', 'tres', 'quatre', 'cincomes'])

class RE_01_00_00(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "RE_01_00_00 - Ingrés Mínim Vital"

    def formula(persona, period, parameters):
        major_de_17_anys = persona("edat", period) > 17
        major_de_22_anys = persona("edat", period) > 22
        menor_de_30_anys = persona("edat", period) < 30
        major_de_30_anys = persona("edat", period) > 29
        vida_independent = persona("vida_independent", period)
        centre_tutelat = persona("prove_de_centre_tutelat", period)
        nr_membres = persona.familia_fins_a_segon_grau.nb_persons()

        situacio_laboral = persona('situacio_laboral', period)
        no_jubilat = situacio_laboral != situacio_laboral.possible_values.jubilat

        es_victima_violencia_de_genere = persona("victima_violencia_de_genere", period)

        compleix_vida_independent =es_victima_violencia_de_genere \
            + menor_de_30_anys * (vida_independent > 1) * persona("alta_ss_12_mesos", period) \
            + major_de_30_anys * (vida_independent >= 1)

        orfe_absolut = persona("es_orfe_dels_dos_progenitors", period) * (persona.unitat_de_convivencia.nb_persons() == 1)
        empadronat_a_estat_espanyol = persona("municipi_empadronament", period) != b'no_empadronat_a_esp'
        compleix_edat = major_de_22_anys \
            + major_de_17_anys * (centre_tutelat + orfe_absolut)

        ingressos_bruts_familia = persona.familia('familia_ingressos_bruts', period.last_year)
        llindar_ingressos = parameters(period).benefits.RE01.llindars_ingressos[clauNombreDeMebres(nr_membres)]
        compleix_nivell_ingressos = ingressos_bruts_familia <= llindar_ingressos

        patrimoni_familia = persona.unitat_de_convivencia('valor_de_patrimoni', period.last_year)
        llindar_patrimoni = parameters(period).benefits.RE01.llindars_patrimoni[clauNombreDeMebres(nr_membres)]
        compleix_nivell_patrimoni = patrimoni_familia <= llindar_patrimoni

        compleix_els_requeriments = compleix_edat \
            * no_jubilat \
            * compleix_vida_independent \
            * compleix_nivell_ingressos \
            * compleix_nivell_patrimoni \
            * empadronat_a_estat_espanyol

        return compleix_els_requeriments
