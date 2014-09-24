__author__ = 'lichengwu'

import urllib2
import thread
import time


def req():
    while True:
        response = urllib2.urlopen(
            "http://42.120.83.52/search/cheapFlight.htm?_ksTS=1406015761108_120&ruleId=4")
        html = str(response.read())
        print html
        if len(html) < 1000:
            print html

if __name__ == '__main__':
    for i in range(1, 10):
        thread.start_new(req, ())

    time.sleep(60000)
