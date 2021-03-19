import sys
from typing import Dict, List, Tuple

sys.setrecursionlimit(5000)

Node = Tuple[str, str]


def list_to_tree(data: List[Node]) -> Dict:
    """
    Функция преобразует список кортежей формата (имя_родительского_узла, имя_дочернего_узла)
    в дерево, представленное в виде словаря

    Parameters
    ---------
    data : list of tuples[str, str]
        Входной список кортежей формата (имя_родительского_узла, имя_дочернего_узла)

    Returns
    ----------
    result : dict
        Словарь, в котором все узлы из входного списка кортежей расположены согласно их иерархии

    Raises
    ------
    ValueError
        Если в исходных данных присутствует цикл из узлов
    """
    has_parent = set()      # множество для хранения узлов, у которых есть родитель
    roots = set()           # множество для хранения корневых узлов, у которых нет родителя

    # словарь, в который будут добавлены все узлы
    all_items = {}
    for parent, child in data:
        # вариант, когда у узла отсутствует родитель, в этом случае он становится корневым узлом
        if not parent:
            all_items[child] = {}
            roots.add(child)
        # вариант, когда родитель присутствует, но еще не занесен в общий словарь
        elif parent not in all_items:
            all_items[parent] = {}
        # вариант, когда родитель присутствует и дочерний узел еще не содержится внутри
        if parent and (child not in all_items[parent]):
            all_items[child] = {}
            all_items[parent][child] = all_items[child]
            has_parent.add(child)

    # формирование результатов
    result = {}
    # В данном цикле из общего словаря выбираются узлы, у которых нет родителя, т.е. они являются корневыми
    # и содержат в себе всех потомков, после чего заносятся в словарь с результатами
    for parent, child in all_items.items():
        if parent not in has_parent:
            result[parent] = child

    # Проверка на наличие циклов в графе
    # Если в графе присутствует цикл, то функция отработает без ошибок,
    # но в результирующем графе будут отсутстствовать все узлы, входящие в цикл.
    # Проверка на наличие циклов происходит путем сравнения длины исходного списка
    # и количества узлов в результирующем словаре.
    if len(data) != _count_nodes(result) - 1:
        raise ValueError('В графе присутствует цикл')

    return result


def _count_nodes(node: Dict) -> int:
    """
    Рекурсивно подсчитывает количество узлов в переданном графе.
    Вспомогательная функция для list_to_tree

    Parameters
    ---------
    node : Dict
        Словарь, содержащий дерево узлов

    Returns
    ----------
    int
        Количество узлов, содержащихся в дереве + 1 (т.к. на первой итерации
        в качестве начального значения берется 1 - ее следует вычесть из результата функции
        для получения точного значения
    """
    if node is None:
        return 0
    return 1 + sum(_count_nodes(node[child]) for child in node.keys())


if __name__ == '__main__':
    data = [
        (None, 'a'),
        (None, 'b'),
        (None, 'c'),
        ('a', 'a1'),
        ('a', 'a2'),
        ('b', 'b1'),
        ('a2', 'a3'),
        ('b1', 'b2'),
        ('a3', 'a4'),
        ('a4', 'a5'),
        ('a', 'd'),
        (None, 'e'),
        ('e', 'f'),
    ]

    data_with_loop = [
        (None, 'a'),
        (None, 'b'),
        (None, 'c'),
        ('a', 'a1'),
        ('a', 'a2'),
        ('b', 'b1'),
        ('a2', 'a3'),
        ('b1', 'b2'),
        ('a3', 'a4'),
        ('a4', 'a5'),
        ('a5', 'a4'),   # loop
        ('a', 'd'),
        ('e', 'f'),
    ]

    tree = {
        'a': {
            'a1': {},
            'a2': {
                'a3': {
                    'a4': {
                        'a5': {},
                    },
                },
            },
            'd': {},
        },
        'b': {
            'b1': {
                'b2': {},
            },
        },
        'c': {},
        'e': {
            'f': {},
        },
    }

    print(list_to_tree(data))
    assert list_to_tree(data) == tree, 'wrong result'

    pairs = [(None, 'a0'),] + [(f'a{i}', f'a{i + 1}') for i in range(999)]
    print(list_to_tree(pairs))
