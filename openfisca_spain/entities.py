# -*- coding: utf-8 -*-

# This file defines the entities needed by our legislation.

from openfisca_core.entities import build_entity

Familia = build_entity(
    key="familia",
    plural="families",
    label=u'Familia',
    roles=[{
        'key': 'parent',
        'plural': 'adults',
        'label': u'Adults',
        'max': 2,
        'subroles': ['primer_adult', 'segon_adult']
        },
        {
        'key': 'altre_adult',
        'plural': 'altres_adults',
        'label': u'Other adults'
        },
        {
        'key': 'menor',
        'plural': 'menors',
        'label': u'Menor',
        }]
    )

Persona = build_entity(
    key="persona",
    plural="persones",
    label=u'Persona',
    is_person=True,
    )

entities = [Familia, Persona]
