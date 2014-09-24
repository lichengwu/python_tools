#!/usr/bin/python
#encoding=gbk
__author__ = 'lichengwu'
import pexpect
import sys
import getopt
import time
import os


def enum(**enums):
    return type('Enum', (), enums)


MODE = enum(FULL='full', STOP='stop', START='start', RESTART='restart')


def run_command(ip, user, password, cmd, tmo=600):
    print 'try connect [%s] using %s' % (ip, user)

    patterns = [user, '.*[Pp]assword:', 'Are you sure you want to continue connecting (yes/no)?',
                '.*[Pp]ermission denied.*',
                pexpect.EOF]
    p = pexpect.spawn(cmd, timeout=tmo)
    p.logfile = sys.stdout
    try:
        try_times = 0
        i = p.expect(patterns)
        while i < len(patterns):
            if try_times > 100:
                print "尝试100次失败，推出!"
                sys.exit(1)
                # first time connect
            if i == 2:
                p.sendline('yes')
            # Permission denied
            elif i == (len(patterns) - 2):
                print '帐户%s没有%s的sudo权限，请申请：http://aops.alibaba-inc.com/workflow/account/new/' % (user, ip)
                sys.exit(1)
            elif i == (len(patterns) - 1):
                break
            else:
                p.sendline(password)
                # go on try connect
            i = p.expect(patterns)
            try_times += 1
        p.flush()
        p.close()
        print '命令[%s]执行完成!' % cmd
    except pexpect.TIMEOUT:
        print '超时，请确认机器[%s]ssh可用，并加大超时时间，当前时间%ss' % (ip, tmo)
        sys.exit(1)
    except pexpect.EOF, e:
        print 'EOF', e
        sys.exit(1)


def get_command(app, user, ip, mode='full'):
    if mode.lower() == MODE.FULL:
        build_cmd = 'sudo -u admin -H rm -rf nohup.out > /dev/null 2>&1 ; sudo -u admin -H nohup /home/admin/build.sh ; sudo -u admin -H chmod +r /home/admin/nohup.out'
    else:
        build_cmd = 'sudo -u admin -H /home/admin/%s/bin/jbossctl %s' % (app, mode)
    build_cmd = 'ssh -t  %s@%s %s' % (user, ip, build_cmd)

    return build_cmd


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "i:u:p:a:m:t:")
    ip = None
    app = None
    timeout = 600
    user = 'chengwu.lcw'
    password = None
    mode = MODE.FULL
    for kv in opts:
        key = kv[0]
        value = kv[1]
        if key == '-i':
            ip = value
        elif key == '-u':
            user = value
        elif key == '-p':
            password = value
        elif key == '-a':
            app = value
        elif key == '-m':
            mode = value
        elif key == '-t':
            timeout = value

    if app is None:
        print '请指定应用!'
        sys.exit(1)

    if ip is None:
        print '请指定远程机器'
        sys.exit(1)

    # print "ip=%s,user=%s,password=%s,timeout=%s,app=%s,mode=%s" % (ip, user, password, timeout, app, mode)
    cmd = get_command(app, user, ip, mode)
    #执行ci
    run_command(ip, user, password, cmd, int(timeout))
    file_name = "/tmp/" + str(int(time.time())) + ".ci"
    #取得结果
    read_cmd = 'scp %s@%s:/home/admin/nohup.out %s' % (user, ip, file_name)
    run_command(ip, user, password, read_cmd)
    #打印到页面
    for line in open(file_name):
        print line
    os.remove(file_name)
    sys.exit(0)
