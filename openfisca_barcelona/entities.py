# -*- coding: utf-8 -*-

# This file defines the entities needed by our legislation.

from openfisca_core.entities import build_entity

Familia = build_entity(
    key="familia",
    plural="families",
    label=u'Familia',
    roles=[{
        'key': 'sustentador_i_custodia',
        'plural': 'sustentadors_i_custodia',
        'label': u'sustentadors i custodia',
        'max': 2,
        'subroles': ['primer_adult', 'segon_adult']
        },
        {
        'key': 'sustentador',
        'plural': 'sustentadors',
        'label': u'sustentadors',
        'max': 2
        },
        {
        'key': 'altres_familiars',
        'plural': 'altres_familiars',
        'label': u'Other familiar'
        },
        {
        'key': 'menor',
        'plural': 'menors',
        'label': u'Menor',
        },
        {
        'key': 'altres_persones',
        'plural': 'altres_persones',
        'label': u'altres persones',
        }

    ]
    )


FamiliaFins2onGrau = build_entity(
    key="familia_fins_a_segon_grau",
    plural="families_fins_a_segon_grau",
    label=u'Familia fins a segon grau',
    roles=[{
        'key': 'familiars',
        'plural': 'familiars',
        'label': u'persones familiars'
    },
    {
        'key': 'no_familiars',
        'plural': 'no_familiars',
        'label': u'persones no familiars'
    }
    ]
)

UnitatDeConvivencia = build_entity(
    key="unitat_de_convivencia",
    plural="unitats_de_convivencia",
    label=u'Unitat de convivència',
    roles=[{
        'key': 'persones_que_conviuen',
        'plural': 'persones_que_conviuen',
        'label': u'persones que conviuen'
    },
        {
        'key': 'titular_contracte',
        'plural': 'titulars_contracte',
        'label': u'titular del contracte'
        }
    ]
)

FamiliaRai = build_entity(
    key="familia_rai",
    plural="families_rai",
    label=u'Familia criteris rai',
    roles=[{
        'key': 'familiars',
        'plural': 'familiars',
        'label': u'persones familiars'
    }
    ]
)

FamiliaNombrosa = build_entity(
    key="familia_nombrosa",
    plural="families_nombroses",
    label=u'Familia nombrosa',
    roles=[{
        'key': 'familiars',
        'plural': 'familiars',
        'label': u'persones familiars'
    }
    ]
)

Persona = build_entity(
    key="persona",
    plural="persones",
    label=u'Persona',
    is_person=True,
    )


entities = [Familia, Persona, UnitatDeConvivencia, FamiliaFins2onGrau, FamiliaRai, FamiliaNombrosa]
