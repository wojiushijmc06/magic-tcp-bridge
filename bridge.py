#!/usr/bin/python

# -- coding:utf8 --

import socket
import threading
import time

# 这里填写本地监听的ip和端口

ip = '127.0.0.1'

port = 7002

# 这列填写公网ip和端口

send_ip = '192.168.6.43'

send_port = 6666

# 以下部分无需修改

outList = []

inList = []

outLock = False

inLock = False

runStation = True


def in_get(sock):
    global outLock, outList, inLock, inList, runStation

    while runStation:

        try:

            try:

                data = sock.recv(8192)

                time.sleep(0.1)

            except Exception as ie:

                print(str(ie))

                time.sleep(0.1)

            if len(data) <= 0:

                runStation = False


            elif data:
                # 收到非空数据时对数据进行关键字检索
                print("recvDataClient->>>>>>" + str(data))

                print(type(data))
                # 检索数据中是否包含cat
                if 'cat' in data:
                    # 如果包含cat，则对cat之后的数据进行定位
                    data = bytearray(data)
                    # 这里是定位数据中cat之后的第7位，下面相同
                    body = data.find(b'cat') + 7

                    arm = data.find(b'cat') + 9

                    foot = data.find(b'cat') + 18

                    tail = data.find(b'cat') + 28
                    # 这里对各个值进行判断（ascii）如果数据非0，则修改为0
                    if data[body] != 48 or data[arm] != 48 or data[foot] != 48 or data[tail] != 48:
                        data[body] = 48

                        data[arm] = 48

                        data[foot] = 48

                        data[tail] = 48

                        data = str(data)

                        print("fixDataClient->>>>>>>" + str(data))

                        print(type(data))

            while (outLock == True):

                time.sleep(0.01)

            else:

                outLock = True

                outList.append(data)

                outLock = False

        except Exception as err:

            print('inget' + str(err))


def in_out(sock):
    global outLock, outList, inLock, inList

    while runStation:

        try:

            if len(inList) != 0:

                while (inLock == True):

                    time.sleep(0.01)

                else:

                    inLock = True

                    for i in inList:
                        sock.send(i)

                    del inList[:]

                    inLock = False

            else:

                time.sleep(0.001)

        except Exception as err:

            print(err)


def out_get(sock):
    global outLock, outList, inLock, inList

    while runStation:

        try:

            data = sock.recv(8192)

            # print('recvDataServer->'+str(data))

            time.sleep(0.1)

            while (inLock == True):

                time.sleep(0.01)

            else:

                inLock = True

                inList.append(data)

                inLock = False

        except Exception as err:

            print('outget' + str(err))


def out_out(sock):
    global outLock, outList, inLock, inList

    while runStation:

        try:

            if len(outList) != 0:

                while (outLock == True):

                    time.sleep(0.01)

                else:

                    outLock = True

                    for i in outList:

                        if len(i) > 0:
                            sock.send(i)

                    del outList[:]

                    outLock = False

            else:

                time.sleep(0.001)

        except Exception as err:

            print(err)


def tcplink(sock, addr, ip, port):
    global runStation

    print('Accept new connection from %s:%s...' % addr)

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s1.connect((ip, port))

    inGet = threading.Thread(target=in_get, args=(sock,))

    inGet.start()

    inOut = threading.Thread(target=in_out, args=(sock,))

    inOut.start()

    inOut2 = threading.Thread(target=in_out, args=(sock,))

    inOut2.start()

    # inOut3 = threading.Thread(target=in_out, args=(sock,))

    # inOut3.start()

    outGet = threading.Thread(target=out_get, args=(s1,))

    outGet.start()

    outOut = threading.Thread(target=out_out, args=(s1,))

    outOut.start()

    outOut1 = threading.Thread(target=out_out, args=(s1,))

    outOut1.start()

    # outOut2 = threading.Thread(target=out_out, args=(s1,))

    # outOut2.start()

    while runStation:

        time.sleep(0.5)

    else:

        try:

            sock.close()

            s1.close()

        except Exception:

            pass

    print('Connection from %s:%s closed.' % addr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ip, port))

s.listen(5)

while True:
    sock1, addr = s.accept()

    runStation = True

    outList = []

    inList = []

    outLock = False

    inLock = False

    runStation = True

    t = threading.Thread(target=tcplink, args=(sock1, addr, send_ip, send_port))

    t.start()
