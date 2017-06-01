import os
import sys

def main():
    # print command line arguments
    firebaseurl = sys.argv[1]
    filename = sys.argv[2]
    os.system("firebase-import --database_url " + str(firebaseurl) + " --path / --json " + str(filename))
if __name__ == "__main__":
    main()
