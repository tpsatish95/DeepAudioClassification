# -*- coding: utf-8 -*-
import argparse
import os
import random
import string
import sys
from config import (batchSize, filesPerGenre, nbEpoch, sliceSize, slicesPath,
                    testRatio, validationRatio)

import numpy as np

from datasetTools import getDataset
from model import createModelCifar
from songToData import createSlicesFromAudio

parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains or tests the CNN",
                    nargs='+', choices=["train", "test", "slice"])
args = parser.parse_args()

print("--------------------------")
print("| ** Config ** ")
print(("| Validation ratio: {}".format(validationRatio)))
print(("| Test ratio: {}".format(testRatio)))
print(("| Slices per genre: {}".format(filesPerGenre)))
print(("| Slice size: {}".format(sliceSize)))
print("--------------------------")

if "slice" in args.mode:
    createSlicesFromAudio()
    sys.exit()

# List genres
genres = os.listdir(slicesPath)
genres = [filename for filename in genres if os.path.isdir(slicesPath + filename)]
nbClasses = len(genres)

# Create model
model = createModelCifar(nbClasses, sliceSize)

if "train" in args.mode:

    # Create or load new dataset
    train_X, train_y, validation_X, validation_y = getDataset(
        filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="train")

    # Define run id for graphs
    run_id = "MusicGenres - " + \
        str(batchSize) + " " + ''.join(random.SystemRandom().choice(string.ascii_uppercase)
                                       for _ in range(10))

    # Train the model
    print("[+] Training the model...")
    model.fit(train_X, train_y, n_epoch=nbEpoch, batch_size=batchSize, shuffle=True, validation_set=(
        validation_X, validation_y), snapshot_step=100, show_metric=True, snapshot_epoch=True, run_id=run_id)
    print("    Model trained! ✅")

    # Save trained model
    print("[+] Saving the weights...")
    model.save('musicDNN.tflearn')
    print("[+] Weights saved! ✅💾")

if "test" in args.mode:

    # Create or load new dataset
    test_X, test_y = getDataset(filesPerGenre, genres, sliceSize,
                                validationRatio, testRatio, mode="test")

    # Load weights
    print("[+] Loading weights...")
    model.load(os.getcwd() + '/model/model.tfl.cifar-100')
    print("    Weights loaded! ✅")

    testAccuracy = model.evaluate(test_X, test_y)[0]
    print(("[+] Test accuracy: {} ".format(testAccuracy)))
