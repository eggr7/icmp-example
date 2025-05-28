import subprocess
import platform # Para identificar el sistema operativo y ajustar el comando ping

def hacer_ping(host_destino):
    """
    Envía un solo paquete ICMP Echo Request (ping) al host_destino
    y devuelve True si hay respuesta, False en caso contrario.
    """
    print(f"\n--- Haciendo ping a {host_destino} ---")

    # Parámetro para el número de pings a enviar.
    # En Windows es '-n', en Linux/macOS es '-c'.
    parametro_count = '-n' if platform.system().lower() == 'windows' else '-c'

    # Comando para ejecutar ping. Enviamos solo 1 paquete.
    # 'stdout=subprocess.PIPE' y 'stderr=subprocess.PIPE' ocultan la salida del comando en la consola.
    # 'text=True' decodifica la salida a string.
    comando = ['ping', parametro_count, '1', '-w', '1000', host_destino] # -w 1000 (1 segundo de timeout en ms para Windows)
    if platform.system().lower() != 'windows':
        comando = ['ping', parametro_count, '1', '-W', '1', host_destino] # -W 1 (1 segundo de timeout para Linux/macOS)


    try:
        # Ejecutamos el comando
        proceso = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)

        # Verificamos el código de retorno. 0 usualmente significa éxito.
        if proceso.returncode == 0:
            print(f"Respuesta recibida de {host_destino}")
            # print("Salida del comando:")
            # print(proceso.stdout)
            return True
        else:
            print(f"No se recibió respuesta de {host_destino} o hubo un error.")
            # print("Error (si lo hubo):")
            # print(proceso.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"El comando ping a {host_destino} excedió el tiempo de espera.")
        return False
    except FileNotFoundError:
        print("Error: El comando 'ping' no se encontró. Asegúrate de que esté instalado y en el PATH.")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return False

# --- Ejemplos de Uso ---
# Un host que probablemente responderá
host_existente = "8.8.8.8"  # DNS de Google
hacer_ping(host_existente)

# Un host en una red local privada que probablemente no exista o no responda
# (para ver el caso de fallo)
host_inexistente = "192.168.10.250" 
hacer_ping(host_inexistente)

# También se puede probar con un nombre de dominio 
host_dominio = "www.google.com"
hacer_ping(host_dominio)