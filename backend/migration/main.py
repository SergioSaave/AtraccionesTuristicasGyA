import subprocess

# Ejecutar el script para cargar la red vial
#print("Ejecuto la carga de datos (load_prueba.py)...")
#subprocess.run(["python", "load_prueba.py"], check=True)

# Ejecutar el script de optimización con CPLEX
print("Ejecutado optimización con CPLEX (cplex_alg_prueba.py)...")
subprocess.run(["python", "cplex_alg_prueba.py"], check=True)  # Ajusta los argumentos según sea necesario
