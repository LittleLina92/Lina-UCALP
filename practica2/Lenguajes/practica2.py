import csv
import json
import os
from datetime import datetime

formato_fecha = "%Y-%m-%d %H:%M"
dias_nombres = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

def procesar_csv(nombre_archivo: str):

    conteo_dias = {}
    conteo_campeones = {}
    conteo_findesemana = {}
    campeones_por_dia = {}

    for dia in dias_nombres:
        campeones_por_dia[dia] = {}

    fechas = []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            timestamp = (fila.get("timestamp") or "").strip()
            campeon = (fila.get("campeon") or "").strip()

            fecha = datetime.strptime(timestamp, formato_fecha)
            fechas.append(fecha)

            dia = dias_nombres[fecha.weekday()]

            conteo_dias[dia] = conteo_dias.get(dia, 0) + 1
            conteo_campeones[campeon] = conteo_campeones.get(campeon, 0) + 1

            campeones_dia = campeones_por_dia[dia]
            campeones_dia[campeon] = campeones_dia.get(campeon, 0) + 1

            if dia in ("sábado", "domingo"):
                conteo_findesemana[campeon] = conteo_findesemana.get(campeon, 0) + 1

    total_registros = sum(conteo_dias.values())
    fechas.sort()
    dias_entre = (fechas[-1] - fechas[0]).days if fechas else 0

    dias_con_mas_sesiones = []
    if conteo_dias:
        maximo = max(conteo_dias.values())
        dias_con_mas_sesiones = [d for d, c in conteo_dias.items() if c == maximo]

    campeon_mas_entreno, cantidad_entrenamientos = (None, 0)
    if conteo_campeones:
        campeon_mas_entreno = max(conteo_campeones, key=conteo_campeones.get)
        cantidad_entrenamientos = conteo_campeones[campeon_mas_entreno]

    campeon_findesemana, cantidad_findesemana = (None, 0)
    if conteo_findesemana:
        campeon_findesemana = max(conteo_findesemana, key=conteo_findesemana.get)
        cantidad_findesemana = conteo_findesemana[campeon_findesemana]

    cantidad_dias_distintos = len(conteo_dias) if conteo_dias else 1
    promedio_entrenamientos_por_dia = {
        d: round(conteo_dias.get(d, 0) / cantidad_dias_distintos, 2) for d in dias_nombres
    }

    os.makedirs("salida", exist_ok=True)

    with open("salida/entrenamientos_por_campeon.csv", "w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(["campeon", "cantidad"])
        for campeon, cantidad in sorted(conteo_campeones.items()):
            escritor.writerow([campeon, cantidad])

    with open("salida/resumen_por_dia.json", "w", encoding="utf-8") as archivo_json:
        resumen = {
            "total_registros": total_registros,
            "por_dia": {d: conteo_dias.get(d, 0) for d in dias_nombres},
            "campeones_por_dia": campeones_por_dia
        }
        json.dump(resumen, archivo_json, ensure_ascii=False, indent=2)

    return {
        "total_registros": total_registros,
        "conteo_dias": conteo_dias,
        "dias_con_mas_sesiones": dias_con_mas_sesiones,
        "dias_entre": dias_entre,
        "campeon_mas_entreno": (campeon_mas_entreno, cantidad_entrenamientos),
        "campeon_findesemana": (campeon_findesemana, cantidad_findesemana),
        "promedio_entrenamientos_por_dia": promedio_entrenamientos_por_dia,
        "csv_generado": "salida/entrenamientos_por_campeon.csv",
        "json_generado": "salida/resumen_por_dia.json",
    }

def main():
    print("inicio del programa")
    resultado = procesar_csv("actividad_2.csv")

    print("resumen final")
    print("1. total de registros:", resultado["total_registros"])
    print("2. sesiones por día:", {d: resultado["conteo_dias"].get(d, 0) for d in dias_nombres})
    print("3. día o días con más sesiones:", resultado["dias_con_mas_sesiones"])
    print("4. días entre el primer y último entrenamiento:", resultado["dias_entre"])

    campeon_mas_entreno, cantidad_entrenamientos = resultado["campeon_mas_entreno"]
    print("5. el campeón que más entrenó fue:", campeon_mas_entreno, f"({cantidad_entrenamientos} entrenamientos)")

    campeon_findesemana, cantidad_findesemana = resultado["campeon_findesemana"]
    print("6. el campeón que más entrenó los fines de semana fue:", campeon_findesemana, f"({cantidad_findesemana} entrenamientos)")

    print("7. promedio de entrenamientos por día:", resultado["promedio_entrenamientos_por_dia"])
    print("8. archivo csv generado:", resultado["csv_generado"])
    print("9. archivo json generado:", resultado["json_generado"])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Ups! Error!:", e)
