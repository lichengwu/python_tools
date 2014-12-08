__author__ = 'lichengwu'

import re
import time
import simplejson as json
import datetime
import operator
import search
import sys

ERROR_PATH = "/home/admin/atx/logs/error.log.%s" % (datetime.date.today() - datetime.timedelta(days=1)).strftime(
    "%Y-%m-%d")

SEARCH_URL = "http://10.100.50.110:7001/searchow/search.htm?type=&depCity=%s&arrCity=%s&depDate=%s&tripType=0&searchBy=1366"


def collect():
    route_info = {}
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    p = re.compile(".*depCity=([A-Z]{3}).*arrCity=([A-Z]{3}).*depDate=(.*?),")
    for line in open(ERROR_PATH):
        try:
            if "chosen-failure" not in line:
                continue
            m = p.match(line)
            date = datetime.datetime(*time.strptime(m.groups()[2], "%a %b %d %H:%M:%S %Z %Y")[:3])
            if (yesterday - date).days >= 0:
                date = datetime.date.today()
            key = "%s,%s,%s" % (m.groups()[0], m.groups()[1], date.strftime("%Y-%m-%d"))
            if not route_info.has_key(key):
                route_info[key] = 1
            else:
                route_info[key] = (route_info[key] + 1)
        except Exception, ex:
            print ex
    # print sorted(route_info.iteritems(), key=operator.itemgetter(1), reverse=True)
    return route_info


def sum(path, gt):
    summary = {}
    for line in open(path):
        line = line.replace("/\\n", '')
        data = json.loads(line)
        for k in data:
            route = eval(data[k])
            for k, v in route.items():
                if summary.has_key(k):
                    summary[k] = summary[k] + int(v)
                else:
                    summary[k] = int(v)

    for k, v in summary.items():
        if v <= gt:
            del summary[k]
    return sorted(summary.iteritems(), key=operator.itemgetter(1), reverse=True)


if __name__ == "__main__":
    # print collect()
    path = str(sys.argv[1])
    params = sum(path, 1)
    f = open('/home/chengwu.lcw/stat/price_search/price_search.data',"w")
    urls = []
    for k in params:
        param = k[0].split(",")
        url = SEARCH_URL % (param[0], param[1], param[2])
        f.write(url)
        f.write("\n")
        print urls
        print url+"<br />"
    f.close()
        # s = search.search()
        # s.multi_req(urls, 10, True)