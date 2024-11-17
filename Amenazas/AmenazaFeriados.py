import requests
import json

url = 'https://api.boostr.cl/holidays.json'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    with open('responseAmenazaFeriados.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print("El JSON ha sido descargado y guardado como 'respuesta.json'")
else:
    print(f"Error al realizar la solicitud. Código de estado: {response.status_code}")
