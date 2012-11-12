'''
Create an authentication data structure and save it in a file.
Useful for avoiding:
1) hard-coded authentication data in code
2) manually entering authentication data every time

'''

import pickle

def main():
    to_be_saved = {
        "user" : "",
        "pwd" : ""
        }
    to_be_saved["user"] = raw_input("enter user name:")
    to_be_saved["pwd"] = raw_input("enter password:")
    auth_file = open("auth.pickle", "w")
    pickle.dump(to_be_saved, auth_file)
    auth_file.close()
    pass

if __name__ == '__main__':
    main()
