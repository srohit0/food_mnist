#!/usr/bin/env python

# Author: 
#   Rohit Sharma (srohit0.github.io)
#
# Date: 
#   June 15, 2019
#
# Description:
#   This script creates smaller dataset out of food-101 dataset available at 
#   http://data.vision.ee.ethz.ch/cvl/food-101.tar.gz
#
#   Download and untar the dataset in current directory before using this script.
#       % curl http://data.vision.ee.ethz.ch/cvl/food-101.tar.gz
#       % tar xvz food-101.tar.gz

import os, sys, errno, shutil
import json

nClasses = 10

dsSrc  = 'food-101'
dsDest = 'food-' + str(nClasses)

def mkdir_p(path):
    try:
        os.mkdir(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# Write 
#    1. class file, 
#    2. label text file 
#    3. label json file 
#    4. copy images
def writeDatasetFiles(dsSrc, dsDest, metaTag, classes):

    print "Writing " + str(nClasses) + " " + metaTag + " classes.";

    dsDestLableFile  = dsDest + "/meta/" + metaTag + ".txt"
    dsDestClassFile = dsDest + "/meta/classes.txt"
    with open(dsDestLableFile, 'w') as dlf, open(dsDestClassFile, 'w') as dcf:
        for cls in sorted(classes.keys()):
            # write class
            dcf.write(cls+"\n");
            for lbl in classes[cls]:
                # write label
                dlf.write(cls+"/"+lbl+"\n");

                # copy image
                mkdir_p(dsDest+"/images/"+cls)
                imageFile = "/images/" + cls + "/" + lbl + ".jpg"
                shutil.copy2(dsSrc+imageFile, dsDest+imageFile)

    # Write Json file
    dsDestJsonFile  = dsDest + "/meta/" + metaTag + ".json"
    with open(dsDestJsonFile, 'w') as djf:
        json.dump(classes, djf)

    return;

def createNewDataset(dsSrc, dsDest, training_classes, test_classes):
    mkdir_p(dsDest);
    shutil.copy2(dsSrc+"/license_agreement.txt", dsDest+"/license_agreement.txt")
    shutil.copy2(dsSrc+"/README.txt", dsDest+"/README.txt")
    mkdir_p(dsDest + str("/images"));
    mkdir_p(dsDest + str("/meta"));

    writeDatasetFiles(dsSrc, dsDest, "train", training_classes)

    writeDatasetFiles(dsSrc, dsDest, "test", test_classes)


def genLabels(labelFile, newLabelFile, nClasses, nSamplesPerClass):

    classes = {}
    with open(labelFile) as f:
        content = [x.strip() for x in f.readlines()]

    iClass = 0
    iSamples = 1
    for label in content: 
        cls, lbl = os.path.split(label)

        if ( classes.has_key(cls) and iSamples >= nSamplesPerClass ):
            continue;

        if classes.has_key(cls):
            classes[cls].append(lbl);
            iSamples = iSamples + 1
        else:
            classes[cls] = [lbl]
            iClass   = iClass + 1
            iSamples = 1

        if ( iClass >= nClasses and iSamples >= nSamplesPerClass):
            break 

    return classes

def parseClasses(dsSrc, dsDest):

    training_classes = genLabels(
                        dsSrc  + str("/meta/train.txt"),
                        dsDest + str("/meta/train.txt"),
                        nClasses, 375
                        )
    test_classes = genLabels(
                        dsSrc  + str("/meta/test.txt"),
                        dsDest + str("/meta/test.txt"),
                        nClasses, 125
                        )


    return training_classes, test_classes

def checkPythonVersion(rv):
    currentVersion = sys.version_info
    if currentVersion[0] == rv[0] and currentVersion[1] >= rv[1]:
        pass
    else:
        sys.stderr.write( "\n%s - Error: Python interpreter must be %d.%d or greater (within major version %d)\n" % (sys.argv[0], rv[0], rv[1], rv[0]) )
        sys.exit(-1)
    return 0

if __name__ == "__main__":
    checkPythonVersion( (2,1) )
	training_classes, test_classes = parseClasses(dsSrc, dsDest);
	createNewDataset(dsSrc, dsDest, training_classes, test_classes)
	sys.exit(0)
