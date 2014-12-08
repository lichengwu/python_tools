__author__ = 'lichengwu'

import urllib2
import thread
import time


def check(urls, file, name):
    if not urls:
        return
    for url in urls:
        try:
            response = urllib2.urlopen(url)
            html = str(response.read())
            if "cabin" in html:
                url = url.replace("\n", '')
                if url.endswith("\""):
                    url = url[0:-1]
                file.write(url + "&link_test=t\n")
            else:
                print "expired url:%s" % url
        except Exception, ex:
            print ex

    print "thread %s done" % str(name)


if __name__ == "__main__":
    max_thread = 5
    url_data = {}
    index = 0
    for line in open("/home/chengwu.lcw/jipiao_search_notNeedLogin_n.log"):
        k = index % max_thread
        if not url_data.has_key(k):
            url_data[k] = []
        url_data[k].append(line)
        index += 1

    for k, v in url_data.iteritems():
        print "%s,size=%s" % (k, len(v))

    result = open("tmp.log", "w")

    for i in xrange(0, max_thread):
        thread.start_new(check, (url_data.get(i, None), result, i))
    time.sleep(100000)
    result.close()