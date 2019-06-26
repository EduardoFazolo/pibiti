import logconversion as logconv
from pprint import pprint

filename = "Prod1Torno2.csv"


cases, atividadesDict, atividadeArrayString, atv_to_num = logconv.find_activicties_array_ids(filename)

atv_ocorridas = []

for c in cases:
    atv_ocorridas.append(c.Atividades)

with open("Arquivo.csv","w") as file:
    Linha1 = "Case ID;"
    for i in atividadeArrayString:
        Linha1 += i
        Linha1 += ";"
    file.write(Linha1 + "\n")
    for c in cases:
        temp = c.Atividades
        linha = str(c.ID) + ";"
        for i in range(len(atividadeArrayString)):
            if i in temp:
                linha += "1;"
            else:
                linha += "0;"
        file.write(linha + "\n")

file.close()
reajustes, producao, nProd = logconv.group_activities(atividadeArrayString)
prod = logconv.separate_times_by_groups(filename,[reajustes, producao])
arrayMedias, Mediainter = logconv.MediaMaker(prod)

with open("logPibic1.txt","w") as file:
    file.write("=========================================\n")
    for i in prod:
        file.write("ID: " + str(i.ID)+"\n")
        file.write("Manutencao: "+ str(i.manutencao) + "\n")
        file.write("Tipo :"+i.Tipo+"\n")
        file.write("Atividades: "+str(i.Atividades)+"\n")
        file.write("Tempo: "+str(i.Tempo)+"\n")
        file.write("Tamanho :"+str(i.Tamanho)+"\n")
        file.write("=========================================\n")
    for i,x in zip(arrayMedias,range(len(arrayMedias))):
        file.write("=========================================\n")
        file.write("Media " + str(x)+ ": " + str(i) + "\n")
        file.write("=========================================\n")
    file.write("Media Manutencao: "+ str(Mediainter) + "\n")
    print("Log Done!!!")
file.close()


menorTempo, vetMenorTempo = logconv.Filter([cases,nProd],1)
print("Melhor tempo filtro 1: "+ str(menorTempo))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,True)
print("Numero de peças ideal com filtro = " + str(pecas))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,False)
print("Numero de peças ideal sem filtro = " + str(pecas))

menorTempo, vetMenorTempo = logconv.Filter([cases,nProd,0.30],2)
print("Melhor tempo filtro 2: "+ str(menorTempo))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,True)
print("Numero de peças ideal com filtro = " + str(pecas))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,False)
print("Numero de peças ideal sem filtro = " + str(pecas))

menorTempo, vetMenorTempo = logconv.Filter([cases,producao,atividadesDict],3)
print("Melhor tempo filtro 3: "+ str(menorTempo))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,True)
print("Numero de peças ideal com filtro = " + str(pecas))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,False)
print("Numero de peças ideal sem filtro = " + str(pecas))

menorTempo, vetMenorTempo = logconv.Filter([cases,producao,atividadesDict,0.30],4)
print("Melhor tempo filtro 4: "+ str(menorTempo))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,True)
print("Numero de peças ideal com filtro = " + str(pecas))
pecas = logconv.NumeroProducaoIdeal(menorTempo,arrayMedias,Mediainter,False)
print("Numero de peças ideal sem filtro = " + str(pecas))
