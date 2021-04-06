#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal, queue, select, socket, sys, os                               #Funciones orientadas a conexión, sistema, json y expresiones regulares
from time import time                                                       #Cronometrar tiempos
from time import sleep

ERR = "\033[93m"
END = "\033[0m"
BAR = "\n———————————————————————————————\n"

if __name__ == "__main__":
    if len(sys.argv) != 3 :                                                 
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

    sock.connect(serv_addr)                                                 #Establecemos conexión con el servidor

    inputs = [sys.stdin, sock]                                              #Lista de sockets de entrada
    outputs = [sock]                                                        #Lista de sockets de salida
    que = queue.Queue()                                                     #Creamos una cola

    mssNext = str.encode("")

    while True:
        try:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)     #Select coordina entre i/o

            for sck in readable:                                            #Sockets de entrada disponibles
                if sck == sys.stdin:                                        #Si detecta el teclado
                    mssIn = sys.stdin.readline()
                    mss = "->" + name + ": " + mssIn
                    que.put(mss.encode())

                elif sck == sock:                                           #Un nuevo socket desea conectarse
                    dataRecv = sock.recv(1024)
                    if dataRecv:
                        if dataRecv.decode("utf-8") != mssNext.decode("utf-8").strip("\n"): 
                            print(dataRecv.decode("utf-8"))
                    else:
                        sock.close()                                        #Cerramos el socket
                        print("Conexión finalizada")
                        sys.exit(0)

            for sck in writable:                                            #Sockets de salida disponibles
                if sck == sock:                                             #Un nuevo socket desea
                    try:
                        mssNext = que.get_nowait()                          #Devuelve la línea capturada en sys.stdin
                        sock.send(mssNext)
                    
                    except queue.Empty:
                        pass

            for sck in exceptional:                                         #Condiciones excepcionales
                if sck == sock:
                    sock.close()                                            #Cerramos el socket

        except KeyboardInterrupt:
            sock.close()
            sys.exit()