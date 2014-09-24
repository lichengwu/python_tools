#!/usr/bin/python
#encoding=utf8
__author__ = 'lichengwu'
import pexpect
import sys
import getopt


def run_command(ip, user, password, cmd, tmo=600):
    '''
    执行远程命令
    @ip         命令所在的主机ip
    @user       执行命令的用户
    @password   用户密码
    @cmd        命令
    @tmo        命令执行潮湿时间
    '''

    patterns = [user, '.*[Pp]assword:', 'Are you sure you want to continue connecting (yes/no)?',
                '.*[Pp]ermission denied.*',
                pexpect.EOF]
    p = pexpect.spawn(cmd, timeout=tmo)
    try:
        try_times = 0
        i = p.expect(patterns)
        p.logfile = sys.stdout
        while i < len(patterns):
            if try_times > 100:
                print "%s 失败：尝试%d次" % (ip, try_times)
                return
                # first time connect
            if i == 2:
                p.sendline('yes')
            # Permission denied
            elif i == (len(patterns) - 2):
                print "%s 失败：帐户[%s]没有权限" % (ip, user)
                return
            elif i == (len(patterns) - 1):
                break
            else:
                p.sendline(password)
                # go on try connect
            i = p.expect(patterns)
            try_times += 1
        p.flush()
        p.close()
        print "%s 执行成功!" % ip
    except pexpect.TIMEOUT:
        print "%s 失败：超时" % ip
        return
    except pexpect.EOF:
        print "%s 失败：EOF" % ip
        return


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "i:u:p:t:")
    ips = None
    timeout = 600
    user = 'chengwu.lcw'
    password = None
    cmd = None
    for kv in opts:
        key = kv[0]
        value = kv[1]
        if key == '-i':
            ips = value
        elif key == '-u':
            user = value
        elif key == '-p':
            password = value
        elif key == '-t':
            timeout = value

    cmd = ' '.join(args)

    if ips is None:
        print '请指定远程机器'
        sys.exit(1)

    if cmd is None:
        print '请输入执行命令'
        sys.exit(1)

    for ip in ips.split(","):
        i_cmd = 'ssh -t  %s@%s %s' % (user, ip, cmd)
        run_command(ip, user, password, i_cmd, int(timeout))
    sys.exit(0)
