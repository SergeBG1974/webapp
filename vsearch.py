def search4letters(phrase: str, letters: str='aeiou') -> set:
    """ Возвращает множество букв из 'letters' найденных в указанной фразе
    :param phrase: Фраза для разбора
    :param letters: Наюор букв, которые требуется найти во фразе, по умолчанию - все гласные
    :return: возвращаем в виде множества
    """
    return set(letters).intersection(set(phrase))