import textwrap


def get_radio_input(alternative, name):
    value = alternative.lower().replace(' ', '_')
    return '<input type="radio" name="{name}" value="{value}"/>{alternative}<br/>'.format(name=name,
                                                                                          value=value,
                                                                                          alternative=alternative)


def textbox_question(question):
    caption = question['caption']
    name = caption.lower().replace(' ', '_')

    return '{caption}: <input type="text" name="{name}"/><br/>'.format(caption=caption,
                                                                       name=name)


def checkbox_question(question):
    name = question['caption'].lower().replace(' ', '_')
    alternatives = question['alternatives']

    return '''{caption}:<br/>
{inputs}'''.format(caption=question['caption'],
                   inputs='\n'.join(get_radio_input(alternative, name) for alternative in alternatives))


def extract_question(question):
    extract_type = {
        'textbox': textbox_question,
        'checkbox': checkbox_question,
    }
    return extract_type[question['type']](question)


def generate(schema):
    title = schema['title']
    questions = schema['questions']

    content = [extract_question(question) for question in questions]

    result = '''<html>
    <meta charset="UTF-8"/>
    <header>
        <title>{title}</title>
    </header>
    <body>
        <p>{title}</p>
        <form action="register">
{content}
        </form>
    </body>
</html>'''.format(title=title,
                  content=textwrap.indent('\n'.join(content), 12 * ' '))
    return result
