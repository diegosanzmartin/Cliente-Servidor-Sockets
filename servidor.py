#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal, select, socket, sys, os, re                                      #Funciones orientadas a conexión, sistema, json y expresiones regulares
from time import time                                                           #Cronometrar tiempos
from time import sleep

ERR = "\033[93m"
END = "\033[0m"

if __name__ == "__main__":
    if len(sys.argv) != 2 :                                                     
        print(ERR + "ERR: Nº de argumentos no válidos" + END)
        sys.exit()
    
    #Variables socket
    servIP = "127.0.0.1"
    servPort = int(sys.argv[1])
    serv_addr = (servIP, servPort)

    if servPort < 1023:                                                         #Comprobamos el nº de puerto
        print(ERR + "ERR: El nº de puerto debe ser mayor que 1023" + END)
        sys.exit()

    #Creación del socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)                                                         #Establecemos modo no bloqueo

    #Conexión socket
    sock.bind(serv_addr)

    sock.listen(10)                                                             #El socket está a la escucha del cliente
    inputs = [sock]                                                             #Lista de sockets de lectura
    outputs = []                                                                #Lista de sockets de escritura
    clientes = {}                                                               #Lista de clientes  
    nCli = 0

    while True:
        try:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)     #Select coordina entre i/o

            for sck in readable:                                                #Sockets de entrada disponibles
                if sck == sock:                                                 #Un nuevo socket desea conectarse                                        
                    cli, cli_add = sock.accept()                                #Aceptamos la conexión de un socket "readable"
                    cli.setblocking(0)                                          #Establecemos modo no bloqueo
                    print("-Cliente:", cli_add)

                    inputs.append(cli)                                          #Añadimos al final la lista inputs
                    outputs.append(cli)                                         #Añadimos al final la lista outputs

                    clientes[cli] = "cli" + str(nCli)
                    cliName = clientes[cli]
                    nCli += 1

                    for s in outputs:
                        mss = "->Server: Nuevo usuario" + str(cli_add)
                        s.send(mss.encode())                                    #Avisamos del nuevo usuario

                else:
                    dataRecv = sck.recv(1024)
                    if dataRecv:
                        dataRecv = dataRecv.strip().decode('utf-8')
                        print(dataRecv)
                        for s in outputs:
                            s.send(dataRecv.encode())                           #Reenviamos mensaje a todos los clientes

                    else:
                        outputs.remove(sck)                                     #Eliminamos el socket de la lista de outputs
                        inputs.remove(sck)                                      #Eliminamos el socket de la lista de inputs
                        sck.close()

                        for s in outputs:
                            mss = "->Server: " + str(cli_add) + " desconectado"
                            s.send(mss.encode())                                #Avisamos de usuario desconectado


            for sck in exceptional:                                             #Condiciones excepcionales
                inputs.remove(sck)                                              #Eliminamos el socket de la lista de inputs
                outputs.remove(sck)                                             #Eliminamos el socket de la lista de outputs
                sck.close()                                                     #Cerramos el socket
        
        except KeyboardInterrupt:
            print("\nCerrando conexión con clientes")
            sys.exit()