import socket

#Esta funcion escanea puertos TCP en un rango aclarado de una direccion IPv4 especificada.
#Este script no tiene threading, por lo que escanea los puertos de uno en uno y puede ser muy lento si se analizan varios puertos.

def scan_ports(target_ip, start_port, end_port):
    print("Escaneando", target_ip, "desde el puerto", start_port, "hasta", end_port)
    #Se crea una lista para almacenar los puertos abiertos.
    open_ports = list()
    for port in range(start_port, end_port + 1):
        #Esto es importante para ver el progreso del escaneo.
        print("Escaneando puerto", port)
        #Se crea un socket para cada puerto e intenta conectarse.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            #Se establece un tiempo limite para realizar la conexion.
            sock.settimeout(0.5)
            #Se intenta conectar al puerto especificado.
            result = sock.connect_ex((target_ip, port))
            #Si no hay error (result == 0), el puerto esta abierto.
            if result == 0:
                # Se agrega el puerto a la lista de puertos abiertos.
                print("Puerto", port, "abierto")
                open_ports.append(port)
    if open_ports:
        print("Puertos abiertos:", open_ports)
    else:
        print("No se encontraron puertos abiertos.")

#Esto asegura que el script se ejecute solo si se ejecuta directamente.
if __name__ == "__main__":
    ip = input("Cual IPv4 quieres escanear? ")
    start_port = int(input("Desde que puerto quieres empezar? "))
    end_port = int(input("Hasta que puerto quieres escanear? "))
    scan_ports(ip, start_port, end_port)