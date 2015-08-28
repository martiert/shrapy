#!/usr/bin/env python
import unittest
import html_generation


class TestHtmlGeneration(unittest.TestCase):
    def test_simple_person_schema(self):
        schema = {
            'title': 'Superhero Registration Act',
            'questions': [
                {
                    'caption': 'Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Email',
                    'type': 'textbox',
                },
            ],
        }

        expected = '''<html>
    <meta charset="UTF-8"/>
    <header>
        <title>Superhero Registration Act</title>
    </header>
    <body>
        <p>Superhero Registration Act</p>
        <form action="register">
            Name: <input type="text" name="name"/><br/>
            Email: <input type="text" name="email"/><br/>
        </form>
    </body>
</html>'''
        self.assertEqual(expected, html_generation.generate(schema))

    def test_schema_with_checkbox(self):
        schema = {
            'title': 'Superhero Registration Act',
            'questions': [
                {
                    'caption': 'Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Id',
                    'type': 'textbox',
                },
                {
                    'caption': 'Superpower',
                    'type': 'checkbox',
                    'alternatives': [
                        'Flying',
                        'Invisibility',
                        'Superstrength',
                    ],
                },
            ],
        }

        expected = '''<html>
    <meta charset="UTF-8"/>
    <header>
        <title>Superhero Registration Act</title>
    </header>
    <body>
        <p>Superhero Registration Act</p>
        <form action="register">
            Name: <input type="text" name="name"/><br/>
            Id: <input type="text" name="id"/><br/>
            Superpower:<br/>
            <input type="radio" name="superpower" value="flying"/>Flying<br/>
            <input type="radio" name="superpower" value="invisibility"/>Invisibility<br/>
            <input type="radio" name="superpower" value="superstrength"/>Superstrength<br/>
        </form>
    </body>
</html>'''
        self.assertEqual(expected, html_generation.generate(schema))

    def test_missing_title(self):
        schema = {
            'questions': [
                {
                    'caption': 'Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Email',
                    'type': 'textbox',
                },
            ],
        }
        with self.assertRaises(KeyError):
            html_generation.generate(schema)
