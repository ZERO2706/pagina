import paramiko
import os
import datetime

# Configuración SFTP
SFTP_HOST = "192.168.1.249"
SFTP_PORT = 8022
SFTP_USER = "usr_alfin"
SFTP_PASSWORD = "+6oM;{YQQpi&*"
SFTP_REMOTE_PATH = "/IN/ASIGNACION/"

# Rutas locales
ruta_asignacion_1 = r"\\192.168.1.249\Compartido\compartido_Refinansa_2022\Alfin\2025\Mayo_2025\Asignacion diaria"
ruta_asignacion_2 = r"\\192.168.1.249\Compartido\compartido_Refinansa_2022\Alfin\2025\Mayo_2025\Asignacion_dxd"
RUTAS_LOCALES = [ruta_asignacion_1, ruta_asignacion_2]

# Eliminar archivos .txt existentes en Asignacion_dxd
for archivo in os.listdir(ruta_asignacion_2):
    if archivo.endswith(".txt"):
        try:
            os.remove(os.path.join(ruta_asignacion_2, archivo))
            print(f"Eliminado antiguo: {archivo}")
        except Exception as e:
            print(f"No se pudo eliminar {archivo}: {e}")

# Obtener fecha actual en formato YYMMDD
fecha_hoy = datetime.datetime.now().strftime("%Y%m%d")

# Archivos a descargar
archivos_a_descargar = [
    f"BASE_ASIG_REFINANSA_G1_{fecha_hoy}.txt",
    f"BASE_ASIG_REFINANSA_G2_{fecha_hoy}.txt"
]

# Asegurar que las carpetas de destino existen
for ruta in RUTAS_LOCALES:
    os.makedirs(ruta, exist_ok=True)

# Conexión SFTP y descarga
try:
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)

    for archivo in archivos_a_descargar:
        remote_file = SFTP_REMOTE_PATH + archivo

        try:
            # Descargar archivo desde SFTP
            with sftp.file(remote_file, 'r') as remote_f:
                contenido = remote_f.read()

            for ruta in RUTAS_LOCALES:
                local_file = os.path.join(ruta, archivo)
                with open(local_file, 'wb') as local_f:
                    local_f.write(contenido)
                print(f"Guardado en: {local_file}")

        except FileNotFoundError:
            print(f"No encontrado en SFTP: {archivo}")

    sftp.close()
    transport.close()
except Exception as e:
    print(f"Error en la conexión SFTP: {e}")