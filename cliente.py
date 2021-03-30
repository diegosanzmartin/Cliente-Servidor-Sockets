#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal, queue, select, socket, sys, os                                      #Funciones orientadas a conexión, sistema
from time import time                                                       #Cronometrar tiempos
from time import sleep

ERR = "\033[93m"
END = "\033[0m"
BAR = "\n———————————————————————————————\n"

if __name__ == "__main__":
    if len(sys.argv) != 3 :                                                 #Esta función compara los tiempos para
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()

    #Variables socket
    servIP = sys.argv[1]
    servPort = int(sys.argv[2])
    serv_addr = (servIP, servPort)
    
    if servPort < 1023:                                                     #Comprobamos el nº de puerto
        print(ERR + "ERR: El nº de puerto debe ser mayor que 1023" + END)
        sys.exit()

    name = ""
    while len(name) <= 0:
        name = input("Nombre: ")

    #Creación del socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Conexión socket

    print(BAR, "Conectando con %s:%s" % serv_addr, BAR)

    sock.connect(serv_addr)

    inputs = [sys.stdin, sock]
    outputs = [sock]
    que = queue.Queue()

    mssNext = str.encode("")

    while True:
        try:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)

            for sck in readable:
                if sck == sys.stdin:
                    mssIn = sys.stdin.readline()
                    mss = "->" + name + ": " + mssIn
                    que.put(mss.encode())

                elif sck == sock:
                    dataRecv = sock.recv(1024)
                    if dataRecv:
                        if dataRecv.decode("utf-8") != mssNext.decode("utf-8").strip("\n"):
                            print(dataRecv.decode("utf-8"))
                    else:
                        sock.close()
                        print("Conexión finalizada")
                        sys.exit(0)

            for sck in writable:
                if sck == sock:
                    try:
                        mssNext = que.get_nowait()
                        sock.send(mssNext)
                    
                    except queue.Empty:
                        pass

            for sck in exceptional:
                if sck == sock:
                    sock.close()

        except KeyboardInterrupt:
            sock.close()
            sys.exit()