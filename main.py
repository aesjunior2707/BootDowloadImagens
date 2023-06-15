import sqlite3
import numpy as np
import os
import urllib.request
import zipfile
import shutil
import tkinter as tk
import threading

# Cria a janela
janela = tk.Tk()

janela.title("Boot Imagens Sousas Imobiliaria")

janela.geometry("750x500")

# Cria o campo de texto
campo_texto = tk.Text(janela, width=500, height=20)
campo_texto.pack()

# Cria o botão
botao = tk.Button(janela, text="Iniciar",height=20)
botao.configure(bg="green", font=("Arial", 12))
botao.pack(fill="x")

def focusUltimaLinhas():
    campo_texto.see("end")
        # Define o ponto de inserção na última linha
    campo_texto.mark_set("insert", "end")


def BaixarImagens():
    campo_texto.insert("end", "Iniciando o download das imagens...\n")
    focusUltimaLinhas()
    # Conecta ao banco de dados (se o banco de dados não existir, ele será criado automaticamente)
    conn = sqlite3.connect('data\SousasImobiliaria.db')

    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executa um comando SQL
    cursor.execute(' select CLIENTES.NOME,IMOVEIS.IDIMOVEL,IMOVEISFOTOS.URL_IMG_GRANDE  from CLIENTES ,IMOVEIS ,IMOVEISFOTOS '+
                ' where IMOVEIS.IDIMOVEL = IMOVEISFOTOS.IDIMOVEL AND CLIENTES.IDCLIENTE = IMOVEIS.IDCLIENTE')

    resultados = cursor.fetchall()

    campo_texto.insert("end", 'Conectado no banco de dados com sucesso !!!\n')
    focusUltimaLinhas()

    array_resultados = np.array(resultados)

    indices_ordenados = np.argsort(array_resultados[:, 0])

    meu_array_ordenado = array_resultados[indices_ordenados]

    indice = 0

    for valor in meu_array_ordenado:
        indice += 1 * 100
        NomeCliente = valor[0].replace('/','') # Id do Cliente
        idImovel = valor[1] # Nome do Cliente 
        diretorio = 'imgs/'+ NomeCliente

        if not os.path.exists(diretorio):
            os.mkdir(diretorio)

        nome_imagem = str(indice) + '.jpg'

        diretorioImovel = diretorio + '/' + str(idImovel)
    
        if not os.path.exists(diretorioImovel):
            os.mkdir(diretorioImovel)
    
        URLImg = valor[2]
    
        try:
            campo_texto.insert("end", "Baixando imagem do imovel: "+ str(idImovel) + " do Cliente:  " + NomeCliente + "\n")
            focusUltimaLinhas()
            urllib.request.urlretrieve(URLImg, os.path.join(diretorioImovel, nome_imagem))
        except Exception as e:
            focusUltimaLinhas()
            campo_texto.insert("end", URLImg + ' : ' + str(e))
           
    for valor in meu_array_ordenado:
        NomeCliente = valor[0].replace('/','') # Id do Cliente
        diretorio = 'imgs/'+ NomeCliente 
    
        if os.path.exists(diretorio):
            pastaZipada = diretorio + '.zip'
            focusUltimaLinhas()
            campo_texto.insert("end", 'Zipando pasta : '+diretorio +'.zip...\n')
            arquivo_zip = zipfile.ZipFile(pastaZipada, 'w')
            # Percorre todos os arquivos e subpastas da pasta e adiciona ao arquivo zip
            for pasta_raiz, pastas, arquivos in os.walk(diretorio):
                focusUltimaLinhas()
                campo_texto.insert("end", 'Adicionando as imagens... \n')
                for arquivo in arquivos:
                    caminho_completo = os.path.join(pasta_raiz, arquivo)
                    arquivo_zip.write(caminho_completo)

            # Fecha o arquivo zip
            arquivo_zip.close()
            shutil.rmtree(diretorio)
            focusUltimaLinhas()
            campo_texto.insert("end", 'Download Feito com sucesso!! \n')

    cursor.close()
    conn.close()
   
def Iniciar():
    thread = threading.Thread(target=BaixarImagens)
    thread.start() 
# Associa a função ao botão
botao.config(command=Iniciar)
botao.pack()

# Executa a janela
janela.mainloop()    












