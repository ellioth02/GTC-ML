# debug print
print("Loading libraries...")

# import dependencies
import sys
from time import time
import tensorflow as tf
from audio_recorder import Recorder
from audio_classifier import Analyzer
from handle_result import check_machine

# suppress tensorflow warnings
tf.get_logger().setLevel("ERROR")

# functions
def main(args):
    testing = False
    # parse command arguments
    if len(args) != 0:
        # test argument
        if args[0] == "test":
            testing = True
            print("Running in test mode")
    # create ML analyzer
    print("Loading GTC ML Model...")
    model = Analyzer(verbose = testing, load_YAMNet = False)
    print("GTC ML Model has been loaded")
    # create recording microphone
    microphone = Recorder()
    # check when to start machine supervision
    __check_start()
    # start mic
    microphone.start()
    print("Recording...")
    while True:
        # load audio
        waveform = microphone()
        # analyze
        category, confidence = model.analyze_audio(waveform)
        # do not take action, if testing
        if testing:
            continue
        # take action
        check_machine(category, confidence)

# print msg before running a function and then print the time it took
def __timed_operation(func, msg: str) -> None:
    # print descriptive text
    print(msg, end = None)
    start_time = time()
    func()
    end_time = time()
    delay = end_time - start_time
    print(f"[{delay} s]")

def __check_start() -> None:
    choice = ""
    while choice != "yes" and choice != "y":
        choice = input("Start (yes)? ")

# Entry point
if __name__ == "__main__":
    main(sys.argv[1:])
