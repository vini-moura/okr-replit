from okr import *
from users import *
from ciclo import *
from pandas import *


users = read_csv('users.csv')
times = read_csv("times_users.csv")
okr = read_csv("okr.csv")
atualizacoes = read_csv('atualizacoes.csv')
t_u = read_csv('times_users.csv')


print("Bem vindo ao app okr por vinicius oliveira\n")

on = True
while on:
  escolha = input("Digite 1 para fazer login, 2 para cadastrar novo usuário ou 3 para sair:  ")
  if escolha == '1':
    usuario = login()
    while usuario != 0:
      
      u = users[users['id_user'] == usuario[0]]
      t = times[times['id_user'] == usuario[0]]
      o = Okr(u[['id_user']], u[['user']], t[['id_time']], t[["time"]])
      
      c = Ciclo()
      c.ciclo_def()
      
      acao = input("\nDigite 1 para cadastrar, 2 para atualizar e 3 para monitorar um OKR  ")
      #acao = 'monitorar'
      if acao == "1":
        o.cadastrar_okr()
      elif acao == "2":
        o.atualizar_kr()
      elif acao == "3":
        o.monitorar_okr(c.ciclo)
      elif acao == "sair" or acao == 'exit' or acao == 's' or acao == 'e' or acao == '4':
        usuario = 0
        on = False
      else:
        pass
        
  elif escolha == '2':
    cadastro()
    
  elif escolha == '3':
    on = False
    
  else:
    pass