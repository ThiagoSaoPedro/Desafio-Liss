from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import csv

def scraping(url, name, max_processos=1500):

    service = Service()
    options = webdriver.ChromeOptions()

    partes_env_list = []
    n_processos_list = []
    tribunal_list = []
    localidade_list = []
    uf_list = []
    classe_list = []


    driver = uc.Chrome(service=service, options=options)


    driver.get(url)


    ultimotamanho = driver.execute_script('return document.body.scrollHeight')

    # Executa rolagens
    for contador in range(1000): 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)

        novoultimotamanho = driver.execute_script('return document.body.scrollHeight')

        if novoultimotamanho == ultimotamanho:
            break
        ultimotamanho = novoultimotamanho

        if len(n_processos_list) >= max_processos:
            break
        
    partes = driver.find_elements(By.TAG_NAME, 'Strong')
    for i in partes:
        if(name.split()[0] != i.text.split()[0]):
            partes_envolvidas = i.text
            partes_env_list.append(partes_envolvidas)
            if len(partes_env_list) >= max_processos:
                break


    processos = driver.find_elements(By.CLASS_NAME, 'LawsuitCardPersonPage-header-processNumber')
    for i in processos:
        processo_text = i.text.split()
        if len(processo_text) >= 3:
            numero_processos = processo_text[2]
            n_processos_list.append(numero_processos)
        else:
            n_processos_list.append('')
        if len(n_processos_list) >= max_processos:
            break

    texto = driver.find_elements(By.CLASS_NAME, 'LawsuitCardPersonPage-body-row-item-text')
        
    for i in texto:
        if (i.text[:2].isupper()):
            tribunal_localidade_uf = i.text
            uf = tribunal_localidade_uf[-2:]
            uf_list.append(uf)
            tribunal_localidade_uf = tribunal_localidade_uf[:-2]
            tribunal = tribunal_localidade_uf.split()[0]
            tribunal_list.append(tribunal)
            tribunal_localidade_uf = tribunal_localidade_uf[7:]
            localidade = tribunal_localidade_uf.strip(", ")
            localidade_list.append(localidade)
        else:
            classe = i.text
            classe_list.append(classe)

        if len(tribunal_list) >= max_processos or len(localidade_list) >= max_processos or len(uf_list) >= max_processos or len(classe_list) >= max_processos:
            break

    max_length = max(len(partes_env_list), len(n_processos_list), len(tribunal_list), len(localidade_list), len(uf_list), len(classe_list))

    partes_env_list.extend([''] * (max_length - len(partes_env_list)))
    n_processos_list.extend([''] * (max_length - len(n_processos_list)))
    tribunal_list.extend([''] * (max_length - len(tribunal_list)))
    localidade_list.extend([''] * (max_length - len(localidade_list)))
    uf_list.extend([''] * (max_length - len(uf_list)))
    classe_list.extend([''] * (max_length - len(classe_list)))

    dict_processos = {
        "Tribunal" : tribunal_list,
        "Uf" : uf_list,
        "Localidade" : localidade_list,
        "Procedimento" : classe_list,
        "Partes" : partes_env_list
    }
    
    with open(f'{name}', 'w', newline='') as arquivo:
        dict_writer = csv.DictWriter(arquivo, fieldnames=dict_processos.keys())
        dict_writer.writeheader()
        for i in range(max_length):
            row = {key: dict_processos[key][i] for key in dict_processos}
            dict_writer.writerow(row)

scraping("https://www.jusbrasil.com.br/processos/nome/29201840/nike-do-brasil-comercio-e-participacoes-ltda", "Nike do Brasil Comércio e Participações Ltda.csv")

scraping("https://www.jusbrasil.com.br/processos/nome/28654972/adidas-do-brasil-ltda", "Adidas do Brasil Ltda.csv")

scraping("https://www.jusbrasil.com.br/processos/nome/65417283/puma-do-brasil-ltda", "Puma do Brasil Ltda.csv")

scraping("https://www.jusbrasil.com.br/processos/nome/28195165/reebok-produtos-esportivos-brasil-ltda", "Reebok Produtos Esportivos Ltda.csv")

scraping("https://www.jusbrasil.com.br/processos/nome/30873463/asics-brasil-distribuicao-e-comercio-de-artigos-esportivos-ltda", "Asics Brasil, Distribuição e Comércio de Artigos Esportivos Ltda.csv")

scraping("https://www.jusbrasil.com.br/processos/nome/313427154/under-armour-brasil-comercio-e-distribuicao-de-artigos-esportivos-ltda", "Under Armour Brasil Comércio e Distribuição de Artigos Esportivos Ltda.csv")
