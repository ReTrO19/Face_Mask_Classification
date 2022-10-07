from shutil import copyfile
import os
from tqdm import tqdm
import random

def split_data(SOURCE, TRAINING, TESTING, SPLIT_SIZE):
    files = []
    
    for filename in tqdm(os.listdir(SOURCE),desc="Verifying Images"):
        file = SOURCE + filename
        if os.path.getsize(file) > 0:
            files.append(filename)
        else:
            print(filename + " is zero length, so ignoring.")
    print("Verification Complete")

    training_length = int(len(files) * SPLIT_SIZE)
    testing_length = int(len(files) - training_length)
    shuffled_set = random.sample(files, len(files))
    training_set = shuffled_set[0:training_length]
    testing_set = shuffled_set[training_length:]

    for filename in tqdm(training_set,desc="Processing Training Images"):
        this_file = SOURCE + filename
        destination = TRAINING + filename
        copyfile(this_file, destination)

    for filename in tqdm(testing_set,desc="Processing Testing Images"):
        this_file = SOURCE + filename
        destination = TESTING + filename
        copyfile(this_file, destination)

def create_req_folder(root_folder):
    try:
        os.mkdir(os.path.join(root_folder,'MaskNoMaskDS'))
        os.mkdir(os.path.join(root_folder,'MaskNoMaskDS\\training'))
        os.mkdir(os.path.join(root_folder,'MaskNoMaskDS\\testing'))
        os.mkdir(os.path.join(root_folder,'MaskNoMaskDS\\training\\with_mask'))
        os.mkdir(os.path.join(root_folder,'MaskNoMaskDS\\training\\without_mask'))
        os.mkdir(os.path.join(root_folder,'MaskNoMaskDS\\testing\\with_mask'))
        os.mkdir(os.path.join(root_folder,'MaskNoMaskDS\\testing\\without_mask'))
    except OSError:
        pass


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Input values for the split_data function')
    parser.add_argument('--root_folder','-rf',type=bool,help='Pass Root path to the project ',required=True)
    args = parser.parse_args()



    SPLIT_SIZE = 0.9
    WITH_MASK_SOURCE_DIR = os.path.join(args.root_folder,"data\\with_mask\\")
    TRAINING_WITH_MASK_DIR = os.path.join(args.root_folder,"MaskNoMaskDS\\training\\with_mask\\")
    TESTING_WITH_MASK_DIR = os.path.join(args.root_folder,"MaskNoMaskDS\\testing\\with_mask\\")
    WITHOUT_MASK_SOURCE_DIR = os.path.join(args.root_folder,"data\\without_mask\\")
    TRAINING_WITHOUT_MASK_DIR = os.path.join(args.root_folder,"MaskNoMaskDS\\training\\without_mask\\")
    TESTING_WITHOUT_MASK_DIR = os.path.join(args.root_folder,"MaskNoMaskDS\\testing\\without_mask\\")
    create_req_folder(args.root_folder)
    split_data(WITH_MASK_SOURCE_DIR, TRAINING_WITH_MASK_DIR, TESTING_WITH_MASK_DIR, SPLIT_SIZE)
    split_data(WITHOUT_MASK_SOURCE_DIR, TRAINING_WITHOUT_MASK_DIR, TESTING_WITHOUT_MASK_DIR, SPLIT_SIZE)