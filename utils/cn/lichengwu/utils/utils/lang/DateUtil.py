# coding=utf-8
'''
Created on 2011-12-8

@author: lichengwu
'''

import datetime

class DateUtil:
    '''
    时间工具类
    '''
    
    def now():
        '''
        当前时间
        '''
        return datetime.datetime.now()
    
    def yesterday():
        '''
        昨天
        '''
        return datetime.date.today() + datetime.timedelta(days= -1)
    
    def tomorrow():
        '''
        明天
        '''
        return datetime.date.today() + datetime.timedelta(days=1)
    
    def work_day(begin_date, end_date, date_off=None):
        '''
        计算两个日期的工作日天数，
        日期的格式为datetime.date
        默认周末为5，6
        星期一到星期日为 0。。。6
        '''
        if not date_off:
            date_off = 5, 6
        total_days = (end_date - begin_date).days + 1
        if total_days < 1:
            raise Exception, 'end date must greater than begin date'
        wk = begin_date.weekday();
        return len([x for x in range(total_days) if (x + wk) % 7 not in date_off])
    
    
    
    now = staticmethod(now)
    yesterday = staticmethod(yesterday)
    tomorrow = staticmethod(tomorrow)
    work_day = staticmethod(work_day)
    
    
if __name__ == '__main__':
    print DateUtil.now()
    print (DateUtil.yesterday() - DateUtil.tomorrow()).days
