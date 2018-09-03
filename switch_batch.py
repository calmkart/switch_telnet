# encoding=utf-8
import sys
import telnetlib
import time


def tel(ip, user, password):
    tn = telnetlib.Telnet(ip, port=23)
    tn.read_until('Verification\r\n\r\nUsername: ')
    tn.write(user+'\n')
#   tn.set_debuglevel(2)
    # password
    tn.read_until('Password: ')
    tn.write(password+'\n')
    # login fail
    if tn.read_some() == '\r\nPassword: ':
        print '\033[1;31;40m'+ip+'\033[0m'+'     password is wrong,login false!'
        tn.close()
        return 1
    # login successs
    tn.write('enable\n')
    # password
    tn.read_until('Password: ')
    tn.write(password+'\n')
    # enable susccess set terimal length
    tn.read_until('Switch#')
    tn.write('ter len 0\n')
    time.sleep(1)
    if tn.read_some() == 'ter len 0\r\nSwitch#':
        print ip+'     telnet login susccess'
        return tn
    print ip+'     terminal length 0 false!'
    return 1


def comm(tn, ip, cmd):
    tn.write(cmd+'\n')
    time.sleep(.2)
    result = tn.read_very_eager()
    print('\033[1;31;40m'+ip+'\033[0m'+'   '+result)


ip_list = []
user_list = []
password_list = []
tn = []
ip_fp = open('ip_list', 'r')
ip_fs = ip_fp.read()
ip_fp.close()
fa = ip_fs.split('\n')

for i in range(0, len(fa)-1):
    f_res = fa[i].split(',')
    ip_list.append(f_res[0])
    user_list.append(f_res[1])
    password_list.append(f_res[2])

for i in range(0, len(fa)-1):
    tn.append(tel(ip_list[i], user_list[i], password_list[i]))


while 1:
    cmd = raw_input("input the command: ")
    if cmd == 'quit':
        for i in range(0, len(fa)-1):
            tn[i].write('quit\n')
        break

    for i in range(0, len(fa)-1):
        comm(tn[i], ip_list[i], cmd+'\n')
