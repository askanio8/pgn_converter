import numpy as np


start_position = np.zeros((32, 9, 8), dtype=int)

start_position[0, 8, 4] = 1; start_position[0, 7, 0] = 1; start_position[0, 8, 6] = 1  # белая ладья, a1, ход белых
start_position[1, 8, 3] = 1; start_position[1, 7, 1] = 1; start_position[1, 8, 6] = 1  # белый конь, b1, ход белых
start_position[2, 8, 2] = 1; start_position[2, 7, 2] = 1; start_position[2, 8, 6] = 1  # белый слон, c1, ход белых
start_position[3, 8, 1] = 1; start_position[3, 7, 3] = 1; start_position[3, 8, 6] = 1  # белый ферзь, d1, ход белых
start_position[4, 8, 0] = 1; start_position[4, 7, 4] = 1; start_position[4, 8, 6] = 1  # белый король, e1, ход белых
start_position[5, 8, 2] = 1; start_position[5, 7, 5] = 1; start_position[5, 8, 6] = 1  # белый слон, f1, ход белых
start_position[6, 8, 3] = 1; start_position[6, 7, 6] = 1; start_position[6, 8, 6] = 1  # белый конь, g1, ход белых
start_position[7, 8, 4] = 1; start_position[7, 7, 7] = 1; start_position[7, 8, 6] = 1  # белая ладья, h1, ход белых

start_position[8, 8, 5] = 1; start_position[8, 6, 0] = 1; start_position[8, 8, 6] = 1  # белая пешка, a2, ход белых
start_position[9, 8, 5] = 1; start_position[9, 6, 1] = 1; start_position[9, 8, 6] = 1  # белая пешка, b2, ход белых
start_position[10, 8, 5] = 1; start_position[10, 6, 2] = 1; start_position[10, 8, 6] = 1  # белая пешка, c2, ход белых
start_position[11, 8, 5] = 1; start_position[11, 6, 3] = 1; start_position[11, 8, 6] = 1  # белая пешка, d2, ход белых
start_position[12, 8, 5] = 1; start_position[12, 6, 4] = 1; start_position[12, 8, 6] = 1  # белая пешка, e2, ход белых
start_position[13, 8, 5] = 1; start_position[13, 6, 5] = 1; start_position[13, 8, 6] = 1  # белая пешка, f2, ход белых
start_position[14, 8, 5] = 1; start_position[14, 6, 6] = 1; start_position[14, 8, 6] = 1  # белая пешка, g2, ход белых
start_position[15, 8, 5] = 1; start_position[15, 6, 7] = 1; start_position[15, 8, 6] = 1  # белая пешка, h2, ход белых

start_position[16, 8, 4] = 1; start_position[16, 0, 0] = 1  # черная ладья, a8
start_position[17, 8, 3] = 1; start_position[17, 0, 1] = 1  # черный конь, b8
start_position[18, 8, 2] = 1; start_position[18, 0, 2] = 1  # черный слон, c8
start_position[19, 8, 1] = 1; start_position[19, 0, 3] = 1  # черный ферзь, d8
start_position[20, 8, 0] = 1; start_position[20, 0, 4] = 1  # черный король, e8
start_position[21, 8, 2] = 1; start_position[21, 0, 5] = 1  # черный слон, f8
start_position[22, 8, 3] = 1; start_position[22, 0, 6] = 1  # черный конь, g8
start_position[23, 8, 4] = 1; start_position[23, 0, 7] = 1  # черная ладья, h8

start_position[24, 8, 5] = 1; start_position[24, 1, 0] = 1  # черная пешка, a7
start_position[25, 8, 5] = 1; start_position[25, 1, 1] = 1  # черная пешка, b7
start_position[26, 8, 5] = 1; start_position[26, 1, 2] = 1  # черная пешка, c7
start_position[27, 8, 5] = 1; start_position[27, 1, 3] = 1  # черная пешка, d7
start_position[28, 8, 5] = 1; start_position[28, 1, 4] = 1  # черная пешка, e7
start_position[29, 8, 5] = 1; start_position[29, 1, 5] = 1  # черная пешка, f7
start_position[30, 8, 5] = 1; start_position[30, 1, 6] = 1  # черная пешка, g7
start_position[31, 8, 5] = 1; start_position[31, 1, 7] = 1  # черная пешка, h7

start_position[:, 8, 7] = 1  # эти фигуры на доске
