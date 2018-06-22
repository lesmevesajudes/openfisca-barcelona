# -*- coding: utf-8 -*-

# This file defines the entities needed by our legislation.

from openfisca_core.entities import build_entity

Familia = build_entity(
    key="familia",
    plural="families",
    label=u'Familia',
    roles=[{
        'key': 'adult',
        'plural': 'adults',
        'label': u'Adults',
        'max': 2,
        'subroles': ['primer_adult', 'segon_adult']
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

Persona = build_entity(
    key="persona",
    plural="persones",
    label=u'Persona',
    is_person=True,
    )

entities = [Familia, Persona, UnitatDeConvivencia]
