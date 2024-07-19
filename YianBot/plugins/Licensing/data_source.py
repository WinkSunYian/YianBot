import os
from random import choices, randint
import cv2
import numpy as np


def get_card(k):
    path = "src\\card\\"
    names = choices(os.listdir(path), k=k)
    image_list = []
    for name in names:
        image_list.append(cv2.imread(path + name))

    if k == 4:
        image1 = np.concatenate([image_list[0], image_list[1]], axis=1)
        image2 = np.concatenate([image_list[2], image_list[3]], axis=1)
        image = np.vstack((image1, image2))
    elif k == 5:
        blank = [
            np.ones((190, 67, 3), dtype=np.uint8) * 255,
            np.ones((190, 1, 3), dtype=np.uint8) * 255,
            np.ones((190, 67, 3), dtype=np.uint8) * 255
        ]
        image1 = np.concatenate([blank[0], image_list[0], blank[1], image_list[1], blank[2]], axis=1)
        image2 = np.concatenate([image_list[2], image_list[3], image_list[4]], axis=1)
        image = np.vstack((image1, image2))
    elif k == 6:
        image1 = np.concatenate([image_list[0], image_list[1], image_list[2]], axis=1)
        image2 = np.concatenate([image_list[3], image_list[4], image_list[5]], axis=1)
        image = np.vstack((image1, image2))
    else:
        image = np.concatenate(image_list, axis=1)

    to_path = f"src\\temp\\{randint(1, 1000)}.png"
    cv2.imwrite(to_path, image)
    return os.path.abspath(to_path)
