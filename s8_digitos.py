digitos = []
nummax_digito = 10 #10^9
#94 92 - 52 - 410
for d1 in range(nummax_digito):
    for d2 in range(nummax_digito):
        for d3 in range(nummax_digito):
            #print(str(d1)+" "+str(d2)+" "+str(d3))
            digitos.append(str(d1)+" "+str(d2)+" "+str(d3))

#9 4 9 2 - 5 2 - 4 10
nummax_digito = 100
digitos = []
for d1 in range(nummax_digito):
    for d2 in range(nummax_digito):
        for d3 in range(nummax_digito):
            digitos.append(str(d1)+" "+str(d2)+" "+str(d3))