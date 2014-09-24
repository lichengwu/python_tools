__author__ = 'lichengwu'

import re
import time


class CmsLogUtil:
    __path = ''
    # some regular expression pattern
    # like this '2012-12-19T10:25:19'
    __START_TIME_PATTERN = re.compile('^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}):')
    # [GC [1 CMS-initial-mark: 2723087K(3145728K)] 3525585K(4106944K), 0.5421880 secs] [Times: user=0.54 sys=0.00, real=0.54 secs]
    __INITIAL_MARK = re.compile('.*CMS-initial-mark.*real=(\d+\.\d+) secs')
    # 2013-09-16T10:55:04.208+0800: 97.669: [GC[YG occupancy: 89270 K (961216 K)]97.669: [Rescan (parallel) , 0.2488090 secs]97.918: [weak refs processing, 0.0045450 secs]97.923: [class unloading, 0.0013850 secs]97.924: [scrub symbol & string tables, 0.0010980 secs] [1 CMS-remark: 2180854K(3145728K)] 2270124K(4106944K), 0.2565300 secs] [Times: user=0.92 sys=0.01, real=0.26 secs]
    __REMARK = re.compile('.*CMS-remark.*real=(\d+\.\d+) secs')
    #  [CMS-concurrent-mark: 4.914/12.860 secs] [Times: user=19.21 sys=0.09, real=12.88 secs]
    __CONCURRENT_MARK = re.compile('.*CMS-concurrent-mark.*real=(\d+\.\d+) secs')
    # [GC 24.168: [ParNew: 961216K->87360K(961216K), 0.3447740 secs] 1443823K->638087K(4106944K), 0.3448640 secs] [Times: user=1.17 sys=0.01, real=0.34 secs]
    __PAR_NEW = re.compile('.*ParNew.*real=(\d+\.\d+) secs')

    # constructor
    def __init__(self, path):
        self.__path = path

    def analyse(self):
        initMark = []
        remark = []
        concurrentMark = []
        parNew = []

        begin = None
        end = None

        for line in open(self.__path):
            initialMarkPattern = self.__INITIAL_MARK.match(line)
            remarkPattern = self.__REMARK.match(line)
            concurrentMarkPattern = self.__CONCURRENT_MARK.match(line)
            timeLinePattern = self.__START_TIME_PATTERN.match(line)
            parNewPattern = self.__PAR_NEW.match(line)

            if initialMarkPattern:
                cell = initialMarkPattern.groups()
                initMark.append(float(cell[0]))

            if remarkPattern:
                cell = remarkPattern.groups()
                remark.append(float(cell[0]))
            if concurrentMarkPattern:
                cell = concurrentMarkPattern.groups()
                concurrentMark.append(float(cell[0]))

            if parNewPattern:
                parNew.append(float(parNewPattern.groups()[0]))

            if timeLinePattern:
                currentTime = self.__get_datetime(line)
                if not begin or begin > currentTime:
                    begin = currentTime
                if not end or end < currentTime:
                    end = currentTime

        avgInitMark = self._avg(initMark)
        avgRemark = self._avg(remark)
        print 'avg-par-new[%d times]:%4.2fs' % (len(parNew), self._avg(parNew))
        print 'avg-init-mark[%d times]:%4.2fs' % (len(initMark), avgInitMark)
        print 'avg-remark[%d times]:%4.2fs' % (len(remark), avgRemark)
        print 'avg-concurrent-mark[%d times]:%4.2fs' % (len(concurrentMark), self._avg(concurrentMark))
        print 'avg-stop-time:%4.2fs' % (avgInitMark + avgRemark)
        total = end - begin
        print "throughput:%4.2f%%" % ((total - sum(initMark) - sum(remark)) * 100 / total)

    def _avg(self, list):
        size = len(list)
        if size <= 0:
            size = 1
        return sum(list) / size

    # get datetime from header line
    def __get_datetime(self, str):
        # time like this '2012-12-12T19:01:28.610'
        if len(str) > 23:
            return time.mktime(time.strptime(str[0:19], '%Y-%m-%dT%H:%M:%S'))
        else:
            return None


if __name__ == "__main__":
    util = CmsLogUtil('/home/zuojing/tmp/atw/gc.log')
    util.analyse()
