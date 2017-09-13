# -*- coding: utf-8 -*-

# This file defines the entities needed by our legislation.

from openfisca_core.entities import build_entity

Household = build_entity(
    key="household",
    plural="households",
    label=u'Household',
    roles=[{
        'key': 'parent',
        'plural': 'parents',
        'label': u'Parents',
        'max': 2,
        'subroles': ['first_parent', 'second_parent']
        },
        {
        'key': 'other_adult',
        'plural': 'other_adults',
        'label': u'Other adults'
        },
        {
        'key': 'child',
        'plural': 'children',
        'label': u'Child',
        }]
    )

Person = build_entity(
    key="person",
    plural="persons",
    label=u'Person',
    is_person=True,
    )

entities = [Household, Person]
