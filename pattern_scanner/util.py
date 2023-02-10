import numpy as np


def get_crosspt(x11, y11, x12, y12, x21, y21, x22, y22):   #교점 찾기
    if x12==x11 or x22==x21:
        return np.nan, np.nan
    m1 = (y12 - y11) / (x12 - x11)
    m2 = (y22 - y21) / (x22 - x21)
    if m1==m2:
        return np.nan, np.nan
    cx = (x11 * m1 - y11 - x21 * m2 + y21) / (m1 - m2)
    cy = m1 * (cx - x11) + y11
    return cx, cy