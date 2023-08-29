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


def get_table_of_trader(list_of_header_block: tuple[str, ...], list_of_text_blocks: list[tuple[str, ...]],
                        inventory_header: str) -> str:
    len_ = len(list_of_text_blocks)
    text = [TOP_BORDER]

    for row in list_of_header_block:
        text.append(ROW.format(row))
    text += [MIDDLE_BORDER, ROW.format(f'{inventory_header}:'), LINE_BORDER]

    for i, text_block in enumerate(list_of_text_blocks):
        for row in text_block:
            text.append(ROW.format(row))
        if (i + 1) < len_:
            text.append(LINE_BORDER)
    text.append(BOTTOM_BORDER)
    return '\n'.join(text)


def get_table_fissures(header: str, list_of_text_block_by_tier: list[list[tuple[str, ...]]]) -> str:
    len_list = len(list_of_text_block_by_tier)
    text = [TOP_BORDER, ROW.format(header), MIDDLE_BORDER]
    for i, tier_blocks in enumerate(list_of_text_block_by_tier):
        len_blocks = len(tier_blocks)
        for j, text_block in enumerate(tier_blocks):
            for row in text_block:
                text.append(ROW.format(row))
            if (j + 1) < len_blocks:
                text.append(LINE_BORDER)
        if (i + 1) < len_list:
            text.append(MIDDLE_BORDER)
    text.append(BOTTOM_BORDER)
    return '\n'.join(text)


