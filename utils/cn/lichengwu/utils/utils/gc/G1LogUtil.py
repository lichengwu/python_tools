# coding=utf-8
__author__ = 'lichengwu'

import datetime
import re


'''
Garbage First Log Analyse Util
'''


class G1LogUtil:
    __path = ''
    # some regular expression pattern
    # like this '2012-12-19T10:25:19'
    __START_LINE_PATTERN = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:.*pause.*')
    # like this '112M(112M)->0B(112M)'
    __MEMORY_INFO_PATTERN = re.compile('(\d+)([M|B|K|G])\((\d+)([M|B|K|G])\)->(\d+)([M|B|K|G])\((\d+)([M|B|K|G])\)')
    # like this '16M->16M'
    __SIMPLE_MEMORY_INFO_PATTERN = re.compile('(\d+)([M|B|K|G])->(\d+)([M|B|K|G])')

    # constructor
    def __init__(self, path):
        self.__path = path


    """
    analyse G1 log for java
    """

    def analyse(self):
        # get log reader
        reader = self.__reader(self.__path)
        # number of GC times
        gc_count = 0
        gc_count_young = 0
        gc_count_mixed = 0
        # total stop the world time
        total_stop_time = 0.000000
        # max heap size
        max_heap_size = 0
        # min heap size
        min_heap_size = 0xEFFFFFFFFFFFFFFFF
        # max eden size
        max_eden_size = 0
        # min eden size
        min_eden_size = 0xEFFFFFFFFFFFFFFFF
        # survivor size
        survivor_size = None
        # total eden size for statistics
        total_eden_size = 0
        # map store memory info
        memory_usage_map = {'young_garbage_percent': [], 'heap_garbage_percent': [], 'young_usage_percent': [],
                            'heap_usage_percent': []}
        #log start time
        start_time = None
        # log end time
        finish_time = None
        # gc work thread count
        gc_work_thread_number = None

        each_line = reader.next()

        while each_line:
            if self.__is_start_line(each_line):
                token = each_line.split(' ')
                if 'initial-mark' in each_line:
                    total_stop_time += float(token[6])
                else:
                    total_stop_time += float(token[5])

                if start_time is None:
                    start_time = self.__get_datetime(token[0])
                finish_time = token[0]

                gc_count += 1

                gc_type = token[4][1:-2]
                if gc_type == 'young':
                    gc_count_young += 1
                elif gc_type == 'mixed':
                    gc_count_mixed += 1

            elif each_line.find('   [Eden:') == 0:
                '''
                parse memory info
                '''
                memory_info = each_line.split(' ')

                eden_info = self.__parse_memory_info(memory_info[4])

                survivor_info = self.__parse_memory_info(memory_info[6])

                if survivor_size is None:
                    survivor_size = survivor_info[1]

                heap_info = self.__parse_memory_info(memory_info[8])

                max_heap_size = max(max_heap_size, heap_info[1])
                min_heap_size = min(heap_info[1], min_heap_size)
                # garbage (heap) / before gc (heap)
                memory_usage_map['heap_garbage_percent'].append(float(heap_info[0] - heap_info[2]) / heap_info[0])
                # before gc (heap) / heap size
                memory_usage_map['heap_usage_percent'].append(float(heap_info[0]) / heap_info[1])
                max_eden_size = max(max_eden_size, eden_info[1])
                min_eden_size = min(eden_info[1], min_eden_size)
                # garbage (eden+survivor) / before gc (eden+survivor)
                memory_usage_map['young_garbage_percent'].append(
                    float(eden_info[0] + survivor_info[0] - eden_info[2] - survivor_info[1]) / (
                        eden_info[0] + survivor_info[0]))
                # before gc(eden+survivor) / eden+survivor*2
                memory_usage_map['young_usage_percent'].append(
                    float(eden_info[0] + survivor_info[0]) / (eden_info[1] + survivor_info[1] * 2))
                total_eden_size += eden_info[1]

            elif gc_work_thread_number is None and each_line.find('      [GC Worker Start') == 0:
                gc_work_thread_number = len(each_line.strip().split('  ')) - 1

            each_line = reader.next()

        finish_time = self.__get_datetime(finish_time)

        reader.close()

        print '''G1 log Time:
        [%s] - [%s]''' % (
            start_time.strftime('%Y-%m-%d %H:%M:%S'), finish_time.strftime('%Y-%m-%d %H:%M:%S'))

        summary = '''Memory Info:
        Min Heap Size\t= %sM
        Max Heap Size\t= %sM
        Min Eden Size\t= %sM
        Max Eden Size\t= %sM
        Avg Eden Size\t= %sM
        Survivor Size\t= %sM''' % (
            (max_heap_size / 1024), (min_heap_size / 1024), (max_eden_size / 1024), (min_eden_size / 1023),
            (total_eden_size / gc_count / 1024), survivor_size / 1024)

        print summary

        gc_info = '''GC Info:
        GC Work Threads\t= %s
        Avg Stop Time\t= %.2fms
        GC Throughput\t= %.2f%%
        ''' % (gc_work_thread_number, (total_stop_time * 1000 / gc_count),
               total_stop_time * 100 / (finish_time - start_time).total_seconds())

        gc_info += '''GC(yong) Times\t= %s
        GC(mixed) Times\t= %s
        Total GC Times\t= %s
        ''' % (gc_count_young, gc_count_mixed, gc_count)

        gc_info += '''Avg Yong Generation Garbage Rate\t= %.2f%%
        Avg Heap Garbage Rate\t= %.2f%%
        ''' % (sum(memory_usage_map['young_garbage_percent']) * 100 / len(memory_usage_map['young_garbage_percent']),
               sum(memory_usage_map['heap_garbage_percent']) * 100 / len(memory_usage_map['heap_garbage_percent']))

        gc_info += '''Avg Max Young Generation Usage Rate\t=%.2f%%
        Avg Max Heap Usage Rate\t=%.2f%%
        ''' % (sum(memory_usage_map['young_usage_percent']) * 100 / len(memory_usage_map['young_garbage_percent']),
               sum(memory_usage_map['heap_usage_percent']) * 100 / len(memory_usage_map['heap_usage_percent']))

        print  gc_info

    # get datetime from header line
    def __get_datetime(self, str):
        # time like this '2012-12-12T19:01:28.610'
        datetime_string = str
        if len(str) > 23:
            datetime_string = str[0:23]
        return datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S.%f')

    # test if the line is g1 log start line
    def __is_start_line(self, line):
        #pattern = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:')
        return self.__START_LINE_PATTERN.match(line) is not None

    # private reader for read each line
    def __reader(self, path):
        log_file = open(path, 'r')
        line = log_file.readline()
        while line:
            yield line
            line = log_file.readline()
        log_file.close()
        yield None

    '''
    parse memory info to a tuple in kilobyte
    eg: 1M->1M parse to (1024,1024)
        2M(2M)->0B(1M) parse to (2028,2048,0,1024)
    '''

    def __parse_memory_info(self, info):
        match = self.__MEMORY_INFO_PATTERN.match(info)
        if match:
            cell = match.groups()
            return int(cell[0]) * self.__unit2kb(cell[1]), int(cell[2]) * self.__unit2kb(cell[3]), int(
                cell[4]) * self.__unit2kb(cell[5]), int(cell[6]) * self.__unit2kb(cell[7])

        match = self.__SIMPLE_MEMORY_INFO_PATTERN.match(info)
        if match:
            cell = match.groups()
            return int(cell[0]) * self.__unit2kb(cell[1]), int(cell[2]) * self.__unit2kb(cell[3])

        return None

    # covert unit to KB
    # M = 1024K
    # G = 1024K = 1024K*1024
    def __unit2kb(self, unit):
        if unit == 'M':
            return 1024
        elif unit == 'K':
            return 1
        elif unit == "G":
            return 1048576
        else:
            return 1


if __name__ == '__main__':
    analyseG1Log = G1LogUtil('/home/zuojing/tmp/atw/gc.log')
    analyseG1Log.analyse()
