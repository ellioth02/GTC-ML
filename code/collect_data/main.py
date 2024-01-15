import sys
import os

# fix current dir imports
__SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__SCRIPT_DIR))

# import from this package
from collect_data.__gather_data import gather_data
from collect_data.__generate_metadata import create_metadata

# functions
def main(args):
    if len(args) == 0:
        # program is running in cli mode
        # print cli
        print("Collect Data for ML tranning of GTC Model")
        print("=========================================")
        while True:
            print("What would you like to do?")
            print("\t1. Collect data from the different recording sessions")
            print("\t2. Create metadata for Model")
            print("\t3. Both of the above")
            print("\t0. Exit")
            # get input and compute selected operation
            choice = input("> ")
            if choice.isdecimal():
                # convert to int
                choice = int(choice)
                if match_user_choice(choice):
                    # if user input matched, stop invalid input loop
                    break
            # an error has occurred
            print("Invalid Input! Try Again!\n")
    else:
        # program is running in argument mode
        if args[0].isdecimal():
            choice = int(args[0])
            if match_user_choice(choice):
                # everthing worked, return
                return
        # an error occurred, print error
        print("ERROR: Illegal Arguments!")
        exit(-1)


# run user specified operation by matching the user input with right operations
def match_user_choice(choice: int) -> bool:
    # switch case
    if choice == 1:
        print("Collecting data...")
        gather_data()
        return True
    elif choice == 2:
        print("Creating metadata...")
        create_metadata()
        return True
    elif choice == 3:
        print("Collecting data...")
        gather_data()
        print("Creating metadata...")
        create_metadata()
        return True
    elif choice == 0:
        print("Exiting...")
        return True
    # no match
    return False

# Entry Point
if __name__ == "__main__":
    # run main function with all arguments except "python file.py"
    main(sys.argv[1:])
