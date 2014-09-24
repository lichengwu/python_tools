#coding=utf-8
'''
Created on 2011-12-7

@author: lichengwu
'''
def add2syspath(a_path):
    '''
    将一个路径放入系统变量里面，如果路径不存在，返回-1
    如果系统变量里面已存在这个路径 返回 0
    添加成过返回1
    '''
    import sys, os
    if not os.path.exists(a_path):
        return -1
    new_path = os.path.abspath(a_path)

    if sys.platform == 'win32':
        new_path = new_path.lower()
    
    for exist_path in sys.path:
        exist_path = os.path.abspath(exist_path)
        if sys.platform == 'win32':
            exist_path = exist_path.lower()
        if new_path in (exist_path, exist_path + os.sep):
            return 0
    sys.path.append(new_path)
    return 1

if __name__ == '__main__':
    import sys
    print sys.path
    print add2syspath(r'D:\\')
