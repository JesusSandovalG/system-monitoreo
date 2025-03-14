Este script monitorea el uso del sistema en tiempo real, registrando métricas como el uso de CPU, RAM, disco y red. Además, identifica los procesos que consumen más recursos y almacena la información en formatos CSV y JSON.

Características:
- Monitoreo en tiempo real de CPU, RAM, disco y red.
- Detección de procesos con mayor consumo de CPU y RAM.
- Exportación de logs a CSV y JSON cada 5 registros.
- Alertas visuales cuando el uso de CPU o RAM supera los límites recomendados.
- Gráficas del uso de CPU y RAM con límites recomendados.

Instalación:
- Asegúrate de tener Python 3 instalado.
- Instala las dependencias necesarias con:
bash
pip install psutil matplotlib
python monitor.py
