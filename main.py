import subprocess
import sys

def ejecutar_docker_compose():
    try:
        # Ejecutar el comando docker-compose up --build
        result = subprocess.run(['docker-compose', 'up', '--build'], check=True, capture_output=True, text=True)
        
        # Mostrar la salida del comando
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Manejar errores en la ejecución del comando
        print("Error al ejecutar docker-compose:")
        print(e.stderr)
        sys.exit(e.returncode)

if __name__ == '__main__':
    ejecutar_docker_compose()