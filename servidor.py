#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal, select, socket, sys, os                                      #Funciones orientadas a conexión, sistema
from time import time                                                       #Cronometrar tiempos
from time import sleep

ERR = "\033[93m"
END = "\033[0m"

if __name__ == "__main__":
    if len(sys.argv) != 2 :                                                 #Esta función compara los tiempos para
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()
    
    #Variables socket
    servIP = "127.0.0.1"
    servPort = int(sys.argv[1])
    serv_addr = (servIP, servPort)

    if servPort < 1023:                                                     #Comprobamos el nº de puerto
        print(ERR + "ERR: El nº de puerto debe ser mayor que 1023" + END)
        sys.exit()

    #Creación del socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Conexión socket
    sock.bind(serv_addr)

    sock.listen(1)                                                          #El socket está a la escucha del cliente
    listCli = [sock]                                                        #Lista con un solo socket como elemento

    while True:
        try:
            readCli, writeCli, exctCli = select.select(listCli, [], ())     #Select bloqueado con listCli

            for sck in readCli:
                if sck == sock:
                    cli, cli_add = sock.accept()
                    print("-Cliente:", cli_add)
                    listCli.append(cli)

                else:
                    dataRecv = sck.recvfrom(1024)
                    mss = dataRecv[0].decode()
                    lenMss = len(mss)

                    if lenMss > 0:
                        print("cli: ", mss)
                    
                    else:
                        print("-Cliente", cli_add, "desconectado")
                        sck.close()
                        listCli.remove(sck)
        
        except KeyboardInterrupt:
            sys.exit()