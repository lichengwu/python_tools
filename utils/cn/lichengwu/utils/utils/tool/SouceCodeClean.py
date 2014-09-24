__author__ = 'zuojing'

import sys
import os
import shutil

'''
delete dirty dirs in path
make source code clean
'''

if __name__ == "__main__":


    def findInPath(basePath, includeDir):
        # list dir
        dirs = os.listdir(basePath)

        for dir in dirs:
            path = os.path.join(basePath, dir)
            if os.path.isdir(path):
                if dir in includeDir:
                    # remove dirty dirs
                    confirm = raw_input("delete %s ?[Y/n]" % path)
                    if confirm == 'Y' or confirm == 'y' or confirm == '':
                        shutil.rmtree(path)
                    break
                else:
                    findInPath(path, includeDir)


    if len(sys.argv) < 2:
        print 'source code path exists...'
        print 'usage:'
        print '\tcmd path dirs'
        exit(0)

    includeDir = []
    for i in range(2, len(sys.argv)):
        includeDir.append(sys.argv[i])

    path = sys.argv[1]
    print 'clean source code in %s' % path
    findInPath(path, includeDir)
