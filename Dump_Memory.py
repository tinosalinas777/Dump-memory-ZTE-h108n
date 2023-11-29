#!/usr/bin/env python3


import serial
import time 

# Configurar el puerto serial
puerto = "/dev/ttyUSB0"  # Reemplaza con tu puerto UART especifico en sistemas basados en linux o windows
baudios = 115200

ser = serial.Serial(puerto, baudios, timeout=5)

nombre_archivo = "dumpMemory_uart.txt"   #este es el nombre del archivo que creara para guardar el dump

def enviar_comando(serial, comando):
    serial.write(comando.encode('utf-8'))

try:
    with open(nombre_archivo, 'w') as archivo:
        
        direccion_memoria = 0xb2000000  # Direccion de memoria inicial
        incremento = 0x00000100  # Valor de incremento, es 256 en decimal ya que cuenta con 256 sectores
        direccion_limite=0xb2ff00f0 #direccion final a leer obtenida con elcomando flfinfo

        while direccion_memoria <= direccion_limite:
            time.sleep(0.2)
            # Enviar comando para leer desde la direccion de memoria actual
            comando = f"md {hex(direccion_memoria)}\n"
            enviar_comando(ser, comando)

            # Leer datos desde el puerto serial
            datos_recibidos = ser.readline().decode('utf-8').rstrip()
            if "RTL8676#" not in datos_recibidos:                      #aca se fija el prompt y no lo guarda
                if datos_recibidos:
                 print(f" {datos_recibidos}")

                 # Escribir datos en el archivo
                 archivo.write(f" {datos_recibidos}\n")

                 # Incrementar direccion de memoria
                 direccion_memoria += incremento

            

except KeyboardInterrupt:
    print("Interrupcion del usuario. Cerrando puerto serial.")
    ser.close()
