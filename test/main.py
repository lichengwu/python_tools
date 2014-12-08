__author__ = 'lichengwu'
# encoding=utf8

import urllib
import json


if __name__ == "__main__":

    u = urllib.urlopen(
        "http://s.jipiao.trip.taobao.com/search/cheapFlight.htm?ruleId=2&dateRange=2014-12-06,2015-01-06;2015-01-06,2014-02-06;2015-02-06,2015-02-28")
    html = str(u.read()).strip()[1:-1]
    cheap_flight = json.loads(html)
    data = cheap_flight["data"]["flights"]
    for flight in data:
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (
            flight["depName"], flight["arrName"], flight["depCode"], flight["arrCode"], flight["depDate"], flight[
                "price"], flight["discount"],
            "http://s.jipiao.trip.taobao.com/flight_search_result.htm?tripType=0&depCity=%s&depDate=%s&arrCity=%s" % (
                flight["depCode"], flight["depDate"], flight["arrCode"]))
    print len(data)
