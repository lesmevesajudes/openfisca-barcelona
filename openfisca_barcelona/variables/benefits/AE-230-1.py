# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_barcelona.entities import *


class AE_230_01_mensual(Variable):
    value_type = float
    unit = 'currency'
    entity = Persona
    definition_period = MONTH
    label = "Ajuda 0-16"

    def formula(persona, period, parameters):
        es_sustentador_i_te_la_custodia = persona.has_role(Familia.SUSTENTADOR_I_CUSTODIA)
        tipus_monoparental = persona.familia('tipus_familia_monoparental', period)
        es_monoparental = tipus_monoparental != tipus_monoparental.possible_values.nop
        tipus_custodia = persona.familia('tipus_custodia', period)
        es_monoparental_custodia_total = es_monoparental * (tipus_custodia == tipus_custodia.possible_values.total)
        es_monoparental_custodia_compartida = es_monoparental * (tipus_custodia == tipus_custodia.possible_values.compartida)
        compleix_criteris_AE230 = persona.familia.members('compleix_criteris_AE230', period)
        algun_membre_compleix_criteris_AE230 = persona.familia.any(compleix_criteris_AE230)
        import_ajuda = parameters(period).benefits.AE230.import_total[tipus_custodia]

        return algun_membre_compleix_criteris_AE230 * es_monoparental * es_sustentador_i_te_la_custodia * import_ajuda
