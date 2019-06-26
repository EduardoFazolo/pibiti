from datetime import datetime
import math
#from statsmodels.tsa.arima_model import ARIMA

DEBUG = False

#================================================================= Clases ====================================================       
class ClassCaseByID(object):
    def __init__(self,ID):
        self.ID = ID
        self.Atividades = []
        self.DuracaoATV = []
        self.DuracaoTotal = 0
    def SumDuracaoTotal(self):
        self.DuracaoTotal = 0
        for i in self.DuracaoATV:
            self.DuracaoTotal += i

class ClassPruducaoReajuste(object):
    def __init__(self,idd,Tipo,Atv,Dur,Tem,Tam,Intrup):
        self.ID = idd
        self.Tipo = Tipo
        self.Atividades = Atv
        self.Duraçoes = Dur
        self.Tempo = Tem
        self.Tamanho = Tam
        self.interrupt = Intrup
class ClassMedia(object):
    def __init__(self):
        self.tempo = 0
        self.tamanho = 0
#================================================================= Funçoes ====================================================
def FindAtividades(Arquivo):
    atividade = []
    count = 0
    with open(Arquivo,"r") as file:
        for line in file:
            if count != 0:
                partesLinhas = line.split(";")
                if not(partesLinhas[1] in atividade):
                    atividade.append(partesLinhas[1])
            count += 1
    file.close()
    return atividade

def find_activicties_array_ids(Arquivo):

    atvs = FindAtividades(Arquivo)
    at = dict()
    atividades = dict()

    for (a, i) in zip(atvs, range(0, len(atvs))):
        at[a] = i
    
    contador = 0
    linha = 0
    arrayID = []
    atividade = []
    with open(Arquivo,"r") as file:
        for line in file:
            if linha != 0:
                tempLine = line.split(";")
                if int(tempLine[0]) > contador :
                    tempClass = ClassCaseByID(int(tempLine[0]))
                    arrayID.append(tempClass)
                    contador += 1
                temp = arrayID[(int(tempLine[0])-1)]
                temp.Atividades.append(at[tempLine[1]])
                temp.DuracaoATV.append(int(tempLine[4]))

                if not(tempLine[1] in atividade):
                    atividade.append(tempLine[1])
            linha += 1    
    file.close()

    for (a, i) in zip(atividade, range(0, len(atividade))):
        atividades[i] = a

    return arrayID, atividades, atividade
                
def GetVetDuracaoTodasAtividades(arquivo,VetAtividades):
    count = 0
    VetorTempoAtividades = []
    for atv in VetAtividades:
        temp = ClassAtividade(atv)
        VetorTempoAtividades.append(temp)
    with open(arquivo) as file:
        for line in file:
            if count !=0:
                Lineparts = line.split(";")
                for atv in VetorTempoAtividades:
                    if atv.Nome == Lineparts[1]:
                        atv.Vetduracao.append(int(Lineparts[4]))
                        atv.TamanhoVetDuracao += 1
                        break
                
            count +=1
    file.close()
    return VetorTempoAtividades


def group_activities(activities):

    print('\n=================================\n')
    print('Producao: 1')
    print('Reajustes: 2')

    nProd = 0
    reajustes = []
    producao = []

    for activity in activities:
        inp = input('Activity: ' + activity + ': ')
        if(inp == '1'):
            producao.append(activity)
            nProd += 1
        elif(inp == '2'):
            reajustes.append(activity)
    

    return [reajustes, producao, nProd]

