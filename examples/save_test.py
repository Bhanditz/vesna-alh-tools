'''
Created on Nov 2, 2012

@author: zoltanp
'''
import pickle

def main():
    saved = {
        "user" : "user1",
        "pwd" : "pwd1"
        }
    f = open("foo.pickle", "w")
    pickle.dump(saved, f)
    f.close()
    pass
    
if __name__ == '__main__':
    main()
