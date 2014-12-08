# encoding=utf8

__author__ = 'lichengwu'

import urllib2
import simplejson as json
import datetime
import sys

reload(sys)

sys.setdefaultencoding('utf8')

CONFIG_PATH = "/home/chengwu.lcw/cfg"

TARGET_PATH = "/home/admin/atc/target/atc.war/"

J = "jsonp%s(%s)"

XP_URL = "http://s.jipiao.trip.taobao.com/search/cheapestProductList.htm?ruleId=%s"
# XP_URL = "http://10.101.106.144:8080/search/cheapestProductList.htm?ruleId=%s&xtabCode=548"

# LOW_PRICE_URL = "http://10.125.15.22:8080/search/cheapFlight.htm?ruleId=%s&routeSize=%s&filterRoutes=%s&routes=%s"
LOW_PRICE_URL = "http://s.jipiao.trip.taobao.com/search/cheapFlight.htm?ruleId=%s&routeSize=%s&filterRoutes=%s&routes=%s&_input_charset=utf8"

'''
    load xp and low price rule id config from file path
'''


def load_config(path):
    f = None
    cfg = {}
    try:
        f = open(path)
        config = f.readline()
        if config:
            for kv in config.split(";"):
                c = kv.split(",")
                if len(c) != 2:
                    continue
                cfg[c[0]] = c[1]
        print "[config]:%s" % str(cfg)
        return cfg
    except Exception, ex:
        if f:
            f.close()
        print ex
        return cfg


'''
    merge low price data to xp
'''


def json_merge(xp, low_price):
    if not low_price:
        return xp
    for low_price in low_price.get("data").get("flights"):
        _flight = {}
        _flight["depCode"] = low_price.get("depCode")
        _flight["arrCode"] = low_price.get("arrCode")
        _flight["depName"] = low_price.get("depName")
        _flight["arrName"] = low_price.get("arrName")
        _flight["price"] = low_price.get("price")
        _flight["depDate"] = low_price.get("depDate")
        _flight["week"] = low_price.get("week")
        _flight["discount"] = low_price.get("discount")
        _flight["img"] = low_price.get("img")
        _flight["soldOut"] = False
        if low_price.get("shopHost"):
            _flight["shopHost"] = low_price.get("shopHost")
        if low_price.get("depNameGBK"):
            _flight["depNameGBK"] = low_price.get("depNameGBK")
        if low_price.get("arrNameGBK"):
            _flight["arrNameGBK"] = low_price.get("arrNameGBK")
        _flight["travelStartDate"] = low_price.get("depDate")
        _flight["travelEndDate"] = low_price.get("depDate")
        if low_price.get("priceDesc"):
            _flight["priceDesc"] = low_price.get("priceDesc")
        _flight["flightNumber"] = low_price.get("flightNumber")
        _flight["depTime"] = low_price.get("depTime")
        xp.get('data').get('flights').append(_flight)
    return xp


'''
    request data from url
'''


def fetch_data(url):
    data = {}
    try:
        resp = urllib2.urlopen(url)
        html = str(resp.read()).strip()[1:-1]
        data = json.loads(html)
        if not data.get('data'):
            data['data'] = {}
        if not data.get('data').get('flights'):
            data.get('data')['flights'] = []
        return data
    except Exception, ex:
        print ex
        return data


def check_result(data_json, xp_id):
    if not data_json:
        print "[%s] check error, not data" % xp_id
        return
    _flights = data_json.get('data').get('flights')
    if not _flights or len(_flights) == 0:
        print "[%s] check error, no flight" % xp_id
        return

    for _flight in _flights:
        discount = _flight.get("discount")
        if discount:
            _flight["discount"] = "%.1f" % float(discount)
    return


if __name__ == "__main__":
    # 1. load config
    global_cfg = load_config(CONFIG_PATH)
    for k, v in global_cfg.iteritems():
        try:
            xp_id = str(k)
            print "[%s] start" % xp_id
            xp_json = fetch_data(XP_URL % xp_id)
            print "[%s] fetch xp ok!" % xp_id
            cfg = xp_json.get('data').get("config")
            flights = xp_json.get('data').get('flights')
            routes = ""
            cityName = cfg.get('tabs')[0]['tabName']
            max_flt = int(cfg.get('flightSize', 10))
            act_num = len(flights)
            route_size = max_flt - act_num
            print "[%s] remind %s slots!" % (xp_id, str(route_size))
            exclude_routes = []
            low_price_json = None
            vv = v.split("-")
            rule_id = vv[0]
            flag = None
            if len(vv) > 1:
                flag = vv[1]
            if route_size > 0:
                if len(flights) > 0:
                    flights_ = flights[0]
                    if flights_.get("arrName") == cityName:
                        routes = "-" + flights_.get("arrCode")
                    if flights_.get("depName") == cityName:
                        routes = flights_.get("depCode") + "-"
                else:
                    if flag and flag == "1":
                        routes = "-" + cityName
                    else:
                        routes = cityName + "-"
                    routes = unicode.encode(routes, "utf8")
                for flight in flights:
                    exclude_routes.append(flight.get("depCode") + flight.get("arrCode"))
                ext = ",".join(exclude_routes)
                print "[%s] fetch low price, param:rule_id=%s,exclude=%s,routes=%s" % (xp_id, rule_id, ext, routes.encode("gbk"))
                low_price_json = fetch_data(LOW_PRICE_URL % (rule_id, route_size, ext, routes))
                json_merge(xp_json, low_price_json)
                print "[%s] json merge done!" % xp_id
            check_result(xp_json, xp_id)
            file_name = TARGET_PATH + xp_id + ".json"
            rs = J % (xp_id, json.dumps(xp_json))
            f = open(file_name, "w")
            f.write(rs)
            f.close()
            print "[%s] write to file:%s" % (xp_id, file_name)
            print "[%s] data:%s" % (xp_id, rs)
            print "[%s] done at %s" % (xp_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception, ex:
            print ex
        print "\n"
