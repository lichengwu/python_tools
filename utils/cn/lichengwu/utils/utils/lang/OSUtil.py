'''
Created on 2011-12-8

@author: lichengwu
'''


def main(cmd, inc=60):
    '''
    定时执行
    '''
    import time, os

    while True:
        os.system(cmd)
        time.sleep(inc)


if __name__ == '__main__':
    main('dir', 1)