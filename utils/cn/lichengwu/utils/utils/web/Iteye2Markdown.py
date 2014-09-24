__author__ = 'lichengwu'

from HTMLParser import HTMLParser
import urlparse,urllib


if __name__ == "__main__":

    wp = urllib.urlopen("http://softbeta.iteye.com/blog/1797485","User Agent")
    print wp.read()


