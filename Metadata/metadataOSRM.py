import requests
import json

# Coordenadas de actividades en formato lat,long
activities = [
    "-33.4489,-70.6693",  # Ejemplo: Santiago
    "-33.4569,-70.6483",  # Ejemplo: Plaza de Armas
    "-33.4691,-70.6410"   # Ejemplo: Cerro San Cristóbal
]

# Función para calcular el tiempo y la ruta utilizando la API de OSRM
def calcular_ruta(activities):
    total_time = 0
    routes = []
    
    for i in range(len(activities) - 1):
        coord1 = activities[i].split(',')
        coord2 = activities[i + 1].split(',')

        # Llamada a la API de OSRM para calcular el tiempo de viaje
        url = f"http://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=false"
        print(url)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if 'routes' in data and len(data['routes']) > 0:
                travel_time = data['routes'][0]['duration'] / 60  # Convertir a minutos
                total_time += travel_time
                
                # Agregar la ruta al resultado
                routes.append({
                    "start": activities[i],
                    "end": activities[i + 1],
                    "duration": travel_time,
                    "geometry": data['routes'][0].get('geometry', None)  # Guardar la geometría de la ruta si está disponible
                })
            else:
                print(f"No se encontraron rutas entre {coord1} y {coord2}.")
        else:
            print(f"Error al calcular la ruta entre {coord1} y {coord2}: {response.status_code} - {response.text}")

    return {
        "total_time": round(total_time, 2),
        "routes": routes
    }

# Calcular las rutas
resultado = calcular_ruta(activities)

# Guardar la respuesta JSON en un archivo
with open('metadataOSRM.json', 'w') as json_file:
    json.dump(resultado, json_file, indent=4, ensure_ascii=False)

print("El JSON con el tiempo y las rutas se ha guardado como metadataOSRM.json.")
