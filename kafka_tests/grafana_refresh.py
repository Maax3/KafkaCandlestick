
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Configuración
GRAFANA_URL = os.getenv("GRAFANA_URL")
API_KEY = os.getenv("API_KEY")
DASHBOARD_UID =   # UID del dashboard que quieres actualizar
PANEL_ID = 1  # ID del panel específico
REFRESH_INTERVAL = 15  # Intervalo de actualización en segundos

# Función para actualizar el panel
def refresh_panel():
    url = f"{GRAFANA_URL}/api/annotations"
    headers = {
        'Authorization': f"Bearer {API_KEY}",
        'Content-Type': 'application/json'
    }
    payload = {
        "dashboardUid": DASHBOARD_UID,
        "panelId": PANEL_ID,
        "time": int(time.time() * 1000),  # Timestamp en milisegundos
        "text": "Actualización forzada"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("Panel actualizado correctamente")
    else:
        print(f"Error al actualizar el panel: {response.status_code}")

# Bucle para actualizar el panel en el intervalo definido
import time
while True:
    refresh_panel()
    time.sleep(REFRESH_INTERVAL)
