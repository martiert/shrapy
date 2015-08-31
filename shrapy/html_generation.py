import textwrap


class MissingRequiredFieldError(Exception):
    def __init__(self, field):
        self._field = field

    def __str__(self):
        return 'Missing required field: {field}'.format(field=self._field)


class AlternativesMissingError(Exception):
    def __init__(self, boxtype, name):
        self._boxtype = boxtype
        self._name = name

    def __str__(self):
        return 'Missing {type} alternatives for question: {question}'.format(type=self._boxtype,
                                                                             question=self._name)


def get_radio_input(alternative, name):
    value = alternative.lower().replace(' ', '_')
    return '<input type="radio" name="{name}" value="{value}"/>{alternative}<br/>'.format(name=name,
                                                                                          value=value,
                                                                                          alternative=alternative)


def get_checkbox_input(alternative, name):
    value = alternative.lower().replace(' ', '_')
    return '<input type="checkbox" name="{name}" value="{value}"/>{alternative}<br/>'.format(name=name,
                                                                                             value=value,
                                                                                             alternative=alternative)


def textbox_question(question):
    caption = question['caption']
    name = caption.lower().replace(' ', '_')

    return '{caption}: <input type="text" name="{name}"/><br/>'.format(caption=caption,
                                                                       name=name)


def radio_question(question):
    name = question['caption'].lower().replace(' ', '_')
    alternatives = question['alternatives']

    if not alternatives:
        raise AlternativesMissingError('radio button', question['caption'])

    return '''{caption}:<br/>
{inputs}'''.format(caption=question['caption'],
                   inputs='\n'.join(get_radio_input(alternative, name) for alternative in alternatives))


def checkbox_question(question):
    name = question['caption'].lower().replace(' ', '_')
    alternatives = question['alternatives']

    if not alternatives:
        raise AlternativesMissingError('checkbox', question['caption'])

    return '''{caption}:<br/>
{inputs}'''.format(caption=question['caption'],
                   inputs='\n'.join(get_checkbox_input(alternative, name) for alternative in alternatives))


def extract_question(question):
    extract_type = {
        'textbox': textbox_question,
        'radio': radio_question,
        'checkbox': checkbox_question,
    }
    try:
        type = question['type']
    except KeyError:
        raise MissingRequiredFieldError('type')

    return extract_type[type](question)


def generate(schema):
    try:
        title = schema['title']
    except KeyError:
        raise MissingRequiredFieldError('title')

    description = ''
    if 'description' in schema:
        description = schema['description']

    questions = schema['questions']

    content = [extract_question(question) for question in questions]

    result = '''<html>
    <head>
        <meta charset="UTF-8"/>
        <title>{title}</title>
    </head>
    <body>
        <p>{title}</p>
        <p>{description}</p>
        <form action="register">
{content}
        </form>
    </body>
</html>'''.format(title=title,
                  description=description,
                  content=textwrap.indent('\n'.join(content), 12 * ' '))
    return result
