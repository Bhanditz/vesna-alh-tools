'''
Created on Nov 2, 2012

@author: zoltanp
'''
import pickle

def main():
    try:
        f = open("f1oo.pickle", "r")
    except IOError:
        print "open error"
        return
    data = pickle.load(f)
    print data
    print data['user']
    print data['pwd']
    pass

if __name__ == '__main__':
    main()