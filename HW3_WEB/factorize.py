from time import time
from multiprocessing import Pool, cpu_count

def find_numbs(number):
    res_list = []
    for i in range(1, number+1):
        if number % i == 0:
            res_list.append(i)
    return res_list

def factorize(*numbers):
    result = []
    for number in numbers:
        result.append(find_numbs(number))
    return result

def multi_facrorize(*numbers):
    with Pool(cpu_count()) as p:
        result = p.map(find_numbs, numbers)
    return result

if __name__ == '__main__':
    start = time()
    a, b, c, d  = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(f"Execution time factorize(): {time()- start} ")

    start1 = time()
    a, b, c, d  = multi_facrorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(f"Execution time multi_facrorize(): {time()- start1}")
    print(f"CPU count: {cpu_count()}")

#Execution time factorize(): 0.2950429916381836 
#Execution time multi_facrorize(): 0.3877997398376465
#CPU count: 8