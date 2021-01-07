# -*- coding: utf-8 -*-
# author: pinakinathc

import glob
import os
import json
import numpy as np

if __name__ == '__main__':

    ''' Get all the URL of images we want to annotate '''
    url_list = [".\\images\\00000.jpg",
    ".\\images\\00110.jpg",
    ".\\images\\00130.jpg",
    ".\\images\\00155.jpg"]
    np.random.shuffle(url_list)

    user_list = ['17', '19'] # Add all unique user IDs you want.
    user_len = len(user_list)
    N = len(url_list) // len(user_list)

    all_data = {'users': {}}
    for idx, user in enumerate(user_list):
        all_data['users'][user] = []
        all_data[user] = {}

        for image_url in url_list[N*idx: N*(idx+1)]: # Each user is assigned N Images
            all_data['users'][user].append(image_url)

    with open('all_data_skeleton.json', 'w') as fp:
        json.dump(all_data, fp)

