import Adafruit_DHT as sensor
import paramiko as ssh
import numpy as np
import pandas as pd
from datetime import datetime as date


global servidor

# função para executar comando no servidor
def executa(comando):
    (stdin, stderr, stdout) = servidor.exec_command(comando)

def escrever(dado, arquivo):
    data = {'temp':[dado]}
    escritor = pd.DataFrame(data)

        leitor = ler(arquivo)

        if len(leitor['temp']) == 10:
            vazio = pd.DataFrame()
            vazio.to_csv(arquivo, index=False)
        else:
            final = pd.concat([leitor, escritor], ignore_index=True, axis=0)
            final.to_csv(arquivo, index=False)

    

def ler(arquivo):
    try:
        resultado = pd.read_csv(arquivo)
    except pd.errors.EmptyDataError:
        resultado = None
        
    return resultado

def conecta_ssh:
    chave = ssh.RSAKey.from_private_key_file('/home/pi/.ssh/id_rsa')  # indica o local da chave privada de SSH
    servidor = ssh.SSHClient()  # seta c como variável q receberá os parâmetros de SSH
    servidor.set_missing_host_key_policy(ssh.AutoAddPolicy())  # linha insegura, procurar meio mais seguro
    # estou tentando ver como deixar o 192.168.2.40 com a chave pública já dentro dele, com o arquivo known_hosts
    servidor.connect(
        hostname='192.168.2.40',
        username='akawai',
        password=None,
        pkey=chave)  # efetua conexão via SSH, com os parâmetros

# definição inicial das variáveis do contador
# e da variável tempM (média de temperatura)
# e da variável tempD (desvio padrão da temperatura)
i=tempM=tempD=0
# codigo para conexão no 192.168.2.40
conecta_ssh()

# código para efetuar leitura do sensor DHT, conectado na porta GPIO25 do Raspberry
# DHT_SENSOR indica q o tipo de sensor é o DHT11
# DHT_PIN indica que a porta GPIO é a 25
DHT_SENSOR = sensor.DHT11
DHT_PIN = 25

temperature = sensor.read(DHT_SENSOR, DHT_PIN)[1] #temperatura é obtida através da leitura

if temperature is not None: # se a leitura de temperatura não é inválida
    if ler('temps.txt') == None:
        tabela = "<FONT size=6><TABLE BORDER=1 BORDERCOLOR=black><TR><TD>Data \ Horas</TD><TH>00h~02h</TH><TH>02h~04h</TH><TH>04h~06h</TH><TH>06h~08h</TH><TH>08h~10h</TH><TH>10h~12h</TH><TH>12h~14h</TH><TH>14h~16h</TH><TH>16h~18h</TH><TH>18h~20h</TH><TH>20h~22h</TH><TH>22h~24h</TH></TR><TR><TD>" + date.now().strftime("%d") + "/" + date.now().strftime("%m") + "</TD>"        
    elif len(ler(temps.txt)) == 12:
        tempM = np.mean(leitor['temp'])
        tempD = np.std(leitor['temp'])
        for i in range(0,13):
            tabela+= "<TD>{0:0.1f}C &PlusMinus; {1:0.1f}</TD>".format(tempM, tempD)

        tabela += "</TR>"


            executa('echo  + ' >> 1.html')
      

executa('echo ' + tabela +  ' >> 1.html')
