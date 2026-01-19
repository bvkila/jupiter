"""
biblioteca destinada à automatização de tarefas na web
bem como interações com o gerenciamento de arquivos no computador
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from tkinter import messagebox
import tkinter as tk
import time
import json


class AutomacaoWeb:

    '''
    A seguinte classe fornece uma base robusta para tarefas comuns de RPA (Robotic Process Automation) dentro da web.
    Sua estrutura consiste em:

    1. NAVEGAÇÕES DENTRO DO DRIVER
    
    Gerenciamento de Driver: inicialização otimizada do Microsoft Edge, incluindo suporte para modo Headless (segundo plano).
    Controle de Abas: abertura, troca e fechamento inteligente de abas.
    
    
    2. INTERAÇÕES COM A PÁGINA

    Interações Avançadas: cliques, digitação (com limpeza automática), Hover (passar o mouse) e seleção de dropdowns.
    Tratamento de Esperas: uso nativo de `WebDriverWait` para garantir que os elementos existam antes da interação, reduzindo erros de sincronismo.
    Captura de Tela: método integrado para screenshots de auditoria.
    Suporte a Iframes: facilidade para entrar e sair de contextos de frames.

    3. VERIFICAÇÕES

    Verificação de Textos: verifica se um texto específico existe na página.
    Verificação de Elementos: verifica se um elemento específico existe na página.

    '''

    def __init__(self):
        
        self.driver = None
        self.timeout = 10 #define tempo de espera padrão


### NAVEGAÇÕES DENTRO DO DRIVER

    def iniciar_driver(self, headless=False):
        
        #inicializa o driver e configura as opções do navegador.
        edge_options = Options()
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--log-level=3")

        #se headless for verdadeiro, configura o driver para rodar em modo headless
        if headless:
            edge_options.add_argument("--headless=new") 
        self.driver = webdriver.Edge(options=edge_options)
        self.driver.maximize_window()

    def abrir_url(self, url):
        
        #carrega uma página web.
        self.driver.get(url)
    
    def abrir_nova_aba(self, url):
        
        #abre uma nova aba e foca nela automaticamente.
        try:
            # 'tab' abre uma aba. 'window' abriria uma nova janela separada.
            self.driver.switch_to.new_window('tab') 
            self.driver.get(url)
        except Exception as e:
            messagebox.showerror(f"Erro ao abrir nova aba: {e}")
    
    def alternar_aba(self, indice):
        #muda o foco para a aba especificada pelo índice (0 é a primeira, 1 é a segunda...).
        try:
            abas = self.driver.window_handles
            self.driver.switch_to.window(abas[indice])
        except Exception as e:
            messagebox.showerror(f"Erro ao mudar para a aba {indice}: {e}")
        
    def fechar_aba(self):
    
        #fecha a aba atual e volta o foco para a aba anterior (se houver).    
        try:
            # .close() fecha SÓ a aba atual (diferente de .quit() que fecha tudo)
            self.driver.close()
            
            #boa prática: voltar o foco para a última aba aberta para não ficar "sem foco"
            if len(self.driver.window_handles) > 0:
                self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            messagebox.showerror(f"Erro ao fechar aba: {e}")

    def recarregar_driver(self):
        
        #recarrega (atualiza) a página atual (F5).
        try:
            self.driver.refresh()
        except Exception as e:
             messagebox.showerror(f"Erro ao recarregar a página: {e}")

    def fechar_driver(self):
        
        #fecha o navegador e encerra a sessão do driver.
        self.driver.quit()



### INTERAÇÕES COM A PÁGINA

    def clicar(self, xpath):
    
        #clica em um elemento identificado pelo xpath.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.click()
        except Exception as e:
            messagebox.showerror(f"Erro ao clicar no elemento {xpath}: {e}")

    def digitar(self, xpath, texto):
        
        #digita um texto em um elemento identificado pelo xpath.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.clear()
            elemento.send_keys(texto)
        except Exception as e:
            messagebox.showerror(f"Erro ao digitar no elemento {xpath}: {e}")
    
    def passar_mouse(self, xpath):
        
        #simula a ação de mover o cursor do mouse sobre o elemento (Hover).
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            actions = ActionChains(self.driver)
            actions.move_to_element(elemento).perform()
        except Exception as e:
            messagebox.showerror(f"Erro ao passar mouse sobre {xpath}: {e}")
    
    def selecionar_texto(self, xpath, texto):

        #seleciona um texto dentro de um elemento.
        try:
            Select(WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))).select_by_visible_text(texto)
        except Exception as e:
            messagebox.showerror(f"Erro ao selecionar {texto} no elemento {xpath}: {e}")

    def selecionar_valor(self, xpath, valor):

        #seleciona um valor dentro de um elemento.
        try:
            Select(WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))).select_by_value(valor)
        except Exception as e:
            messagebox.showerror(f"Erro ao selecionar {valor} no elemento {xpath}: {e}")

    def limpar(self, xpath):

        #limpa o conteúdo de um elemento de entrada.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath))); elemento.clear()
        except Exception as e:
            messagebox.showerror(f"Erro ao limpar o conteúdo do elemento {xpath}: {e}")
    
    def obter_texto(self, xpath):

        #obtém o texto de um elemento.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.text
        except Exception as e:
            messagebox.showerror(f"Erro ao obter o texto do elemento {xpath}: {e}")
    
    def obter_atributo(self, xpath, atributo):

        #obtém o atributo de um elemento.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.get_attribute(atributo)
        except Exception as e:
            messagebox.showerror(f"Erro ao obter o atributo do elemento {xpath}: {e}")
    
    def rolar_ate_elemento(self, xpath):
        
        #rola a tela até que o elemento específico esteja visível.
        try:
            elemento = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        except Exception as e:
            messagebox.showerror(f"Erro ao rolar até o elemento {xpath}: {e}")
    
    def aguardar_elemento_sumir(self, xpath):
        
        #aguarda até que o elemento não esteja mais visível.
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            messagebox.showerror(f"Erro ou timeout ao aguardar elemento sumir {xpath}: {e}")
    
    def encontrar_elementos(self, xpath):
        
        #retorna uma lista com todos os elementos identificados pelo xpath.
        try:
            return self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            messagebox.showerror(f"Erro ao encontrar elementos {xpath}: {e}")

    def tirar_screenshot(self, nome_arquivo):
        
        #salva uma imagem da tela atual.
        try:
            self.driver.save_screenshot(f"{nome_arquivo}.png")
        except Exception as e:
            messagebox.showerror(f"Erro ao salvar screenshot: {e}")
    
    def entrar_iframe(self, xpath):
        
        #muda o foco do driver para dentro de um iframe.
        try:
            WebDriverWait(self.driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
        except Exception as e:
            messagebox.showerror(f"Erro ao entrar no iframe {xpath}: {e}")

    def sair_iframe(self):
        
        #volta o foco para a página principal.
        self.driver.switch_to.default_content()
    
    def salvar_cookies(self, nome_arquivo="cookies.json"):
        
        #coleta todos os cookies da sessão atual e salva em um arquivo JSON.
        #útil para manter o login em execuções futuras.
  
        #exibe uma mensagem de aviso para o usuário
        #a ideia é que após clicar em ok, o código prossiga
        root = tk.Tk()
        root.attributes('-topmost', True) #deixa a janela sempre no topo
        root.withdraw()
        messagebox.showwarning(
            'Atenção',
            'Clique em "OK" apenas quando estiver pronto para salvar os cookies.',
            parent=root
        )
        root.destroy()

        try:
            #obtém lista de dicionários com os cookies
            cookies = self.driver.get_cookies()
            with open(nome_arquivo, 'w') as arquivo:
                json.dump(cookies, arquivo, indent=4)
        except Exception as e:
            print(f"Erro ao salvar cookies: {e}")
    
    def carregar_cookies(self, nome_arquivo="cookies.json"):

        #carrega os cookies salvos em um arquivo JSON.
        #a URL precisa já estar carregada para o carregamento funcionar.

        try:

            with open(nome_arquivo, 'r') as arquivo:
                cookies = json.load(arquivo)
            for cookie in cookies:
                try:

                    #remove o domínio para evitar erro de "Invalid Cookie Domain".
                    #o selenium vai atribuir o cookie ao domínio atual automaticamente.
                    if 'domain' in cookie:
                        del cookie['domain']

                    #garante que a expiração seja um número inteiro (alguns salvam como float)
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    
                    #remove sameSite se existir, pois causa conflitos frequentes em Chrome/Edge
                    if 'sameSite' in cookie:
                        del cookie['sameSite']

                    #adiciona o cookie limpo
                    self.driver.add_cookie(cookie)
                
                except Exception as e_cookie:
                    #é normal alguns cookies falharem (ex: cookies de sessão já expirados)
                    print(f"Ignorando cookie '{cookie.get('name', 'desconhecido')}': {e_cookie}")

            self.recarregar_driver() 

        except FileNotFoundError:
            messagebox.showwarning("Aviso", f"Arquivo '{nome_arquivo}' não existe. Faça o login manual primeiro.")

        except Exception as e:
            print(f"Erro ao carregar cookies: {e}")



### VERIFICAÇÕES

    '''
    Em algumas das funções, como não dá pra passar o self.timeout no argumento da função,
    tem-se que passar como None e definir o timeout dentro da função. E se não for seleiconado
    um valor pro timeout ele usa o self.timeout.
    '''

    def verifica_selecionado(self, xpath, timeout=None):


        if timeout is None:
            timeout = self.timeout

        #verifica se um elemento (como checkbox) está selecionado.
        try:
            elemento = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.is_selected()
        except Exception as e:
            messagebox.showerror(f"Erro ao obter o texto do elemento {xpath}: {e}")
    
    def verifica_habilitado(self, xpath, timeout=None):
 

        if timeout is None:
            timeout = self.timeout

        #verifica se um elemento está habilitado
        try:
            elemento = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.is_enabled()
        except Exception as e:
            messagebox.showerror(f"Erro ao obter o texto do elemento {xpath}: {e}")

    def verifica_clicavel(self, xpath, timeout=None):
    

        if timeout is None:
            timeout = self.timeout

        #verifica se o elemento está visível E habilitado para clique.
        try:
            #o wait.until vai esperar até que o elemento seja clicável ou o tempo esgote
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return True
        except TimeoutException:
            #se o tempo (10s) passar e não ficar clicável, retorna False
            return False
        except Exception as e:
            messagebox.showerror(f"Erro ao verificar clicabilidade de {xpath}: {e}")
            return False
    
    def verifica_existe(self, xpath, timeout=None):


        if timeout is None:
            timeout = self.timeout

        #verifica se um elemento existe na página (Retorna True ou False).
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False
        except Exception as e:
            messagebox.showerror(f"Erro inesperado ao verificar elemento {xpath}: {e}")
            return False

import os
import shutil
from tkinter import filedialog

class FileExplorer:
    
    '''
    Classe destinada à manipulação de arquivos e pastas no sistema operacional.
    Sua estrutura consiste em:

    ...continuação
    '''

    def __init__(self):
        
        #inicializador simples, pode ser expandido se necessário manter estados (ex: pasta padrão)
        pass

### MANIPULAÇÃO DE ARQUIVOS

    def selecionar_arquivo(self, titulo="Selecione um arquivo", tipos_arquivos=[("Todos os arquivos", "*.*")]):
        
        #abre uma janela para o usuário escolher um arquivo.
        #retorna o caminho completo do arquivo ou None (se cancelado).
        try:
            caminho = filedialog.askopenfilename(
                title=titulo,
                filetypes=tipos_arquivos
            )
            return caminho if caminho else None
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar arquivo: {e}")
            return None
    
    def selecionar_multiplos_arquivos(self, titulo="Selecione os arquivos"):
        
        #permite selecionar vários arquivos de uma vez.
        #retorna uma lista de caminhos.
        try:
            arquivos = filedialog.askopenfilenames(title=titulo)
            return list(arquivos) if arquivos else []
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar arquivos: {e}")
            return []

    def renomear_arquivo(self, caminho_atual, novo_nome):
        
        #renomeia um arquivo mantendo-o na mesma pasta.
        #'caminho_atual' deve ser o path completo.
        #'novo_nome' deve ser apenas o nome do arquivo com extensão (ex: "relatorio_final.pdf").
        try:
            diretorio = os.path.dirname(caminho_atual)
            novo_caminho = os.path.join(diretorio, novo_nome)
            
            os.rename(caminho_atual, novo_caminho)
            messagebox.showerror(f"Arquivo renomeado para: {novo_nome}")
            return novo_caminho # Retorna o novo path para uso futuro
        except Exception as e:
            messagebox.showerror(f"Erro ao renomear arquivo {caminho_atual}: {e}")

    def mover_arquivo(self, origem, destino):
        
        #move um arquivo de 'origem' para 'destino'.
        #o destino pode ser uma pasta ou um novo caminho completo de arquivo.
        try:
            shutil.move(origem, destino)
            messagebox.showerror(f"Arquivo movido de {origem} para {destino}")
        except Exception as e:
            messagebox.showerror(f"Erro ao mover arquivo: {e}")

    def copiar_arquivo(self, origem, destino):
        
        #copia um arquivo mantendo os metadados (datas de criação, etc).
        try:
            shutil.copy2(origem, destino)
            messagebox.showerror(f"Arquivo copiado para {destino}")
        except Exception as e:
            messagebox.showerror(f"Erro ao copiar arquivo: {e}")

    def excluir_arquivo(self, caminho):
        
        #remove um arquivo permanentemente.
        try:
            if os.path.exists(caminho):
                os.remove(caminho)
                messagebox.showerror(f"Arquivo excluído: {caminho}")
            else:
                messagebox.showerror(f"Arquivo não encontrado para exclusão: {caminho}")
        except Exception as e:
            messagebox.showerror(f"Erro ao excluir arquivo: {e}")

    def aguardar_arquivo(caminho_arquivo, timeout=20):
        '''
        aguarda até que um arquivo exista no caminho especificado ou até que o tempo limite seja atingido
        '''
        inicio = time.time()
        while not os.path.exists(caminho_arquivo):
            if time.time() - inicio > timeout:
                raise TimeoutError(f"O arquivo {caminho_arquivo} não foi encontrado dentro do tempo limite de {timeout} segundos.")

### GERENCIAMENTO DE PASTAS

    def selecionar_pasta(self, titulo="Selecione uma pasta"):
        
        #abre uma janela para o usuário escolher um diretório.
        #retorna o caminho da pasta ou None (se cancelado).
        try:
            pasta = filedialog.askdirectory(title=titulo)
            return pasta if pasta else None
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar pasta: {e}")
            return None

    def criar_pasta(self, caminho_pasta):
        
        #cria uma pasta (e subpastas se necessário). 
        #exist_ok=True evita erro se a pasta já existir.
        try:
            os.makedirs(caminho_pasta, exist_ok=True)
            messagebox.showerror(f"Pasta garantida: {caminho_pasta}")
        except Exception as e:
            messagebox.showerror(f"Erro ao criar pasta: {e}")

    def listar_arquivos(self, diretorio, extensao=None):
        
        #retorna uma lista com os nomes dos arquivos no diretório.
        #se 'extensao' for informado (ex: '.pdf'), filtra a lista.
        try:
            arquivos = os.listdir(diretorio)
            if extensao:
                arquivos = [f for f in arquivos if f.endswith(extensao)]
            return arquivos
        except Exception as e:
            messagebox.showerror(f"Erro ao listar arquivos em {diretorio}: {e}")
            return []
    
    def listar_recursivo(self, diretorio, extensao=None):
        
        #lista TODOS os arquivos, incluindo os que estão em subpastas
        arquivos_encontrados = []
        try:
            for raiz, diretorios, arquivos in os.walk(diretorio):
                for arquivo in arquivos:
                    if extensao is None or arquivo.endswith(extensao):
                        arquivos_encontrados.append(os.path.join(raiz, arquivo))
            return arquivos_encontrados
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na busca recursiva: {e}")
            return []

    def pasta_esta_vazia(self, caminho_pasta):
       
        #verifica se uma pasta não contém arquivos ou subpastas
        return not any(os.scandir(caminho_pasta))
    
    def excluir_pasta_completa(self, caminho_pasta):
        
        #remove a pasta e todo o seu conteúdo (arquivos e subpastas)
        try:
            if os.path.exists(caminho_pasta):
                shutil.rmtree(caminho_pasta)
                messagebox.showinfo("Sucesso", f"Pasta removida: {caminho_pasta}")
            else:
                messagebox.showwarning("Aviso", "Pasta não encontrada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir pasta: {e}")

    def compactar_para_zip(self, caminho_origem, nome_zip):
        
        #cria um arquivo .zip de uma pasta ou arquivo
        #nome_zip não deve conter a extensão .zip ao final
        try:
            shutil.make_archive(nome_zip, 'zip', caminho_origem)
            messagebox.showinfo("Sucesso", f"Arquivo {nome_zip}.zip criado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao compactar: {e}")

    def descompactar_zip(self, arquivo_zip, destino):
        
        #extrai o conteúdo de um arquivo .zip
        try:
            shutil.unpack_archive(arquivo_zip, destino)
            messagebox.showinfo("Sucesso", f"Extraído em: {destino}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao descompactar: {e}")

### UTILITÁRIOS E VERIFICAÇÕES

    def verifica_existe(self, caminho):
        
        #verifica se um arquivo ou pasta existe.
        return os.path.exists(caminho)

    def obter_arquivo_mais_recente(self, diretorio, extensao=None):

        #útil para pegar o último arquivo baixado na pasta de Downloads.
        try:
            arquivos = self.listar_arquivos(diretorio, extensao)
            if not arquivos:
                return None
            
            #reconstrói os caminhos completos
            caminhos_completos = [os.path.join(diretorio, f) for f in arquivos]
            
            #retorna o arquivo com a data de modificação mais recente
            arquivo_recente = max(caminhos_completos, key=os.path.getmtime)
            return arquivo_recente
        except Exception as e:
            messagebox.showerror(f"Erro ao buscar arquivo recente: {e}")
            return None