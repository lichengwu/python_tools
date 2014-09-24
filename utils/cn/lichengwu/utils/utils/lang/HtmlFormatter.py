'''
Created on Dec 3, 2011

@author: lichengwu
'''
#!/usr/bin/env python
import sys, os, htmllib, formatter
# use Unix tput to get the escape sequences for bold, underline, reset
set_bold = os.popen('tput bold').read()
set_underline = os.popen('tput smul').read()
perform_reset = os.popen('tput sgr0').read()
class HtmlFormatter(formatter.AbstractFormatter):
    ''' a formatter that keeps track of bold and italic font states, and
        emits terminal control sequences accordingly.
    '''
    def __init__(self, writer):
        # first, as usual, initialize the superclass
        formatter.AbstractFormatter.__init__(self, writer)
        # start with neither bold nor italic, and no saved font state
        self.fontState = False, False
        self.fontStack = [  ]
    def push_font(self, font):
        # the `font' tuple has four items, we only track the two flags
        # about whether italic and bold are active or not
        is_italic, is_bold = font
        self.fontStack.append((is_italic, is_bold))
        self._updateFontState()
    def pop_font(self, *args):
        # go back to previous font state
        try:
            self.fontStack.pop()
        except IndexError:
            pass
        self._updateFontState()
    def updateFontState(self):
        # emit appropriate terminal control sequences if the state of
        # bold and/or italic(==underline) has just changed
        try:
            newState = self.fontStack[-1]
        except IndexError:
            newState = False, False
        if self.fontState != newState:
            # relevant state change: reset terminal
            print perform_reset,
            # set underine and/or bold if needed
            if newState[0]:
                print set_underline,
            if newState[1]:
                print set_bold,
            # remember the two flags as our current font-state
            self.fontState = newState
if __name__ == '__main__':
    myWriter = formatter.DumbWriter()
    if sys.stdout.isatty():
        myFormatter = HtmlFormatter(myWriter)
    else:
        myFormatter = formatter.AbstractFormatter(myWriter)
    myParser = htmllib.HTMLParser(myFormatter)
    # feed all of standard input to the parser, then terminate operations
    ss = '''
    <html>
    <head>
        <title>title</title>
    </head>
    <body>
        <ul>
            <li>a</li>
            <li>b</li>
            <li>c</li>
        </ul>
        <a href="a.thml">cilck me</a>
        aaa<br />aaaaaaaaaaaa
    </body>
    <html>
    '''
    myParser.feed(ss)
    myParser.close()
