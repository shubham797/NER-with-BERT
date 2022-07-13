import argparse
import shutil
import tqdm
import requests
import os
import os.path as osp
import numpy as np
import urllib.request
import pandas as pd

def analyze(data):
    print('Data analyze\n',data.count(),'\n')

    print("Number of tags: {}".format(len(data.Tag.unique())))
    frequencies = data.Tag.value_counts()
    print(frequencies)

    ## compute frequencies when same tokens begining and end are merged
    tags = {}
    for tag, count in zip(frequencies.index, frequencies):
        if tag != "O":
            if tag[2:] not in tags.keys():
                tags[tag[2:]] = count
            else:
                tags[tag[2:]] += count
        continue

    print(sorted(tags.items(), key=lambda x: x[1], reverse=True))

    # remove cases with tags whose occurence is less than 1000
    comb_entities_to_remove = []
    for k, v in tags.items():
        if v < 1000:
            comb_entities_to_remove.append(k)

    entities_to_remove = []
    for ent in comb_entities_to_remove:
        entities_to_remove.append('B-'+ent)
        entities_to_remove.append('I-'+ent)

    print(entities_to_remove)

def obtain_sentences(data):
    # create new column
    data["sentence"] = np.nan

    sen_mark = True
    sen_cnt = 1
    for it in range(len(data)):
        if pd.isna(data.iloc[it, 0]) and pd.isna(data.iloc[it, 1]):
            sen_cnt += 1
            sen_mark = True
            continue

        if sen_mark:
            data.iloc[it, 2] = sen_cnt
            sen_mark = False

    return data

def load_data(args):
    train_file = osp.join(args.data_dir, args.train_file)
    test_file = osp.join(args.data_dir, args.test_file)

    data = pd.read_csv(train_file, encoding='unicode_escape', sep='\t', names=['Tag', 'Word'], skip_blank_lines=False)
    data = obtain_sentences(data)
    data = analyze(data)

    # data = pd.read_csv(test_file, encoding='unicode_escape', sep='\t', names=['Tag', 'Word'], skip_blank_lines=False)
    # data = obtain_sentences(data)
    # data = analyze(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download dataset')
    parser.add_argument('-d','--data_dir', help='Dataset directory', required=True)
    parser.add_argument('-trf','--train_file', help='Train file name', required=True)
    parser.add_argument('-tsf','--test_file', help='Test file name', required=True)
    parser.add_argument('-o','--overwrite', help='Overwrite existing dataset', required=False, default=False)
    args = parser.parse_args()

    # load data for pre-processing
    load_data(args)

    # python preprocess.py -d "./dataset_folder/" -trf "trivia10k13train.bio" -tsf "trivia10k13test.bio"
