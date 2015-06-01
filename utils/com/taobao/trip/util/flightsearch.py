__author__ = 'lichengwu'

import urllib2

import simplejson as json


class Flight:
    def __init__(self):
        ""

    dep_air_port = ""
    arr_air_port = ""
    dep_date = ""
    cabin = ""
    price = 0
    best_price = 0
    origin_price = 0
    ticket_price = 0
    basic_cabin_price = 0
    discount = 0
    best_discount = 0
    insure_discount = 0
    price_type = None
    product_type = None
    stock_type = None
    fare_type = None
    fare_id = 0
    auto_book = False
    agent_id = 0
    air_line = ""
    flight_no = ""


class FlightSearch:
    mode = 1

    def __init__(self, mode=1):
        self.mode = mode

    MODE_1 = 1
    MODE_2 = 2

    url_1 = "http://s.jipiao.trip.taobao.com/searchow/search.htm?depCity=%s&arrCity=%s&depDate=%s&flightNo=%s&type=%s&_input_charset=utf-8&tripType=%s"

    url_2 = "http://127.0.0.1:7001/searchow/search.htm?depCity=%s&arrCity=%s&depDate=%s&flightNo=%s&type=%s&_input_charset=utf-8&tripType=%s"


    def __build_url(self, dep, arr, dep_date, flight_no, search_type, trip_type=0):
        #
        # search_type = ''
        #
        # if flight_no and len(flight_no.strip()) > 0:
        # search_type = 'lowprice'

        if self.mode == 1:
            return self.url_1 % (dep, arr, dep_date, flight_no, search_type, trip_type)
        if self.mode == 2:
            return self.url_2 % (dep, arr, dep_date, flight_no, search_type, trip_type)

    @staticmethod
    def __cabin2flight(air_data, dep_date):
        raw_cabins = air_data['cabin']
        if not raw_cabins:
            return
        flight = air_data['flight']
        flights = []
        for raw in raw_cabins:
            f = Flight()
            f.cabin = raw['cabin']
            f.auto_book = bool(raw['autoBook'])
            f.basic_cabin_price = int(raw['basicCabinPrice'])
            f.best_discount = int(raw['bestDiscount'])
            f.best_price = int(raw['bestPrice'])
            f.discount = int(raw['discount'])
            f.fare_id = int(raw['fareId'])
            f.fare_type = int(raw['fareType'])
            f.insure_discount = int(raw['insureDiscount'])
            f.origin_price = int(raw['originPrice'])
            f.ticket_price = int(raw['ticketPrice'])
            f.agent_id = int(raw['agentId'])
            f.dep_air_port = flight['depAirport']
            f.arr_air_port = flight['arrAirport']
            f.air_line = flight['airlineCode']
            f.dep_date = dep_date
            f.flight_no = flight['flightNo']
            flights.append(f)
        return flights

    @staticmethod
    def __flight2flight(air_data, dep_date):
        raw_flights = air_data['flight']
        if not raw_flights:
            return
        flights = []
        for raw in raw_flights:
            f = Flight()
            cabin = raw['cabin']
            f.cabin = cabin['cabin']
            f.auto_book = bool(cabin['autoBook'])
            f.basic_cabin_price = int(cabin['basicCabinPrice'])
            f.best_discount = int(cabin['bestDiscount'])
            f.best_price = int(cabin['bestPrice'])
            f.discount = int(cabin['discount'])
            f.fare_id = int(cabin['fareId'])
            f.fare_type = int(cabin['fareType'])
            f.insure_discount = int(cabin['insureDiscount'])
            f.origin_price = int(cabin['originPrice'])
            f.ticket_price = int(cabin['ticketPrice'])
            f.agent_id = int(cabin['agentId'])
            f.dep_air_port = raw['depAirport']
            f.arr_air_port = raw['arrAirport']
            f.air_line = raw['airlineCode']
            f.flight_no = raw['flightNo']
            f.dep_date = dep_date
            flights.append(f)
        return flights


    def req(self, dep, arr, dep_date, flight_no, search_type, trip_type=0):
        url = self.__build_url(dep, arr, dep_date, flight_no, search_type, trip_type)
        print url
        resp = urllib2.urlopen(url)
        html = str(resp.read()).strip()
        raw = html[1:-2].strip()
        js = json.loads(raw, encoding='GBK')
        if not js:
            return

        data = js['data']
        if not data:
            return
        if search_type == 'lowprice':
            return self.__cabin2flight(data, dep_date)
        else:
            return self.__flight2flight(data, dep_date)


if __name__ == "__main__":
    air = FlightSearch(mode=1)
    data = air.req("BJS", "SHA", "2015-10-10", '', '', 0)
    for flight in data:
        print ', '.join(['%s:%s' % item for item in flight.__dict__.items()])
