import random

filenames = ['olahraga_training.txt', 'politik_training.txt', 'entertainment_training.txt']


with open('training2.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)