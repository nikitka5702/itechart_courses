import os
from multiprocessing import Pool

import cv2
import numpy as np


WORK_DIR = 'i_img'
SAVE_DIR = 'i_border_img'

def add_border(file):
    print(f'Working on {file}')
    image = cv2.imread(os.path.join(WORK_DIR, file), cv2.IMREAD_UNCHANGED)
    cv2.imwrite(
        os.path.join(SAVE_DIR, file),
        cv2.rectangle(image, (1, 11), (62, 52), (0, 0, 0, 255), 1)
    )


if __name__ == '__main__':
    with Pool(32) as p:
        p.map(add_border, os.listdir(WORK_DIR))
