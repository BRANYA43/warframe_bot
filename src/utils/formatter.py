LENGTH = 30
TOP_BORDER = '╔' + '═' * LENGTH + '╗'
MIDDLE_BORDER = '╠' + '═' * LENGTH + '╣'
BOTTOM_BORDER = '╚' + '═' * LENGTH + '╝'
LINE_BORDER = '║ ' + '-' * (LENGTH - 1)
ROW = '║ {}'


def get_table(header: str, list_of_text_blocks: list[tuple[str, ...]]) -> str:
    len_ = len(list_of_text_blocks)
    text = [TOP_BORDER, ROW.format(header), MIDDLE_BORDER]

    for i, text_block in enumerate(list_of_text_blocks):
        for row in text_block:
            text.append(ROW.format(row))
        if (i + 1) < len_:
            text.append(MIDDLE_BORDER)
    text.append(BOTTOM_BORDER)
    return '\n'.join(text)


def get_table_of_trader(header: str, list_of_text_blocks: list[tuple[str, ...]]) -> str:
    len_ = len(list_of_text_blocks)
    text = [TOP_BORDER, ROW.format(header), MIDDLE_BORDER, ROW.format('Inventory:'), LINE_BORDER]

    for i, text_block in enumerate(list_of_text_blocks):
        for row in text_block:
            text.append(ROW.format(row))
        if (i + 1) < len_:
            text.append(LINE_BORDER)
    text.append(BOTTOM_BORDER)
    return '\n'.join(text)
