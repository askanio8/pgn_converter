import numpy as np
from templates import templates

COLUMNS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
FIG_TYPES = {'K': 0, 'Q': 1, 'B': 2, 'N': 3, 'R': 4, 'P': 5}


def find_source_field(old_position, figure_type, target_field, source_field, is_capture):
    item_figure = np.nonzero(old_position[:, 8, 6])[0]  # фигуры, имеющие ход
    item_figure = np.intersect1d(item_figure, np.nonzero(old_position[:, 8, FIG_TYPES[figure_type]])[0],
                                 assume_unique=True)  # фигуры нужного типа

    if figure_type == 'P' and source_field == '':
        source_field = target_field[0]

    if len(source_field) == 1:
        item_figure = np.intersect1d(item_figure, np.nonzero(old_position[:, :8, COLUMNS[source_field]])[0],
                                     assume_unique=True)  # в указаннои столбце

    if figure_type == 'P' and len(item_figure) > 1:  # если несколько пешек в одном столбце
        #  и одна из них сделала взятие
        if is_capture:
            if item_figure[0] < 16:
                item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) + 1, COLUMNS[source_field]])[0]
            else:
                item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) - 1, COLUMNS[source_field]])[0]
        else:  # если был ход без взятия
            if item_figure[0] < 16:
                item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) + 1, COLUMNS[target_field[0]]])[0]
                if len(item_figure) == 0:
                    item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) + 2, COLUMNS[target_field[0]]])[0]
            else:
                item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) - 1, COLUMNS[target_field[0]]])[0]
                if len(item_figure) == 0:
                    item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) - 2, COLUMNS[target_field[0]]])[0]

    if len(item_figure) != 1:
        item_figure = find_by_moves(old_position, figure_type, item_figure, target_field)

    assert len(item_figure) == 1  # с архивами с lichess здесь будут происходить ошибки из-за неоднозначных записей
    x, y = np.transpose(np.nonzero(old_position[item_figure[0], :8, :]))[0]  # получаем её координаты
    source_field = list(COLUMNS)[y] + str(8 - x)
    return source_field


def find_by_moves(old_position, figure_type, item_figure, target_field):
    moves = templates[FIG_TYPES[figure_type]]
    moves = moves[np.abs(1 - int(target_field[1])): np.abs(1 - int(target_field[1])) + 8,
            7 - COLUMNS[target_field[0]]: 15 - COLUMNS[target_field[0]]]
    positions = np.transpose(np.nonzero(old_position[item_figure, :8, :]))

    if figure_type == 'N':  # поиск подходящего коня
        for pos in positions:
            if moves[pos[1], pos[2]] == 0:
                item_figure[pos[0]] = -1
        item_figure = item_figure[item_figure >= 0]
        return item_figure

    # если фигура не конь, то ишем так
    our_team_map = np.sum(old_position[old_position[:, 8, 6] == 1, :8, :], axis=0)
    enemy_team_map = np.sum(old_position[old_position[:, 8, 6] == 0, :8, :], axis=0)
    for pos in positions:
        fig_xy = pos[1], pos[2]
        field_xy = 8 - int(target_field[1]), COLUMNS[target_field[0]]
        our_slice = our_team_map[min(fig_xy[0], field_xy[0]):max(fig_xy[0], field_xy[0]) + 1,
                    min(fig_xy[1], field_xy[1]):max(fig_xy[1], field_xy[1]) + 1]
        enemy_slice = enemy_team_map[min(fig_xy[0], field_xy[0]):max(fig_xy[0], field_xy[0]) + 1,
                      min(fig_xy[1], field_xy[1]):max(fig_xy[1], field_xy[1]) + 1]

        # нсли между фигурой и полем нет прямой или диагонали, то фигура не подходит
        if our_slice.shape[0] != 1 and our_slice.shape[1] != 1 and our_slice.shape[0] != our_slice.shape[1]:
            item_figure[pos[0]] = -1
            continue

        if our_slice.shape[0] == 1 or our_slice.shape[1] == 1:  # если фигура и поле на одной прямой
            if not (np.sum(our_slice) == 1 and np.sum(enemy_slice) == 0) \
                    and not (np.sum(our_slice) == 1 and np.sum(enemy_slice) == 1
                             and moves[fig_xy[0], fig_xy[1]] == 1):
                item_figure[pos[0]] = -1
            elif figure_type == 'B':
                item_figure[pos[0]] = -1
        else:  # если между фигурой и полем диагональ
            # если диагональ не главная, то отразим срез
            if not (fig_xy[0] < field_xy[0] and fig_xy[1] < field_xy[1]) \
                    and not (fig_xy[0] > field_xy[0] and fig_xy[1] > field_xy[1]):
                our_slice = np.fliplr(our_slice)
                enemy_slice = np.fliplr(enemy_slice)
            if not (np.sum(np.trace(our_slice)) == 1 and np.sum(np.trace(enemy_slice)) == 0) \
                    and not (np.sum(np.trace(our_slice)) == 1 and np.sum(np.trace(enemy_slice)) == 1
                        and moves[fig_xy[0], fig_xy[1]] == 1):
                item_figure[pos[0]] = -1
            elif figure_type == 'R':
                item_figure[pos[0]] = -1
    item_figure = item_figure[item_figure >= 0]
    return item_figure
