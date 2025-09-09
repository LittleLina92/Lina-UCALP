# version con seleccion previa de rondas y corte temprano

import random

#cantidad de rondas totales, se puede configurar
rondas_totales = int(input("Cuantas rondas jugamos? (las que quieras, pueden ser 500 xD ) "))
opciones = ["piedra", "papel", "tijera"]

print("¡Bienvenido! Vamos a jugar a Piedra, Papel o Tijera.")
print(f"Modo: mejor de {rondas_totales} (se corta antes si alguien ya no puede alcanzar).")
print("Escribí tu jugada (piedra/papel/tijera).")

ronda = 1
puntos_usuario = 0
puntos_pc = 0

while ronda <= rondas_totales:
    print(f"\nRonda {ronda}")

    #  NO cuenta la ronda hasta que sea un valor valido piedra,papel,tijera
    while True:
        jugada_usuario = input("Tu jugada: ").strip().lower()
        if jugada_usuario in opciones:
            break
        print("Entrada no válida. Debe ser piedra, papel o tijera.")

    jugada_pc = random.choice(opciones)
    print(f"La computadora eligió: {jugada_pc}")

    if jugada_usuario == jugada_pc:
        print("Empate.")
    elif (
        (jugada_usuario == "piedra" and jugada_pc == "tijera") or
        (jugada_usuario == "papel" and jugada_pc == "piedra") or
        (jugada_usuario == "tijera" and jugada_pc == "papel")
    ):
        print("¡Ganaste la ronda!")
        puntos_usuario += 1
    else:
        print("Perdiste la ronda.")
        puntos_pc += 1

    # check de corte temprano: si el rival ya no puede alcanzarte o no podes alcanzar al rival 
    rondas_restantes = rondas_totales - ronda
    if puntos_usuario > puntos_pc + rondas_restantes:
        print("\nCorte temprano: ya no te pueden alcanzar.")
        break
    if puntos_pc > puntos_usuario + rondas_restantes:
        print("\nCorte temprano: ya no podés alcanzarlos.")
        break

    ronda += 1

print("\n=== Resultado final ===")
print(f"Tus puntos: {puntos_usuario} | Puntos de la PC: {puntos_pc}")

if puntos_usuario > puntos_pc:
    print("¡Ganaste el juego! :D")
elif puntos_usuario < puntos_pc:
    print("La computadora ganó el juego :( ")
else:
    print("Empate total :/ .")


