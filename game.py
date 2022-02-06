import numpy as np
import re
from find_field import find_source_field


class Game:
    COLUMNS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    FIG_TYPES = {'K': 0, 'Q': 1, 'B': 2, 'N': 3, 'R': 4, 'P': 5}

    def __init__(self, game_string, position):
        self.game_string = game_string
        self.moves_list, self.result, self.is_checkmate = self.get_moves_and_results(game_string)
        self.positions_list = []
        self.positions_list.append(position)
        for move in self.moves_list:
            self.positions_list.append(self.get_next_position(move))

    def get_moves_and_results(self, game_string):
        moves_list = re.sub(r'\d*\.', '', game_string)
        moves_list = moves_list.replace('#', '')
        moves_list = moves_list.split()
        is_checkmate = True if '#' in game_string else False
        result = None
        if moves_list[-1] == '1-0' or moves_list[-1] == '0-1' or moves_list[-1] == '1/2-1/2':
            result = moves_list.pop(-1)
        return moves_list, result, is_checkmate

    def get_next_position(self, move):
        old_position = self.positions_list[-1]
        new_position = np.copy(old_position)
        if 'O-O' in move:  # если рокировка
            self.castling(old_position, new_position, move)
            new_position[:, 8, 6] = np.abs(new_position[:, 8, 6] - 1)
            return new_position
        move = move.replace('+', '')
        replaced_fig = None  # фигура, поставленная на доску вместо пешки
        if move[-2] == '=':
            replaced_fig = move[-1]
            move = move[:-2]
        figure_type = move[0] if move[0].isupper() else 'P'  # тип фигуры, которая двигилась
        move = move.replace(figure_type, '')
        target_field = move[-2:]  # поле, на которое стала фигура
        move = move.replace(target_field, '')
        is_capture = True if move.find('x') >= 0 else False  # было ли взятие
        move = move.replace('x', '')
        source_field = move  # исходное поле

        assert 0 <= len(source_field) <= 2, f"source_field={source_field}"
        if is_capture:
            self.drop_figure(old_position, new_position, target_field)
        if len(source_field) < 2:
            source_field = find_source_field(old_position, figure_type, target_field, source_field, is_capture)
        self.move_figure(old_position, new_position, source_field, target_field)
        if replaced_fig:  # замена пешки на фигуру
            item_fig = np.nonzero(new_position[:, 8 - int(target_field[1]), self.COLUMNS[target_field[0]]])[0]
            new_position[item_fig, 8, 0:6] = 0
            new_position[item_fig, 8, self.FIG_TYPES[replaced_fig]] = 1
        new_position[:, 8, 6] = np.abs(new_position[:, 8, 6] - 1)  # меняем фигурам право хода
        return new_position

    def castling(self, old_position, new_position, direction):
        if direction == 'O-O':
            who_move = np.nonzero(old_position[:, 8, 6])[0]
            if max(who_move) < 16:
                self.move_figure(old_position, new_position, 'e1', 'g1')
                self.move_figure(old_position, new_position, 'h1', 'f1')
            else:
                self.move_figure(old_position, new_position, 'e8', 'g8')
                self.move_figure(old_position, new_position, 'h8', 'f8')
        elif direction == 'O-O-O':
            who_move = np.nonzero(old_position[:, 8, 6])[0]
            if max(who_move) < 16:
                self.move_figure(old_position, new_position, 'e1', 'c1')
                self.move_figure(old_position, new_position, 'a1', 'd1')
            else:
                self.move_figure(old_position, new_position, 'e8', 'c8')
                self.move_figure(old_position, new_position, 'a8', 'd8')

    def move_figure(self, old_position, new_position, old_field, new_field):
        item_figure = np.nonzero(old_position[:, 8 - int(old_field[1]), self.COLUMNS[old_field[0]]])
        new_position[item_figure[0], 8 - int(old_field[1]), self.COLUMNS[old_field[0]]] = 0
        new_position[item_figure[0], 8 - int(new_field[1]), self.COLUMNS[new_field[0]]] = 1

    def drop_figure(self, old_position, new_position, target_field):
        # если там фигура есть
        item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]), self.COLUMNS[target_field[0]]])[0]
        if len(item_figure) == 1:
            new_position[item_figure[0], :, :] = 0
        elif len(item_figure) == 0:  # если нет, значит взятие на проходе
            if 8 - int(target_field[1]) == 2:  # значит белой пешкой бьем черную
                item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) + 1, self.COLUMNS[target_field[0]]])[0]
                new_position[item_figure, :, :] = 0
            elif 8 - int(target_field[1]) == 5:  # значит черной пешкой бьем белую
                item_figure = np.nonzero(old_position[:, 8 - int(target_field[1]) - 1, self.COLUMNS[target_field[0]]])[0]
                new_position[item_figure, :, :] = 0
