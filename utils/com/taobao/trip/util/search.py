__author__ = 'lichengwu'

import urllib2
import time
import thread


class search:
    RATE = 100

    def req(self, urls, name, check=False):
        total = 0
        for _url in urls:
            total += 1
            resp = None
            try:
                if total % self.RATE == 0:
                    print "[Thread-%s] complete %s" % (name, "%.2f%%" % (total * 100.0 / len(urls)))
                resp = urllib2.urlopen(_url)
                if check:
                    html = str(resp.read()).strip()
                    # data = json.loads(html)
                    if "error\":0" not in html:
                        print "[Thread-%s] no result,url=%s,html=%s" % (name, _url, html)
            except Exception, ex:
                print "[Thread-%s] error:%s,url=%s,result:%s" % (name, ex, _url, resp)
        print "[Thread-%s] done!" % name

    def multi_req(self, _urls, thread_num, check=False):
        url_group = {}
        index = 0
        for _url in _urls:
            key = index % int(thread_num)
            if not url_group.has_key(key):
                url_group[key] = []
            url_group[key].append(_url)
            index += 1

        print "Thread Info:"
        for k, v in url_group.iteritems():
            print "\tThread-%s,url count:%s" % (k, len(v))

        for k, v in url_group.iteritems():
            thread.start_new_thread(self.req, (v, k, check))
        time.sleep(99999)


if __name__ == "__main__":
    search = search()
    urls = []
    for i in xrange(0, 10):
        urls.append(
            "http://s.jipiao.trip.taobao.com/searchow/search.htm?type=&depCity=BJS&arrCity=SHA&depDate=2014-11-11&tripType=0&searchBy=1366")
    search.multi_req(urls, 2, True)