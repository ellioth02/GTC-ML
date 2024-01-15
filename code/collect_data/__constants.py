import os

# describes the different categories of sounds to be identified
CATEGORY = {"sticker_on": 0, "sticker_on_compressor": 1, "sticker_off": 2, "sticker_off_compressor": 3, "background": 4}

# file paths
__FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(__FILE_PATH, "..", "..")
RAW_DATA_PATH = os.path.join(ROOT_PATH, "dataset", "raw")
USED_DATA_PATH = os.path.join(ROOT_PATH, "dataset", "used")
META_PATH = os.path.join(USED_DATA_PATH, "meta")
# data raw recordings
DATA_DST_PATH = os.path.join(USED_DATA_PATH, "audio")
