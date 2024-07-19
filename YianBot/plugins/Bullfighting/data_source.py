import os
from random import choices, randint, sample
import cv2
import numpy as np
from itertools import combinations


def get_card():
    path = "src\\card\\"
    names = choices(os.listdir(path), 5)
    image_list = []
    for name in names:
        image_list.append(cv2.imread(path + name))

    blank = [
        np.ones((190, 67, 3), dtype=np.uint8) * 255,
        np.ones((190, 1, 3), dtype=np.uint8) * 255,
        np.ones((190, 67, 3), dtype=np.uint8) * 255
    ]
    image1 = np.concatenate([blank[0], image_list[0], blank[1], image_list[1], blank[2]], axis=1)
    image2 = np.concatenate([image_list[2], image_list[3], image_list[4]], axis=1)
    image = np.vstack((image1, image2))

    to_path = f"src\\temp\\{randint(1, 1000)}.png"
    cv2.imwrite(to_path, image)
    return os.path.abspath(to_path)


def concatenate_images(image_names):
    """
    将10张图片拼接成两排显示，每排5张。

    :param image_names: 包含10个图像文件名的列表。
    :return: 拼接后图像的绝对路径。
    """

    path = os.path.join("src", "card")  # 图片存放的目录
    image_list = [cv2.imread(os.path.join(path, name)) for name in image_names]

    # 分别拼接上下两排图片
    image_top_row = np.concatenate(image_list[:5], axis=1)
    image_bottom_row = np.concatenate(image_list[5:], axis=1)

    # 将两排图片垂直拼接
    image_concatenated = np.vstack((image_top_row, image_bottom_row))

    # 保存拼接后的图片
    to_path = os.path.join("src", "temp", f"{randint(1, 999)}.png")
    cv2.imwrite(to_path, image_concatenated)

    return os.path.abspath(to_path)


def get_random_filenames(path="src\\card\\", num_files=10):
    """
    从指定目录中随机选取指定数量的不重复文件名。

    :param path: 目录路径
    :param num_files: 需要选取的文件数量，默认为10
    :return: 选取的文件名列表
    """
    # 列出目录中的所有文件
    all_filenames = os.listdir(path)

    # 随机选取指定数量的不重复文件名
    selected_filenames = sample(all_filenames, num_files)

    return selected_filenames


def card_value_from_filename(filename):
    """
    从文件名中提取牌的数值。
    """
    value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10,
                 'A': 1, 'joker': 10}
    # 提取牌面（去除花色和.png后缀）
    card_face = filename.split('_')[1].replace('.png', '')
    # 返回牌的数值
    return value_map[card_face]


def check_bull(cards):
    """
    检查五张牌中是否有牛，并返回结果。
    """
    cards_values = [card_value_from_filename(card) for card in cards]
    for combo in combinations(cards_values, 3):
        if sum(combo) % 10 == 0:
            remaining_cards = cards_values.copy()
            for card in combo:
                remaining_cards.remove(card)
            bull_size = sum(remaining_cards) % 10
            return 10 if bull_size == 0 else bull_size
    return 0


def calculate_bull_for_two_groups(cards):
    """
    计算前五个和后五个的牛数，并返回一个元组。
    """
    # 分别计算前五个和后五个的牛数
    bull_first_group = check_bull(cards[:5])
    bull_second_group = check_bull(cards[5:])
    return (bull_first_group, bull_second_group)
