from func_timeout import *
import math

def CalculateWithTimeout():
    fr = open('solution.txt', 'r')
    question = fr.readline()
    fr.close()
    try:
        solution = str(eval(question))
        
    except:
        solution = ''
    fw = open('solution.txt', 'w')
    fw.write('>' + solution)
    fw.close()
if __name__ == '__main__':
    CalculateWithTimeout()
    