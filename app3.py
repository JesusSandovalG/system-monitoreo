import psutil
import time
import csv
import json
from datetime import datetime
import matplotlib.pyplot as plt

# punto para alertas
CPU_THRESHOLD = 80  # limite, porcentaje de CPU recomendado
RAM_THRESHOLD = 70  # limite, porcentaje de RAM recomendado

# funcion nombre de proceso que mas consume en sistema
def get_top_process():
    processes = []
    for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # procesos de CPU y de RAM
    top_cpu = max(processes, key=lambda p: p["cpu_percent"])
    top_ram = max(processes, key=lambda p: p["memory_percent"])
    return top_cpu, top_ram

# funcion de datos (logs) a CSV
def export_to_csv(logs, filename='system_logs.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPU Usage (%)", "RAM Usage (%)", "Disk Usage (%)", 
                         "Network Sent (MB)", "Network Received (MB)", 
                         "Top CPU Process", "Top RAM Process"])
        writer.writerows(logs)

# funcion de datos (logs) a JSON
def export_to_json(logs, filename='system_logs.json'):
    data = [
        {
            "Timestamp": log[0],
            "CPU Usage (%)": log[1],
            "RAM Usage (%)": log[2],
            "Disk Usage (%)": log[3],
            "Network Sent (MB)": log[4],
            "Network Received (MB)": log[5],
            "Top CPU Process": log[6],
            "Top RAM Process": log[7],
        }
        for log in logs
    ]
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# funcion de uso de recursos
def plot_usage(logs):
    timestamps = [log[0] for log in logs]
    cpu_usage = [log[1] for log in logs]
    ram_usage = [log[2] for log in logs]
    
    plt.figure(figsize=(10, 6))
    
    # empieza grafica
    # movimientos personalizacion
    plt.plot(timestamps, cpu_usage, label="Uso de CPU (%)", color="black", marker='o')
    plt.plot(timestamps, ram_usage, label="Uso de RAM (%)", color="black", marker='x')
    
    # lineas de porcentajes recomendados
    plt.axhline(y=CPU_THRESHOLD, color="green", linestyle="--", label=f"Porcentaje recomendado de uso de CPU ({CPU_THRESHOLD}%)")
    plt.axhline(y=RAM_THRESHOLD, color="blue", linestyle="--", label=f"Porcentaje recomendado de uso de RAM ({RAM_THRESHOLD}%)")
    
    # textos, tamano, y show para mostrar grafica
    plt.xticks(rotation=45)
    plt.xlabel("Fecha y Tiempo")
    plt.ylabel("Uso (%)")
    plt.title("Uso de CPU y RAM con límites recomendados")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()

# funcion principal, lo que va mostrando en la consola
def monitor_system():
    logs = []
    print("Iniciando chequeo de recursos del sistema (Ctrl+C para salir)...\n")
    try:
        while True:
            # informes del sistema
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            net_io = psutil.net_io_counters()
            net_sent = net_io.bytes_sent / (1024 ** 2)  # necesario convertir a MB
            net_recv = net_io.bytes_recv / (1024 ** 2)  # necesario convertir a MB
            
            # hora actual, datetime now y le ponemos el formato que es
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # con un top, como lo visto en clase, tenemos los procesos que consumen mas memoria y mas cpu
            top_cpu, top_ram = get_top_process()
            top_cpu_info = f"{top_cpu['name']} (PID {top_cpu['pid']} - {top_cpu['cpu_percent']}%)"
            top_ram_info = f"{top_ram['name']} (PID {top_ram['pid']} - {top_ram['memory_percent']}%)"
            
            # imprimir el informe, hora + datos, damos info general, pero en las graficas nos enfocamos en el uso de cpu y ram
            print(f"\n[{timestamp}] CPU: {cpu_usage}% | RAM: {ram_usage}% | Disco: {disk_usage}% | Red Enviada: {net_sent:.2f} MB | Red Recibida: {net_recv:.2f} MB")
            print(f"🔍 Proceso más consumidor de CPU: {top_cpu_info}")
            print(f"🔍 Proceso más consumidor de RAM: {top_ram_info}")

            # si se pasa el uso recomendado soltamos unas alertas
            if cpu_usage > CPU_THRESHOLD:
                print(f"⚠️ ALERTA: Uso de CPU alto ({cpu_usage}%)")
            if ram_usage > RAM_THRESHOLD:
                print(f"⚠️ ALERTA: Uso de RAM alto ({ram_usage}%)")

            # hora de guardar los logs
            logs.append([timestamp, cpu_usage, ram_usage, disk_usage, net_sent, net_recv, top_cpu_info, top_ram_info])

            # la exportacion se hara cada 5 registros
            if len(logs) % 5 == 0:
                export_to_csv(logs)
                export_to_json(logs)

            # para graficar tambien tomara en cuenta 5 registros
            if len(logs) % 5 == 0:  
                plot_usage(logs)

            time.sleep(3)  # saltos de 1 segundo
    except KeyboardInterrupt:
        print("\nMonitor detenido. Exportando logs...")
        export_to_csv(logs)
        export_to_json(logs)
        print("Logs exportados a 'system_logs.csv' y 'system_logs.json'. ¡Hasta luego!")

# ejecutar monitor o grafica
if __name__ == "__main__":
    monitor_system()

