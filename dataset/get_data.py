'''
Pull named entity recognition (NER) tasks dataset.
Dataset list available at following github link:
    https://github.com/juand-r/entity-recognition-datasets
'''

import argparse
import shutil
import tqdm
import requests
import os
import os.path as osp
import urllib.request
import pandas as pd

def fetchFileFromLink(link, savepath, overwrite=True):
    if not osp.exists(savepath):
        os.makedirs(savepath)

    filename = osp.join(savepath, osp.basename(link))
    if osp.exists(filename) and not overwrite:
        print('File {} exists'.format(filename))
        return

    response = requests.get(link, stream=True)
    with open(filename, "wb") as handle:
        for data in tqdm.tqdm(response.iter_content()):
            handle.write(data)
    print('File {} downloaded'.format(filename))


def getDatasetLinkFromName(name):
    if name.lower() in ['mitmovie', 'mitrestaurant']:
        train_link = 'https://groups.csail.mit.edu/sls/downloads/movie/trivia10k13train.bio'
        test_link = 'https://groups.csail.mit.edu/sls/downloads/movie/trivia10k13test.bio'
        return train_link, test_link

    elif name.lower() in ['wikineural']:
        train_link = 'https://github.com/Babelscape/wikineural/blob/master/data/wikineural/en/train.conllu'
        test_link = 'https://github.com/Babelscape/wikineural/blob/master/data/wikineural/en/test.conllu'
        return train_link, test_link


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download dataset')
    parser.add_argument('-n','--name', help='Dataset name', required=True)
    parser.add_argument('-d','--save_dir', help='Dataset save directory', required=True)
    parser.add_argument('-o','--overwrite', help='Overwrite existing dataset', required=False, default=False)
    args = parser.parse_args()

    # get the dataset links
    train_link, test_link = getDatasetLinkFromName(args.name)

    # download dataset
    fetchFileFromLink(train_link, args.save_dir, args.overwrite)
    fetchFileFromLink(test_link, args.save_dir, args.overwrite)
