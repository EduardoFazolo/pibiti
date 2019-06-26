import logconversion as logconv

filename = "Prod1Torno2.csv"
path = './data/'
nomes_atividades = logconv.FindAtividades(path+filename)
cases, num_to_atv, atividades, atv_to_num = logconv.find_activicties_array_ids(path+filename)

def agrupar_atividades(activities):

    print('\n=================================\n')
    print('Enumere as atividades')
    print('Atividades com o mesmo numero serao tradadas como parte do mesmo grupo')
    print('Se nenhum numero for digitado, as atividades serao separadas automaticamente')

    grupos = dict()

    for activity in activities:
        inpt = input('Atividade: ' + activity + ': ')
        if not inpt.isdigit():
            inpt = -99
        else:
            inpt = int(inpt)

        if len(grupos) == 0:                # Primeiro caso
            if inpt == -99:
                grupos[0] = [activity]      # Se o input for vazio, cria um grupo na posicao 0
            else:
                grupos[inpt] = [activity]   # Senão, cria o grupo desejado

        else:                               # Demais casos
            if inpt != -99:              # Se o usuario digitou um numero
                if inpt in list(grupos.keys()):   # Se o grupo já existe, adiciona a atividade ao grupo
                    grupos[inpt].append(activity)
                else:
                    grupos[inpt] = [activity] # Se não existe, crie um novo
            
            elif inpt == -99:
                grupos[int(list(grupos.keys())[-1]) + 1] = [activity]
    
    return grupos

def organizar_ordem_eventos(groups):

    nova_ordem = []

    for num,grupo in groups.items():
        print(grupo)
        if len(grupo) > 1:
            print("Enumere as atividades de acordo com a ordem que devem acontecer")
            for atv in grupo:
                i = input(atv + ": ")
                nova_ordem.append(int(i))
            novo_grupo = grupo.copy()
            for atv,i in zip(grupo, range(len(grupo))):
                novo_grupo[nova_ordem[i]] = atv

            nova_ordem = []
            groups[num] = novo_grupo

    print(groups)


def separar_series_temporais(grupos, casos):

    print("Numero de casos antes:" + str(len(casos)))

    deletees = []

    for caso in casos:
        for atv,i in zip(caso.Atividades, range(len(caso.DuracaoATV))):
            if num_to_atv[atv] in grupos[0]:
                caso.DuracaoProd += caso.DuracaoATV[i]
            else:
                caso.OffProcess.append(atv)
                caso.DuracaoAtvExtra.append(caso.DuracaoATV[i])

        if len(caso.DuracaoAtvExtra) == 0 and len(caso.Atividades) < 3:
            deletees.append(caso)
    
    for d in deletees:
        casos.remove(d)
    
    print("Numero de casos depois:" + str(len(casos)))

def gerar_csv_logIdeal():

    grupos = agrupar_atividades(nomes_atividades)
    print(grupos)
    separar_series_temporais(grupos, cases)
    output_name = 'ideal_' + filename

    with open(path + output_name,'w') as file:
        file.write('CASE_ID, Atividade, Duracao\n')
        for caso in cases:
            file.write(str(caso.ID) + ',Producao,'+ str(caso.DuracaoProd) + '\n')
            if len(caso.DuracaoAtvExtra) > 0:
                for c_id,c_dur in zip(caso.OffProcess, caso.DuracaoAtvExtra):
                    file.write(str(caso.ID) + ',' + str(num_to_atv[c_id]) + ',' + str(c_dur) + '\n')


grps = agrupar_atividades(atividades)
organizar_ordem_eventos(grps)
separar_series_temporais(grps, cases)