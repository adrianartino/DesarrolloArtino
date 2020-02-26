import math;
print("-------------------------------------------------------------")
print("                         PROBLEMA 4                          ")
print("                  ÍNDICE DE SENSACIÓN TÉRMICA                ")
print("-------------------------------------------------------------")

velocidadviento = float(input("     Ingresa la velocidad del viento en millas:\n        "))

temperatura = float(input("     Ingresa la temperatura en grados Fahrenheit:\n        "))

if(velocidadviento >=0 and velocidadviento <= 4):
    print("El índice de senación térmica es: ",temperatura," grados.")
elif(velocidadviento >= 45):
    sensacion = (1.6*temperatura) - 55
    print("El índice de senación térmica es: ",sensacion," grados.")
elif(velocidadviento >4 and velocidadviento < 45):
    sensacion2 = 91.4 + (91.4 - temperatura)*(0.0203 * (math.sqrt (velocidadviento) - 0.474))
    print("El índice de senación térmica es: ",sensacion2," grados.")