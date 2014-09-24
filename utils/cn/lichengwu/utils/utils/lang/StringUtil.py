# Created on Dec 3, 2011
# coding=utf-8
from __future__ import division

__author__ = 'lichengwu'

import string


class StringUtil:
    '''
    String工具类
    '''

    null_trans = None

    def __init__(self):
        self.null_trans = string.maketrans('', '')

    # 测试字符串，32-127是文本字符
    text_characters = ''.join(map(chr, range(32, 127))) + '\n\r\t\b'

    def istext(s, text_characters=text_characters, threadhold=0.30):
        '''
        判断一个字符串是文本还是二进制
        如果字符串中30%字符高位被置1，则是二进制
        '''

        #如果s包含控制，返回false
        if '\0' in s:
            return False
        #“空”的字符串是文本
        if not s:
            return True
        #获得s的非文本字符串构成的子串
        t = s.translate(StringUtil.null_trans, text_characters)
        return len(t) / len(s) <= threadhold

    def is_string_like(s):
        #通过判断行为，断定是否是字符串
        try:
            str(s).upper()
        except:
            return False
        return True

    def re_indent(s, numberSpace):
        '''重新缩进行'''

        leading_space = ' ' * numberSpace
        return '\n'.join(leading_space + line.lstrip() for line in s.splitlines())


    istext = staticmethod(istext)
    is_string_like = staticmethod(is_string_like)
    re_indent = staticmethod(re_indent)


if __name__ == '__main__':
    s = '''line one
    line 2
    line 3
    line 4
    '''
    print StringUtil.re_indent(s, 10)
