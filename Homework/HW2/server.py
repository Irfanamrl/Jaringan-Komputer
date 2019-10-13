#!/usr/bin/env python3
import socket

from _thread import *
import threading
import platform
import subprocess
import re
import os
import psutil
import shutil
import urllib

print_lock = threading.Lock()
success_cli = []
failed_cli = []

def getHardware():
    answer = ''
    a = subprocess.Popen(['lscpu'], stdout = subprocess.PIPE)
    b = subprocess.run(['grep', 'Arthitecture'], stdin = a.stdout,
            stdout=subprocess.PIPE, encoding = 'utf-8')
    answer += b.stdout +"\n"
    if platform.system() == 'Linux':
        a = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE)
        b = subprocess.Popen(['grep', 'Model name'], stdin=a.stdout,
                stdout=subprocess.PIPE)
        answer += b.stdout.read().decode()

    a = subprocess.Popen(['lscpu'], stdout=subprocess.PIPE)
    mem = subprocess.run(['grep', 'cache:'], stdin = a.stdout,
            stdout=subprocess.PIPE, encoding='utf-8')
    answer += "\n" + mem.stdout
    return answer + "\n\n"

def getPhysicalMem():
    answer = ''
    tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    answer += 'Kapasitas Total: ' + str(tot_m)
    answer += '\nKapasitas yang telah digunakan: ' + str(used_m)
    answer += '\nKapasitas yang tersisa: ' + str(free_m)
    return answer

def getSwapMem():
    answer = ''
    answer += 'Kapasitas total: ' + str(psutil.swap_memory().total >>20) +' MB'
    answer += '\nKapasitas yang telah digunakan: ' + str(psutil.swap_memory().used >>20) +' MB'
    answer += '\nKapasitas yang telah tersedia: ' + str(psutil.swap_memory().free >>20) +' MB'
    return answer

def getStorage():
    answer = ''
    total, used, free = shutil.disk_usage("/")
    answer += 'Kapasitas total ' + str(total//(2**30)) + ' GB'
    answer += '\nKapasitas yang telah digunakan: ' + str((used//2**30)) + ' GB'
    answer += '\nKapasitas yang kosong: '+ str((free//(2**30))) + ' GB'
    return answer

def checkConnection():
    host='http://google.com'
    try:
        urllib.urlopen(host)
        return 'connected'
    except:
        return 'no Internet!'

def logAccess():
    answer = ''
    answer += '\nList of success log'
    for i in success_cli:
        answer += '\n' + i

    answer += '\nList of failed log'
    for a in failed_cli:
        answer += '\n' + a
    return answer
    

# thread fuction
def threaded(c,a,b):
    while True:

        # data received from client
        data = c.recv(1024).decode('utf-8')
        if not data:
            print('Bye')
            # lock released on exit
            print_lock.release()
            break

        # reverse the given string from client
        elif data == 'i':
            c.send(getHardware().encode('utf-8'))
            success_cli.append(str(a) + ' ' +str(b))
        elif data == 'm':
            c.send(getPhysicalMem().encode('utf-8'))
            success_cli.append(str(a) + ' ' +str(b))
        elif data == 'w':
            c.send(getSwapMem().encode('utf-8'))
            success_cli.append(str(a) + ' ' +str(b))
        elif data == 'g':
            c.send(getStorage().encode('utf-8'))
            success_cli.append(str(a) + ' ' +str(b))
        elif data == 'c':
            c.send(checkConnection().encode('utf-8'))
            success_cli.append(str(a) + ' ' +str(b))
        elif data == 'a':
            c.send(logAccess().encode('utf-8'))
            success_cli.append(str(a) + ' ' +str(b))
        else :
            answer = '\nSalah sintaks pak'
            c.send(answer.encode('utf-8'))
            failed_cli.append(str(a) + ' ' +str(b))

        # connection closed
    c.close()


def Main():
    host = ""
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
    
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,addr[0],addr[1]))
    s.close()


if __name__ == '__main__':
    Main()
