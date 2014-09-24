if __name__ == "__main__":
    for i in xrange(0, 64):
        print i
        if (i + 1) % 8 == 0:
            print "========%d========" % ((i / 8) + 1)