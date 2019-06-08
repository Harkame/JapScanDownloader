import sys, os

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../japscandownloader/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import unittest

if __name__ == '__main__':
    iterations = 5

    for iteration in range(iterations):
        sucess = unittest.main(exit=False, argv=unitargs).result.wasSuccessful()

        if not sucess:
            sys.exit(1)
