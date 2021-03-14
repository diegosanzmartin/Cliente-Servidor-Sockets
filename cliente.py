#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal, select, socket, sys, os                                      #Funciones orientadas a conexión, sistema
from time import time                                                       #Cronometrar tiempos
from time import sleep

ERR = "\033[93m"
END = "\033[0m"

if __name__ == "__main__":
    if len(sys.argv) != 3 :                                                 #Esta función compara los tiempos para
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()

    #Variables socket
    servIP = sys.argv[1]
    servPort = int(sys.argv[2])
    server_address = (servIP, servPort)
    
    if servPort < 1023:                                                     #Comprobamos el nº de puerto
        print(ERR + "ERR: El nº de puerto debe ser mayor que 1023" + END)
        sys.exit()

    #Creación del socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Conexión socket
    sock.connect(server_address)

    while True:
        try:
            mss = input("Mensaje: ")
            sock.send(mss.encode())
        except KeyboardInterrupt:
            sys.exit()