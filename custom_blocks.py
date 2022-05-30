import markdown

def spell_card(ctx, title=None, level=None, school=None, casting_time=None, distance=None, components=None, duration=None, classes=None, header='3'):

    spell_html = '<div class="spellcard">\n'

    if title:
        spell_html += f'<h{header} class="spellcard-title">{title}</h{header}>\n'
    if str(level).isdigit():
        level = str(level) + ' уровень'
    if level or school:
        spell_html += f'<p class="spellcard-level-school">{", ".join([x for x in [level, school] if x is not None])}</p>\n'
    if casting_time:
        spell_html += f'<p class="spellcard-property"><b>Время накладывания:</b> {casting_time}</p>\n'
    if distance:
        spell_html += f'<p class="spellcard-property"><b>Дистанция</b>: {distance}</p>\n'
    if components:
        spell_html += f'<p class="spellcard-property"><b>Компоненты</b>: {components}</p>\n'
    if duration:
        spell_html += f'<p class="spellcard-property"><b>Длительность</b>: {duration}</p>\n'
    if classes:
        spell_html += f'<p class="spellcard-property"><b>Классы</b>: {classes}</p>\n'

    text_blocks = [f'<p class="spellcard-text">{line}</p>' for line in ctx.content.split('\n\n') if line != '']
    content = '\n'.join(text_blocks)

    spell_html += f'{content}\n</div>'

    return spell_html


def item_card(ctx, title=None, type=None, subtype=None, quality=None, subquality=None, price=None, header='3'):

    item_html = '<div class="itemcard">\n'

    if title:
        item_html += f'<h{header} class="itemcard-title">{title}</h{header}>\n'

    type_description = None
    if type and subtype:
        type_description = f'{type} ({subtype})'
    elif type:
        type_description = str(type)
    elif subtype:
        type_description = f'({subtype})'

    quality_description = None
    if quality and subquality:
        quality_description = f'{quality} ({subquality})'
    elif quality:
        quality_description = str(quality)
    elif subquality:
        quality_description = f'({subquality})'

    description = None
    if type_description and quality_description:
        description = f'{type_description}, {quality_description}'
    elif type_description:
        description = type_description
    elif quality_description:
        description = quality_description

    if description:
        item_html += f'<p class="itemcard-description">{description}</p>\n'
    if price:
        item_html += f'<p class="itemcard-property"><b>Рекомендованная стоимость</b>: {price}</p>\n'

    text_blocks = [f'<p class="itemcard-text">{line}</p>' for line in ctx.content.split('\n\n') if line != '']
    content = '\n'.join(text_blocks)

    item_html += f'{content}\n</div>'

    return item_html
