import requests
import time
import json

# URL del endpoint
url = "http://127.0.0.1:5000/buscar-museo"
params = {'nombre_museo': 'Parque Bicentenario'}

# Tiempo máximo de espera en segundos
max_wait_time = 60  # Puedes ajustar este valor
interval = 30  # Intervalo entre reintentos en segundos
elapsed_time = 0

while elapsed_time < max_wait_time:
    try:
        # Realizar la solicitud GET
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanzar un error si la respuesta es mala

        # Guardar la respuesta en un archivo JSON
        with open('metadataGPT.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)

        print("El JSON se ha guardado exitosamente.")
        break  # Salir del bucle si la solicitud es exitosa

    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}. Intentando de nuevo en {interval} segundos...")
        time.sleep(interval)  # Esperar antes de reintentar
        elapsed_time += interval  # Incrementar el tiempo transcurrido

if elapsed_time >= max_wait_time:
    print("Se agotó el tiempo de espera para realizar la solicitud.")
