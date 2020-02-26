print ("--------------------------------------------------------")
print("......    BIENVENIDO A LA TORNILLERÍA DE ARTIÑO    .....")
print ("--------------------------------------------------------")

print("     PRECIOS:")
print("         1 tornillo(perno) - 5 centavos")
print("         1 tuerca - 3 centavos")
print("         1 arandela - 1 centavo")

tornillos = int(input("Por favor ingrese los tornillos que necesita: \n   "))
tuercas = int(input("Por favor ingrese las tuercas que necesita: \n   "))
arandelas = int(input("Por favor ingrese las arandelas que necesita: \n   "))


preciotornillos = tornillos * 5
preciotuercas = tuercas*3
precioarandelas = arandelas*1

total = preciotornillos + preciotuercas + precioarandelas

if tuercas < tornillos:
    print("-----------------------------------------------------")
    print("     Compruebe la orden. Hay más tuercas que tornillos.")
else:
    print("-----------------------------------------------------")
    print("     La orden está bien.")

print("     El total es: ",total)

