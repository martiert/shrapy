#!/usr/bin/env python
import unittest
import python_jsonschema_objects as pjs


class TestPersonGenerator(unittest.TestCase):
    def test_simple_person(self):
        schema = {
            'definitions': {
                'Person': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'name': {'type': 'string'},
                        'employee_id': {'type': 'string'},
                    },
                    'required': ['name', 'employee_id'],
                },
            },
            'title': 'definitions',
            'type': 'object',
        }

        builder = pjs.ObjectBuilder(schema)
        ns = builder.build_classes()
        Person = ns.Person
        martin = Person(name='Martin Ertsås', employee_id='385254')
        self.assertEqual('Martin Ertsås', martin.name)
        self.assertEqual('385254', martin.employee_id)

    def test_multiple_classes(self):
        schema = {
            'definitions': {
                'Person': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'name': {'type': 'string'},
                        'employee_id': {'type': 'string'},
                    },
                    'required': ['name', 'employee_id'],
                },
            },
            'title': 'definitions',
            'type': 'object',
            'properties': {
                'NotAttending': {
                    'allOf': [
                        {
                            '$ref': '#/definitions/Person',
                        },
                        {
                            'properties': {
                                'info': {'type': 'string'},
                            },
                            'required': ['info'],
                        },
                    ],
                },
            },
        }

        builder = pjs.ObjectBuilder(schema)
        ns = builder.build_classes()
        Person = ns.Person
        martin = Person(name='Martin Ertsås', employee_id='385254')
        self.assertEqual('Martin Ertsås', martin.name)
        self.assertEqual('385254', martin.employee_id)

        NotAttending = ns.NotAttending
        olve = NotAttending(name='Olve Maudal', employee_id='123456', info='foo')
        self.assertEqual('Olve Maudal', olve.name)
        self.assertEqual('123456', olve.employee_id)
        self.assertEqual('foo', olve.info)
