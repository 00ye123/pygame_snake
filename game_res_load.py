import json
import os
import pygame


def load_scenes(base_dir):
    """
    从目标文件夹中加载所有json文件,返回一个列表。每隔列表表示一个json文件
    """
    # print(f'当前程序路径：{base_dir}')
    level_dir = os.path.join(base_dir, 'data/json')
    scenes = []
    for filename in sorted(os.listdir(level_dir)):
        if filename.endswith('.json'):
            path = os.path.join(level_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                scenes.append(data)
    return scenes


if __name__ == '__main__':
    l = load_scenes(os.path.dirname(__file__))
    print(l[1]['new'])