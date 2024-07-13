import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection import collect_data
from data_preprocessing import preprocess_data
from data_tokenize import data_tokenize


def main():
    collect_data()
    preprocess_data()
    data_tokenize()

if __name__ == "__main__":
    main()
