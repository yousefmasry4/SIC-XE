from src.Files import File
import argparse
import os

class Main():
    def __init__(self):
        pass




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs=1)
    args = parser.parse_args()
    print(args.input[0])
    Main()