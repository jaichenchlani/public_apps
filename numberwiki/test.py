import mathfunctions
from random import randint

# Global variable, for testing
test_numbers_all_positives = [randint(0,9999) for i in range(10)]
test_numbers = [randint(-9999,9999) for i in range(10)]

def test_changeBase():
    n = 999
    for base in range(2,40):
        print("\nNumber {} Base {}:\n{}".format(n,base,mathfunctions.changeBase(n,base)))

def test_isPrime():
    for n in test_numbers_all_positives:
        print("\nNumber {}:\n{}".format(n,mathfunctions.isPrime(n)))

def test_isEven():
    for n in test_numbers_all_positives:
        print("\nNumber {}:\n{}".format(n,mathfunctions.isEven(n)))

def test_getFactors_and_primeFactors():
    for n in test_numbers_all_positives:
        print("\nFactors of Number {}:\n{}".format(n,mathfunctions.getFactors(n)))
        print("\nPrime Factors of Number {}:\n{}".format(n,mathfunctions.getPrimeFactors(n)))

def test_getFactors_and_primeFactors_special():
    n = 1024
    print("\nFactors of Number {}:\n{}".format(n,mathfunctions.getFactors(n)))
    print("\nPrime Factors of Number {}:\n{}".format(n,mathfunctions.getPrimeFactors(n)))

def test_isPositive():
    for n in test_numbers:
        print("\nNumber {}:\n{}".format(n,mathfunctions.isPositive(n)))

def test_isInteger():
    input_string = "jai"
    print("\nInput String {}:\n{}".format(input_string,mathfunctions.isInteger(input_string))) 
    input_string = "53"
    print("\nInput String {}:\n{}".format(input_string,mathfunctions.isInteger(input_string))) 
    input_string = "0"
    print("\nInput String {}:\n{}".format(input_string,mathfunctions.isInteger(input_string))) 
    input_string = "-53"
    print("\nInput String {}:\n{}".format(input_string,mathfunctions.isInteger(input_string))) 
    input_string = "3.5"
    print("\nInput String {}:\n{}".format(input_string,mathfunctions.isInteger(input_string))) 


if __name__ == "__main__":
    # test_changeBase()
    # test_isPrime()
    # test_isEven()
    test_getFactors_and_primeFactors()
    # test_getFactors_and_primeFactors_special()
    # test_isPositive()
    # test_isInteger()


    