def separate_times_by_groups(arquivo, groups):

    reajustes = groups[0]
    producao = groups[1]
    prod_counter = 0
    tempo = 0
    atividadeExecutadas = []
    duracoesExecutadas = []
    count = 0
    interrupcao = False
    IDatual = 0
    IDanterior = 1
    interacao = 1.0
    arrayClassPruducaoReajuste = []
    interupt = 0
    
    with open(arquivo, 'r') as file:
        for line in file:
            if count !=0:
                lineparts = line.split(";")
                if(lineparts[1] in producao):
                    if(interrupcao == True):
                        if tempo != 0:
                            arrayClassPruducaoReajuste.append(ClassPruducaoReajuste(interacao,"Interrupcao",atividadeExecutadas,duracoesExecutadas,tempo,prod_counter,interupt))
                        interupt += 1
                        interacao = 0
                        tempo = 0
                        atividadeExecutadas = []
                        duracoesExecutadas = []
                        prod_counter = 0
                        #interacao = 0
                        interrupcao = False
                    # se o tempo não for nulo
                    IDatual = int(lineparts[0])
                    if(float(lineparts[4]) > 0 and IDatual == IDanterior):
                        tempo += float(lineparts[4])
                        prod_counter += 1.0
                        atividadeExecutadas.append(lineparts[1])
                        duracoesExecutadas.append(int(lineparts[4]))
                        interrupcao = False
                    elif(float(lineparts[4]) > 0 and IDatual != IDanterior):
                        if tempo != 0:
                            if interacao == 0:
                                interacao = 1
                            arrayClassPruducaoReajuste.append(ClassPruducaoReajuste(interacao,"Producao",atividadeExecutadas,duracoesExecutadas,tempo,prod_counter,interupt))
                        tempo = float(lineparts[4])
                        prod_counter = 1
                        atividadeExecutadas = [lineparts[1]]
                        duracoesExecutadas = [int(lineparts[4])]
                        interacao += 1
                        interrupcao = False
                        IDanterior = IDatual
                elif(lineparts[1] in reajustes):
                    if(interrupcao == False):
                        if tempo != 0:
                            arrayClassPruducaoReajuste.append(ClassPruducaoReajuste(interacao,"Producao",atividadeExecutadas,duracoesExecutadas,tempo,prod_counter,interupt))
                        IDanterior = IDatual
                        IDatual = int(lineparts[0])
                        tempo = float(lineparts[4])
                        prod_counter = 1
                        atividadeExecutadas = [lineparts[1]]
                        duracoesExecutadas = [int(lineparts[4])]
                        interacao += 1
                        
                        interrupcao = True
                    elif(interrupcao == True):
                        tempo += float(lineparts[4])
                        atividadeExecutadas.append(lineparts[1])
                        duracoesExecutadas.append(int(lineparts[4]))
                        prod_counter += 1.0
                        interrupcao = True

                
            count +=1
    file.close()
    return arrayClassPruducaoReajuste

def MediaMaker(arrayProd):
    arrayMedias = []
    arrayNum = []
    arrayInterupt = []
    maiorID = 0
    respMedia = []
    count = 0
    respMediaInte = 0
    for i in arrayProd:
        if(i.Tipo != "Interrupcao"):
            if i.ID > maiorID:
                arrayMedias.append(0)
                arrayNum.append(0)
                maiorID += 1
            if i.Tempo > 0:
                arrayMedias[int(i.ID) - 1] += i.Tempo
                arrayNum[int(i.ID) - 1] += 1
        else:
            arrayInterupt.append(i.Tempo)
            pass

    for x in range(len(arrayMedias)):
        respMedia.append(arrayMedias[x]/arrayNum[x])

    for i in arrayInterupt:
        respMediaInte += i
        count += 1
    respMediaInte = respMediaInte/count
    return respMedia,respMediaInte

def Filter(ToFilter,filterOption):
    if filterOption == 1: #filtra com base no numero de atividades de produção
        AtivityByID = ToFilter[0]
        porcentagem = float(ToFilter[1])
        tempos = []
        for i in AtivityByID:
            i.SumDuracaoTotal()
            tempos.append(i.DuracaoTotal)
        tempos.sort()
        melhorTempo = tempos[math.ceil(len(tempos)*porcentagem)]
        if(DEBUG):
            print("Tamanho Vet tempos= "+str(len(tempos)))
        return melhorTempo

    elif filterOption == 3:#metodo 1 porem com verificação de atividades executadas
        aproved = []
        vetMenorTempo = []
        AtivityByID = ToFilter[0]
        atvProd = ToFilter[1]
        atvdict = ToFilter[2]
        porcentagem = ToFilter[3]
        atvlen = len(atvProd)
        for i in AtivityByID:
            i.SumDuracaoTotal()
        for i in AtivityByID:
            fail = False
            temp = []
            for x in i.Atividades: 
                temp.append(atvdict[x])
            for y in range(len(temp)):
                if temp[y] != atvProd[y]:
                    fail = True
                    break
            if len(i.Atividades) != atvlen:
                fail = True
            if fail == False:
                aproved.append(i.DuracaoTotal)
        aproved.sort()
        if(DEBUG):
            print("Tamnho aproved= "+str(len(aproved)))
        menorTempo = aproved[(math.ceil(len(aproved)*porcentagem))]
        return menorTempo

def NumeroProducaoIdeal(menorTempo, arrayMedias, Mediainter, filterTimes):
    count = 0
    timeCount = 0.0
    if(DEBUG):
        print("Antes de cortar ="+str(len(arrayMedias)))
    if filterTimes == True:
        aproved = []
        for i in arrayMedias:
            if i >= menorTempo:
                aproved.append(i)
        arrayMedias = aproved
        if(DEBUG):
            print("Depois de cortar =" + str(len(arrayMedias)))
    for i in arrayMedias:
        timeCount += (i - menorTempo)
        count += 1
        if timeCount > Mediainter:
            count -= 1
            return count
    return count
