__author__ = 'lichengwu'

import urllib
import time


def put(_item_name, _info, _try_time=5):
    count = 0
    for x in xrange(0, _try_time):
        count += 1
        try:
            rs = __inner_put(_item_name, _info)
            if "ok" in rs:
                print "[Success]:%s" % rs
                return
            else:
                print "[Failure]:%s" % rs
                time.sleep(10)
        except Exception, ex:
            print "[Error]:%s" % ex
            time.sleep(10)


def __inner_put(_item_name, _info):
    data = {"collection_flag": 0, "error_info": "", "MSG": _info}
    encode_data = urllib.urlencode({"msg": data})
    url = 'http://127.0.0.1:15776/passive?name=%s&%s' % (_item_name, encode_data,)
    u = urllib.urlopen(url)
    return str(u.read())


#

