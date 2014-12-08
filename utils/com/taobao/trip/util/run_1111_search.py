__author__ = 'lichengwu'

import search
import time
import datetime
import sys

if __name__ == "__main__":
    path = str(sys.argv[1])
    threads = int(sys.argv[2])
    check = False
    if len(sys.argv) > 3:
        check = True
    urls = set()
    for line in open(path):
        params = line.strip().split(";")
        if len(params) != 4:
            continue
        start = datetime.datetime(*time.strptime(params[0], "%Y%m%d")[:3])
        end = datetime.datetime(*time.strptime(params[1], "%Y%m%d")[:3])
        dep = params[2]
        arr = params[3]
        days = (end - start).days + 1
        for diff in xrange(0, days):
            urls.add(
                "http://127.0.0.1:7001/searchow/search.htm?depCity=%s&arrCity=%s&depDate=%s&tripType=0" % (
                    dep, arr, (start + datetime.timedelta(diff)).strftime("%Y-%m-%d")))
    s = search.search()
    s.multi_req(urls, threads, check)
    print len(urls)