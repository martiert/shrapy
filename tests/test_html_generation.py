#!/usr/bin/env python
import unittest
import shrapy.html_generation as html


class TestHtmlGeneration(unittest.TestCase):
    def test_simple_person_schema(self):
        schema = {
            'title': 'Superhero Registration Act',
            'description': 'All super-powered individuals are required to surrender their real names to the government',
            'questions': [
                {
                    'caption': 'Superhuman Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Real Name',
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
        <p>All super-powered individuals are required to surrender their real names to the government</p>
        <form action="register">
            Superhuman Name: <input type="text" name="superhuman_name"/><br/>
            Real Name: <input type="text" name="real_name"/><br/>
        </form>
    </body>
</html>'''
        self.assertEqual(expected, html.generate(schema))

    def test_schema_with_radio(self):
        schema = {
            'title': 'Superhero Registration Act',
            'questions': [
                {
                    'caption': 'Superhuman Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Real Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Superpower',
                    'type': 'radio',
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
        <p></p>
        <form action="register">
            Superhuman Name: <input type="text" name="superhuman_name"/><br/>
            Real Name: <input type="text" name="real_name"/><br/>
            Superpower:<br/>
            <input type="radio" name="superpower" value="flying"/>Flying<br/>
            <input type="radio" name="superpower" value="invisibility"/>Invisibility<br/>
            <input type="radio" name="superpower" value="superstrength"/>Superstrength<br/>
        </form>
    </body>
</html>'''
        self.assertEqual(expected, html.generate(schema))

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
        with self.assertRaisesRegex(html.MissingRequiredFieldError, 'Missing.*title.*'):
            html.generate(schema)

    def test_missing_type_on_question(self):
        schema = {
            'title': 'Superhero Registration Act',
            'questions': [
                {
                    'caption': 'Superhuman Name',
                },
                {
                    'caption': 'Real Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Superpower',
                    'type': 'radio',
                    'alternatives': [
                        'Flying',
                        'Invisibility',
                        'Superstrength',
                    ],
                },
            ],
        }

        with self.assertRaisesRegex(html.MissingRequiredFieldError, 'Missing.*type.*'):
            html.generate(schema)

    def test_missing_no_alternatives_on_radio_buttons(self):
        schema = {
            'title': 'Superhero Registration Act',
            'questions': [
                {
                    'caption': 'Superhuman Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Real Name',
                    'type': 'textbox',
                },
                {
                    'caption': 'Superpower',
                    'type': 'radio',
                    'alternatives': [
                    ],
                },
            ],
        }

        with self.assertRaisesRegex(html.AlternativesMissingError, 'Missing radio button alternatives.*Superpower.*'):
            html.generate(schema)
