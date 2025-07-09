import os
import shutil
import fitz  # PyMuPDF
import re
from datetime import datetime
import time

base_destino = r"C:\Users\ADMIN\Desktop\GUIASGENEMI"
carpeta_origen = os.path.join(base_destino, "por_ordenar")

def obtener_quincena(fecha):
    dia = fecha.day
    mes_nombre = fecha.strftime('%B').capitalize()
    return f"{mes_nombre}_Quincena1" if dia <= 15 else f"{mes_nombre}_Quincena2"

regex_fecha = re.compile(r"Fecha de inicio de Traslado:\s*(\d{2}/\d{2}/\d{4})")
regex_placa_directa = re.compile(r"Principal:\s*([A-Z][A-Z0-9]{4,7})")
regex_placa_enlinea = re.compile(r"Principal:\s*Número de placa:\s*([A-Z][A-Z0-9]{4,7})")

def buscar_placa_flexible(texto):
    # Caso nuevo: Principal: Número de placa: ABC123
    match_enlinea = regex_placa_enlinea.search(texto)
    if match_enlinea:
        return match_enlinea.group(1)

    # Caso directo: Principal: ABC123
    match_directo = regex_placa_directa.search(texto)
    if match_directo:
        return match_directo.group(1)

    # Caso multilinea
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if "Principal" in linea:
            for j in range(i+1, min(i+5, len(lineas))):
                if "Número de placa" in lineas[j]:
                    for k in range(j+1, min(j+3, len(lineas))):
                        posible = lineas[k].strip()
                        if re.fullmatch(r"[A-Z][A-Z0-9]{4,7}", posible):
                            return posible
    return None

def intentar_copiar_archivo(origen, destino, intentos=3, espera=2):
    for i in range(intentos):
        try:
            shutil.copy2(origen, destino)
            return True
        except PermissionError:
            print(f"[INTENTO {i+1}] Archivo bloqueado, reintentando en {espera} segundos...")
            time.sleep(espera)
        except Exception as e:
            print(f"[ERROR] Otro problema al copiar: {e}")
            return False
    return False

procesados = 0
saltados = []

for archivo in os.listdir(carpeta_origen):
    if archivo.lower().endswith(".pdf"):
        ruta_pdf = os.path.join(carpeta_origen, archivo)

        try:
            with fitz.open(ruta_pdf) as doc:
                texto = ""
                for pagina in doc:
                    texto += pagina.get_text()

                match_fecha = regex_fecha.search(texto)
                if not match_fecha:
                    print(f"[ERROR] No se encontró fecha en {archivo}")
                    saltados.append(archivo)
                    continue
                fecha_obj = datetime.strptime(match_fecha.group(1), "%d/%m/%Y")
                carpeta_fecha = fecha_obj.strftime("%d.%m.%y")

                placa = buscar_placa_flexible(texto)
                if not placa:
                    print(f"[ERROR] No se encontró placa en {archivo}")
                    saltados.append(archivo)
                    continue

                quincena = obtener_quincena(fecha_obj)
                ruta_destino = os.path.join(base_destino, quincena, carpeta_fecha, placa)
                os.makedirs(ruta_destino, exist_ok=True)

                ruta_final = os.path.join(ruta_destino, archivo)

                if intentar_copiar_archivo(ruta_pdf, ruta_final):
                    print(f"[OK] {archivo} → {ruta_final}")
                    procesados += 1
                else:
                    print(f"[ERROR] No se pudo copiar {archivo} después de varios intentos")
                    saltados.append(archivo)

        except Exception as e:
            print(f"[ERROR] Falló el procesamiento de {archivo}: {e}")
            saltados.append(archivo)

print(f"\n--- RESUMEN ---")
print(f"Total procesados (copiados): {procesados}")
print(f"Saltados: {len(saltados)}")
if saltados:
    print("Archivos saltados:")
    for s in saltados:
        print(f" - {s}")

input("\nPresiona ENTER para salir...")