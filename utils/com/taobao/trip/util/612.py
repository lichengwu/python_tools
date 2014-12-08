# import json
import urllib2
import time
import thread
import datetime


# def check_price(rid=2, tab_code=None):
# print 'request rid=%s' % rid
# html = None
# try:
# response = urllib2.urlopen(
#             'http://s.jipiao.trip.taobao.com/search/cheapFlight.htm?_ksTS=1402280257772_1778&ruleId=%d' % rid)
#         html = str(response.read()).strip()[1:-1]
#         data = json.loads(html)
#         flights = data['data']['flights']
#         for f in flights:
#             if int(f['price']) > 10000:
#                 print "Error Price [rid=%d],f=%s,host=%s" % (rid, f['price'], data['host'])
#
#     except Exception:
#         print 'exception:%s' % html


def run_search(routes, name=None, s=False, start_date=datetime.date.today(), end_date=datetime.date.today()):
    days = (end_date - start_date).days + 1
    dep_date = start_date
    i_begin = time.time()
    for i in xrange(0, days):
        begin = time.time()
        dep_date = start_date + datetime.timedelta(i)
        dep_str = dep_date.strftime("%Y-%m-%d")
        print "[thread-%s]\t%s [start]" % (name, dep_str)
        for route in routes:
            try:
                ct = route.split("-")
                url = "http://172.21.96.211:7001/searchow/search.htm?searchBy=1280&depCity=" + \
                      ct[0] + "&arrCity=" + ct[1] + "&tripType=0&depDate=" + dep_str
                #print url
                response = urllib2.urlopen(url)
                #html = str(response.read()).strip()[1:-1]
                #print html
                #print "%s,%s-%s,%s [ok]" % (name, ct[0], ct[1], dep_str)
            except Exception:
                pass
        print "[thread-%s]\t%s [done],time used:%ds" % (name, dep_str, (time.time() - begin))
    print "[thread-%s]\t all task done in %ds" % (name, (time.time() - i_begin))
    thread.exit_thread()


def warm_up_routes(c=4, start_date=datetime.date.today(), end_date=datetime.date.today()):
    routes = dict()
    iCunt = 0
    for line in open("/home/chengwu.lcw/bin/data/612_airline"):
        index = iCunt % c
        if not routes.has_key(index):
            routes[index] = set()
        routes[index].add(line.strip())
        iCunt += 1
    for k in routes.keys():
        thread.start_new(run_search, (routes[k], k, True, start_date, end_date))


# if __name__ == '__main__':
#     # while True:
#     # for x in range(45, 62):
#     # check_price(x)
#     # time.sleep(1)