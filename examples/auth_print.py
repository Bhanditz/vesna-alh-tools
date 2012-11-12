
import pickle

def main():
    try:
        f = open("auth.pickle", "r")
    except IOError as e:
        print "I/O error while opening auth.pickle:", e
        return
    data = pickle.load(f)
    print data
    print "user: '%s'" % (data['user'])
    print "pwd : '%s'" % (data['pwd'])
    pass

if __name__ == '__main__':
    main()