from pandas import *

'''
define a classe OKR e tudo o que pode ser feito com ele: cadastrar, atualizar e monitorar
'''

class Okr:
    def __init__(self, id_user, user, id_time, time_user):
        self.id_user = id_user
        self.user = user
        self.id_time = id_time
        self.time_user = time_user

    def cadastrar_okr(self):
        """cadastra novo objetivo + n krs vinculados ao mesmo"""
        obj = read_csv('okr.csv')
        novo_id = obj['id_obj'].iloc[-1] + 1
        texto = input("digite seu novo objetivo:  ")
        setor = input("Digite o setor ao qual o OKR pertence:  ")
        responsavel = input("Digite o nome da pessoa responsável pelo OKR:  ")
        ano = input("Digite o ano de vigência do okr:  ")
        ciclo = input("Digite o ciclo de vigência do okr:  ")
        novo_obj = [novo_id, self.id_time, self.time_user, setor, texto, responsavel, ano, ciclo, self.today]
        obj.loc[len(obj)] = novo_obj
        print(novo_obj)

        n = int(input("\nQuantos KRs serão associados a este Objetivo?  "))
        for i in range(0, n):
            id_obj = novo_id
            krs = read_csv('krs.csv')
            id_kr = krs['id_kr'].iloc[-1] + 1
            texto = input("\nDigite o texto do KR:  ")
            tipo = input("Digite o tipo de KR [a/d/m]:  ")
            un_medida = input("Número absoluto ou porcentagem? [a/p]  ")
            inicial = int(input("Digite o número inicial do KR:  "))
            valor_alterar = int(input("Digite o valor a alterar:  "))
            status = 'novo'
            meta = 0
            atual = ''
            if tipo == 'a' and un_medida == 'a':
                meta = inicial + valor_alterar
            elif tipo == 'a' and un_medida == 'p':
                meta = inicial + (inicial * valor_alterar / 100)
            elif tipo == 'd' and un_medida == 'a':
                meta = inicial - valor_alterar
            elif tipo == 'd' and un_medida == 'p':
                meta = inicial - (inicial * valor_alterar / 100)
            elif tipo == 'm' and un_medida == 'a':
                meta = valor_alterar
            elif tipo == 'm' and un_medida == 'p':
                meta = 100

            novo_kr = [id_kr, id_obj, texto, tipo, un_medida, inicial, valor_alterar, meta, status, self.today, atual]
            print(f'\n{novo_kr}')
            krs.loc[len(krs)] = novo_kr

            obj.to_csv("okr.csv", index=False)
            krs.to_csv("krs.csv", index=False)

    def atualizar_kr(self):
        """atualiza os 3Ps + valor atual do kr selecionado"""
        aobj_on = True
        while aobj_on:
            # seleciona obj
            obj = read_csv('okr.csv')
            print('\nEstes são os objetivos disponíveis para atualização:')
            print(obj[['id_obj', 'texto']])
            id_obj = int(input('Qual objetivo deseja atualizar? [id_obj]  '))
    
            krs = read_csv('krs.csv')
            atualizacoes = read_csv('atualizacoes.csv')
            krs = krs[krs['id_obj'] == id_obj]
    
            # atualiza os kr do mesmo obj até usuario não quiser mais
            akr_on = True
            while akr_on:
                # seleciona um objetivo e então um kr. insere 3p's.
                print("\nEstes são os KR's deste objetivo:")
                print(krs[['id_kr', 'texto', 'inicial', 'meta', 'atual']])
                kr_desejado = int(input('Qual KR deseja atualizar? [id_kr]  '))
                ppp = input("Algum progresso, problema ou plano?:  ")
    
    
                # se kr_desejado já tem atualização, mostra ultima mudança. Se não tem, mostra valor inicial
                if kr_desejado in atualizacoes[['id_kr']].values:
                    atual = atualizacoes.loc[atualizacoes['id_kr'] == kr_desejado, "atual"].tolist()
                else:
                    atual = krs.loc[krs['id_kr'] == kr_desejado, "inicial"].tolist()
                meta = krs.loc[krs['id_kr'] == kr_desejado, 'meta'].tolist()
                mudou = input(f"\nO valor atual do kr é: {atual[-1]} com meta de {meta[0]}. Deseja mudar? [s/n]  ")
    
                # novo_valor é o valor atual até o user quiser alterar, aí novo_valor muda
                novo_valor = atual
                if mudou == 's':
                    novo_valor = input("Qual o novo valor?  ")
                krs.loc[krs['id_kr'] == kr_desejado, 'atual'] = novo_valor
                if kr_desejado in atualizacoes[['id_kr']].values:
                    krs.loc[krs['id_kr'] == kr_desejado, 'status'] = 'iniciado'
    
                krs.to_csv('krs.csv', index=False)
                '''por algum motivo está salvando id_kr em float ao inves de int. DESCOBRIR PQ'''
    
                dados_atu = read_csv('atualizacoes.csv')
                novo_id = dados_atu['id_atualizacao'].iloc[-1] + 1
    
                atualizacao = [novo_id, self.id_user, self.user, id_obj, kr_desejado, ppp, novo_valor, self.today]
                dados_atu.loc[len(dados_atu)] = atualizacao
                dados_atu.to_csv('atualizacoes.csv', index=False)
    
                mais_um = input('Deseja atualizar mais um KR desse Objetivo? [s/n]  ')
                if mais_um == 'n' or mais_um == 'nao' or mais_um == 'não':
                    akr_on = False
                
                """
                fim do loop while para KR
                """
                
            mais_um = input("Deseja atualizar outro OKR?  ")
            if mais_um == 'n' or mais_um == 'nao' or mais_um == 'não':
                aobj_on = False
            

    def monitorar_okr(self, trimestre):
      """imprime os okrs junto com os krs, caso estejam no trimestre atual """
      obj = read_csv('okr.csv')
      krs = read_csv("krs.csv")
      
      aobj = obj[obj['ciclo'] == trimestre]
      ids = aobj['id_obj'].to_list()
      
      akrs = DataFrame()
      for label, row in krs.iterrows():
        if row['id_obj'] in ids:
          akrs[len(akrs)] = row
      akrs = akrs.T
    
      n=0
      for l, r in aobj.iterrows():
        n+=1
        print(f"\n\nObjetivo {n}:")
        print(r[['time','setor','texto','responsavel']].to_frame().T) 
        id_esp = int(r[['id_obj']])
        print('KRs:')
        c = akrs[akrs['id_obj'] == id_esp].reset_index(drop=True)
        print(c[['texto','tipo','inicial','meta','atual']])
        print('\n\n')
