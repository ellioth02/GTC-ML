###############
# gather data #
###############
import os
import json
from enum import Enum
import numpy as np
from scipy.io import wavfile

from collect_data.__constants import ROOT_PATH, DATA_DST_PATH, META_PATH

# represents the data from one recording session
class __BaseDataSet:
    def __init__(self, name: str, id: int) -> None:
        # save name and id
        self.name = name
        self.id = str(id)
        # compute the different paths used by the dataset
        self.data_path = os.path.join(ROOT_PATH, self.name, "data/")
        self.datalist_path = os.path.join(META_PATH, self.name + "-datalist.json")

# specifies which half of audio to copy
class __Half(Enum):
    BOTH = 0
    HEAD = 1
    TAIL = 2

# sampling rate of audio
__SAMPLE_RATE = 16_000

# functions
def gather_data() -> None:
    datasets = [__BaseDataSet("23-12-04", 0), __BaseDataSet("23-12-08", 1)]
    for ds in datasets:
        __collect_dataset(ds)

def __collect_dataset(dataset: __BaseDataSet) -> None:
    # collect data lists
    good, half_head_good, half_tail_good = __get_datalist(dataset)
    # copy halfs
    __collect_from_data_list(dataset, good, __Half.BOTH)
    __collect_from_data_list(dataset, half_head_good, __Half.HEAD)
    __collect_from_data_list(dataset, half_tail_good, __Half.TAIL)


def __get_datalist(dataset: __BaseDataSet) -> ([str], [str], [str]):
    # collect data list
    f = open(dataset.datalist_path, "r")
    data_list = json.load(f)
    f.close()
    good = data_list["good"]
    half_head_good = data_list["half_head_good"]
    half_tail_good = data_list["half_tail_good"]
    return (good, half_head_good, half_tail_good)


def __collect_from_data_list(dataset: __BaseDataSet, list: [str], half: __Half) -> None:
    # copy all file halfs specified in the list to GTC/dataset/audio/
    for name in list:
        __copy_half_wave(dataset, name, half)

def __copy_half_wave(dataset: __BaseDataSet, name: str, half: __Half) -> None:
    # load raw data
    data_path = os.path.join(dataset.data_path, name + ".npy")
    raw_data = np.load(data_path)
    # split audio at half point
    half_point = len(raw_data) // 2
    head = raw_data[:half_point]
    tail = raw_data[half_point:]
    # compute desitination for the wave files
    new_name = dataset.id + "_" + name
    dst_head = os.path.join(DATA_DST_PATH, new_name + "_1.wav")
    dst_tail = os.path.join(DATA_DST_PATH, new_name + "_2.wav")
    # save halfs as wave
    if half == __Half.HEAD:
        # save first 5s of file
        wavfile.write(dst_head, __SAMPLE_RATE, head)
    elif half == __Half.TAIL:
        # save last 5s of file
        wavfile.write(dst_tail, __SAMPLE_RATE, tail)
    else:
        # save first and last 5s of file as two files
        wavfile.write(dst_head, __SAMPLE_RATE, head)
        wavfile.write(dst_tail, __SAMPLE_RATE, tail)
