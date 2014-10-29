__author__ = 'lichengwu'

import time
import re
import sys

if __name__ == '__main__':
    routes = []
    if len(sys.argv) > 1:
        for citys in str(sys.argv[1]).split(","):
            dep_arr = citys.split("-")
            if len(dep_arr) == 2:
                routes.append([dep_arr[0], dep_arr[1]])
    print "hot routes:%s" % routes
    year = time.strftime('%Y')
    month = time.strftime('%m')
    date_str = str(time.strftime('%Y-%m-%d'))
    path = "/home/admin/cai/logs/cronolog/%s/%s/%s-taobao-access_log" % (year, month, time.strftime('%Y-%m-%d'))
    # path = "/Users/lichengwu/Downloads/aa.log"
    print "[log path:%s]" % path
    file_all = open("search_all.log", "w")
    file_hot = open("search_hot.log", "w")
    al_count = 0
    hot_count = 0
    for line in open(path):
        meta = line.split(" ")
        if len(meta) < 6:
            continue
        url = meta[6]
        if date_str in url:
            continue
        if "searchow" in url and "tripType=0" in url and "searchBy" in url:
            result, number = re.subn("searchBy=.*&", "searchBy=1366&", url)
            file_all.write(result)
            file_all.write("\n")
            al_count += 1
            if len(routes) > 0:
                for citys in routes:
                    if "depCity=" + citys[0] in url and "arrCity=" + citys[1] in url:
                        file_hot.write(url)
                        file_hot.write("\n")
                        hot_count += 1
                        break
    file_hot.close()
    file_all.close()
    print "[done]"

