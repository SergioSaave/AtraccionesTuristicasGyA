import os
import subprocess
import threading
import time

# Obtiene el directorio actual donde se está ejecutando el script
current_directory = os.getcwd()

# Define las carpetas hijas relativas a la ubicación actual del script
pnpm_project_dir = os.path.join(current_directory, "Sitio Web/frontend")
docker_project_dir = os.path.join(current_directory, "Sitio Web/backend/migration")
flask_app_path = os.path.join(current_directory, "Sitio Web/backend/app.py")
amenaza_clima_path = os.path.join(current_directory, "Amenazas/AmenazaClima.py")

def run_pnpm_commands():
    try:
        # Cambia al directorio del proyecto con pnpm
        os.chdir(pnpm_project_dir)
        print(f"Cambiando a directorio: {os.getcwd()}")

        # Ejecuta pnpm install
        print(f"Ejecutando pnpm install en {pnpm_project_dir}...")
        pnpm_install = subprocess.Popen(
            ["pnpm", "install"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Captura y muestra la salida del comando
        for line in pnpm_install.stdout:
            print(f"[PNPM] {line.strip()}")
        for line in pnpm_install.stderr:
            print(f"[PNPM ERROR] {line.strip()}")

        pnpm_install.wait()  # Espera a que termine el proceso de instalación

        # Ejecuta pnpm run dev
        print("Ejecutando pnpm run dev...")
        pnpm_run = subprocess.Popen(
            ["pnpm", "run", "dev"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Captura y muestra la salida del comando
        for line in pnpm_run.stdout:
            print(f"[PNPM] {line.strip()}")
        for line in pnpm_run.stderr:
            print(f"[PNPM ERROR] {line.strip()}")
        
        pnpm_run.wait()  # Espera a que termine el proceso de ejecución

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar un comando de pnpm: {e}")
    except Exception as e:
        print(f"Error general: {e}")

def run_docker_compose():
    try:
        # Cambia al directorio del proyecto con docker-compose
        os.chdir(docker_project_dir)
        print(f"Cambiando a directorio: {os.getcwd()}")

        # Ejecuta docker-compose up
        print(f"Ejecutando docker-compose up en {docker_project_dir}...")
        docker_process = subprocess.Popen(
            ["docker-compose", "up"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Captura y muestra la salida del comando
        for line in docker_process.stdout:
            print(f"[DOCKER] {line.strip()}")
        for line in docker_process.stderr:
            print(f"[DOCKER ERROR] {line.strip()}")
        
        docker_process.wait()  # Espera a que el proceso de docker termine

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar docker-compose: {e}")
    except Exception as e:
        print(f"Error general: {e}")

def run_flask_app():
    try:
        # Cambia al directorio del proyecto de Flask
        os.chdir(os.path.dirname(flask_app_path))  # Cambia al directorio de la app
        print(f"Cambiando a directorio: {os.getcwd()}")

        # Ejecuta pip install para instalar las dependencias necesarias
        print("Instalando dependencias de Flask...")
        pip_install = subprocess.Popen(
            ["pip3", "install", "flask", "requests", "numpy"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Captura y muestra la salida del comando
        for line in pip_install.stdout:
            print(f"[PIP] {line.strip()}")
        for line in pip_install.stderr:
            print(f"[PIP ERROR] {line.strip()}")
        
        pip_install.wait()  # Espera a que termine el proceso de instalación

        # Ejecuta la app de Flask
        print(f"Ejecutando Flask app en {flask_app_path}...")
        flask_process = subprocess.Popen(
            ["python3", "app.py"],  # O "python", dependiendo de tu instalación
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Captura y muestra la salida del comando
        for line in flask_process.stdout:
            print(f"[FLASK] {line.strip()}")
        for line in flask_process.stderr:
            print(f"[FLASK ERROR] {line.strip()}")
        
        flask_process.wait()  # Espera a que termine el proceso de Flask

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar la app de Flask: {e}")
    except Exception as e:
        print(f"Error general: {e}")

def run_amenaza_clima():
    try:
        # Cambia al directorio donde se encuentra el script de AmenazaClima
        os.chdir(os.path.dirname(amenaza_clima_path))
        print(f"Cambiando a directorio: {os.getcwd()}")

        # Ejecuta el script AmenazaClima.py
        print(f"Ejecutando script de AmenazaClima en {amenaza_clima_path}...")
        clima_process = subprocess.Popen(
            ["python3", "AmenazaClima.py"],  # O "python", dependiendo de tu instalación
            ["python3", "AmenazaFeriados.py"],  # O "python", dependiendo de tu instalación
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Captura y muestra la salida del comando
        for line in clima_process.stdout:
            print(f"[AMENAZA CLIMA] {line.strip()}")
        for line in clima_process.stderr:
            print(f"[AMENAZA CLIMA ERROR] {line.strip()}")
        
        clima_process.wait()  # Espera a que termine el proceso de AmenazaClima

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el script de AmenazaClima: {e}")
    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    # Ejecutar la función de pnpm en un hilo
    pnpm_thread = threading.Thread(target=run_pnpm_commands)
    pnpm_thread.start()  # Iniciar el hilo de pnpm

    # Esperar 2 segundos antes de iniciar el hilo de docker
    time.sleep(2)

    # Ejecutar la función de docker-compose en un hilo
    docker_thread = threading.Thread(target=run_docker_compose)
    docker_thread.start()  # Iniciar el hilo de docker
    
    time.sleep(2)

    # Ejecutar la función de Flask en un hilo
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()  # Iniciar el hilo de Flask
    
    time.sleep(2)

    # Ejecutar el script de AmenazaClima en un hilo
    amenaza_thread = threading.Thread(target=run_amenaza_clima)
    amenaza_thread.start()  # Iniciar el hilo de AmenazaClima

    # Esperar a que todos los hilos terminen
    amenaza_thread.join()
    pnpm_thread.join()
    docker_thread.join()
    flask_thread.join()

    print("Tareas completadas.")
