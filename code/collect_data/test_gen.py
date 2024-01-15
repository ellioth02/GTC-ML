import os
import sys
import random
from collections import Counter
import statistics

# fix current dir imports
__SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__SCRIPT_DIR))

# import from this package
from collect_data.__generate_metadata import fold_gen

def main():
    for _ in range(10000):
        length = random.randrange(10, 10_000)
        fold_test(length)
    print("All tests passed! :)")

def fold_test(length: int, verbose: bool = False):
    # generate folds
    gen = fold_gen(length)
    fold_values = [fold for fold in gen]
    # calculate stats
    total_fold_count = len(fold_values)
    folds = Counter(fold_values).items()
    different_folds = len(folds)
    deviation = statistics.stdev([count for _, count in folds])
    # check values
    same_len_of_different_folds = different_folds == 5
    fold_value_for_every_item = total_fold_count == length
    # evaluate
    conditions = [same_len_of_different_folds, fold_value_for_every_item]
    test_passed = all(conditions)
    # if test did not pass always show output
    if not test_passed:
        verbose = True
    # test case shown
    if verbose:
        print("FOLD TEST: length = ", length)
        print("##############################")
        # stats
        print("Stats:")
        print("folds: ", folds)
        print("deviation: ", deviation)
        print("different_folds: ", different_folds)
        print("total_fold_count: ", total_fold_count)
        # checks
        print("Checks:")
        print("different_folds == 5: ", same_len_of_different_folds)
        print("total_fold_count == length: ", fold_value_for_every_item)
        print("------------------------------\n\n")
    # if test did not pass, terminate
    if not test_passed:
        print("WARNING: Test did not pass!")
        exit(-1)


if __name__ == "__main__":
    main()
