# 📦 Organizador de Guías SUNAT por Fecha y Placa

Este script automatiza la organización de guías de remisión generadas desde la plataforma SUNAT. Extrae información clave de cada archivo PDF (fecha de inicio de traslado y placa del vehículo) y clasifica los archivos en carpetas correspondientes.

---

## 🧠 ¿Qué problema resuelve?

Cuando se generan muchas guías diarias, organizarlas manualmente es lento y propenso a errores. Este script:

- Lee todos los archivos PDF en una carpeta.
- Extrae del contenido del PDF:
  - Fecha de inicio de traslado.
  - Placa del vehículo.
- Crea una estructura de carpetas automática:
  
/Julio_Quincena1/
├── 01.07.25/
│ └── ASG833/
│ └── [PDF]
---

## ▶️ ¿Cómo se usa?

1. Coloca todos los archivos PDF en una carpeta de entrada.
2. Ajusta la ruta en el script (`ruta_base = "C:\\Users\\frank\\Desktop\\GUIASGENEMI"`).
3. Ejecuta el script:

bash

python organizar_guias.py
