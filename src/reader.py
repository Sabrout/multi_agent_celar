#!/usr/bin/python
import glob


class Reader():

    def __init__(self, nbScen=1):
        # Problem Name
        nbScen = 'scen{0:02}'.format(nbScen)
        for filename in glob.glob('output/'+nbScen+'/*.out'):
            print(filename)


def main():
    reader = Reader(nbScen=2)


if __name__ == "__main__":
    main()