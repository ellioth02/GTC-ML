#####################
# generate metadata #
#####################
import os
import random
import math
from typing import Generator
import pandas as pd

from collect_data.__constants import META_PATH, DATA_DST_PATH, CATEGORY

# dataset metadata
__DATASET_CLASS_MAP_PATH = os.path.join(META_PATH, "class_map.csv")
__DATASET_CSV_PATH = os.path.join(META_PATH, "gtc.csv")

# functions
def create_metadata() -> None:
    __create_class_map_csv()
    __create_dataset_csv()

def __create_class_map_csv() -> None:
    # create empty table with columns
    table = {"id": [], "category": []}
    # fill in table
    for category, id in CATEGORY.items():
        table["id"].append(id)
        table["category"].append(category)
    # create csv file
    date_frame = pd.DataFrame(data=table)
    date_frame.to_csv(__DATASET_CLASS_MAP_PATH, index=False)

def __create_dataset_csv() -> None:
    # create empty table with columns
    table = {"filename": [], "fold": [], "target": [], "category": []}
    # fill in table
    # load list of data files (.wav) in random order
    waveforms = list(filter(lambda f: f.endswith(".wav"), os.listdir(DATA_DST_PATH)))
    random.shuffle(waveforms)
    # create folds generator
    folds = fold_gen(len(waveforms))
    # add each wave file to the dataset
    for file in waveforms:
        __add_file_to_dataset(table, folds, file)
    # create csv file
    date_frame = pd.DataFrame(data=table)
    date_frame.to_csv(__DATASET_CSV_PATH, index=False)

# add file to the table with all columns filled in
def __add_file_to_dataset(table: dict, folds: Generator[int, int, None], file: str) -> None:
    # compute all column values
    filename = file
    fold = next(folds)
    target, category = __file_target_and_category(file)
    # create row and add it to the table
    row = dict(filename = filename, fold = fold, target = target, category = category)
    __table_append_row(table, row)

# append a row to the table
def __table_append_row(table: dict, row: dict) -> None:
    for column, column_list in table.items():
        column_list.append(row[column])

# find the category and target from the file name
def __file_target_and_category(file: str) -> (int, str):
    if "P_" in file:
        name = "sticker_on"
    elif "PK_" in file:
        name = "sticker_on_compressor"
    elif "A_" in file:
        name = "sticker_off"
    elif "AK_" in file:
        name = "sticker_off_compressor"
    else:
        name = "background"
    return (CATEGORY[name], name)

# generator for the fold values
def fold_gen(dataset_length: int) -> int:
    # generator state
    FOLDS = 5
    fold = 1
    counter = 0
    # find fold size
    frac = dataset_length / FOLDS
    fold_size = [math.ceil(frac), math.floor(frac)]
    folds_not_equal = fold_size[0] != fold_size[1]
    # find folds with smallest mean deviation:
    # index gives the index where the folds change size
    # index * fold_size[0] + (FOLDS - index) * fold_size[1] = dataset_length =>
    # => index = (dataset_length - FOLDS * fold_size[1]) / (fold_size[0] - fold_size[1])
    if folds_not_equal:
        index = (dataset_length - FOLDS * fold_size[1]) // (fold_size[0] - fold_size[1])
    f = 0
    # generate folds
    while fold <= FOLDS:
        counter += 1
        yield fold
        if counter == fold_size[f]:
            counter = 0
            fold += 1
            if folds_not_equal and fold == index + 1:
                f += 1
