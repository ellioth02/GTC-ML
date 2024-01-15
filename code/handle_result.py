import time
import os

# constants
__CONFIDENCE_THRESHOLD = 0.7

# functions
# check machine state
def check_machine(category: str, confidence: float) -> None:
    if __is_sticker_off(category) and __is_confident(confidence):
        # the proccess is not working correctly,
        # and the confindence is sufficently large
        # now, raise the alarm
        __print_machine_error()
    else:
        __clear_screen()

def __is_sticker_off(category: str) -> bool:
    return "sticker_off" in category

def __is_confident(confidence: int) -> bool:
    return confidence >= __CONFIDENCE_THRESHOLD

def __print_machine_error() -> None:
    print("###############################")
    print("# W A R N I N G               #")
    print("#", __get_time_str(), "  #")
    print("###############################")
    print("| The sticker is off!         |")
    print("| Resolve immediately!        |")
    print("-------------------------------\n\n")

def __clear_screen():
        # clear screen
        os.system("clear" if os.name == "posix" else "cls")

def __get_time_str() -> str:
    return time.strftime("[%a %Y-%m-%d] %H:%M:%S", time.localtime())
