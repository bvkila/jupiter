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

    Observaçoes:

    - Existe um controle de erro em todas as funções; caso ela não ocorra da maneira esperada,
    um print vai mostrar o que não saiu como o esperado. No entanto, o raise é utilizado para
    não dar erro na execução da automação.

    - As funções de verificações retornam resultados booleanos.


    '''

    def __init__(self, tempo_stun):
        
        self.driver = None
        self.wait = WebDriverWait(self.driver, 10) #define tempo de espera padrão
        self.stun = time.sleep(tempo_stun) #é uma interpretação diferente do "wait"
        #enquanto o wait espera por até x segundos, o stun obrigatoriamente espera x segundos
 
### NAVEGAÇÕES DENTRO DO DRIVER

    def iniciar_driver(self, headless=False):
        
        #inicializa o driver
        try:
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

        except Exception as e:
            print(f"Erro ao iniciar o driver: {e}")
            raise

    def abrir_url(self, url):

        #abre uma URL (precisa iniciar o driver primeiro).
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Erro ao abrir URL: {e}")
            raise
    
    def abrir_nova_aba(self, url):
        
        #abre uma nova aba e foca nela automaticamente.
        try:
            # 'tab' abre uma aba. 'window' abriria uma nova janela separada.
            self.driver.switch_to.new_window('tab') 
            self.driver.get(url)
        except Exception as e:
            print(f"Erro ao abrir nova aba: {e}")
            raise
    
    def alternar_aba(self, indice):

        #muda o foco para a aba especificada pelo índice (0 é a primeira, 1 é a segunda...).
        try:
            abas = self.driver.window_handles
            self.driver.switch_to.window(abas[indice])
        except Exception as e:
            print(f"Erro ao mudar para a aba {indice}: {e}")
            raise
        
    def fechar_aba(self):
    
        #fecha a aba atual e volta o foco para a aba anterior (se houver).    
        try:
            # .close() fecha SÓ a aba atual (diferente de .quit() que fecha tudo)
            self.driver.close()
            
            #boa prática: voltar o foco para a última aba aberta para não ficar "sem foco"
            if len(self.driver.window_handles) > 0:
                self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            print(f"Erro ao fechar aba: {e}")
            raise

    def recarregar_driver(self):
        
        #recarrega (atualiza) a página atual (F5).
        try:
            self.driver.refresh()
        except Exception as e:
            print(f"Erro ao recarregar a página: {e}")
            raise

    def fechar_driver(self):

        #fecha o navegador e encerra a sessão do driver.    
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Erro ao fechar o driver: {e}")
            raise

### INTERAÇÕES COM A PÁGINA

    def clicar(self, xpath):
    
        #clica em um elemento identificado pelo xpath.
        self.stun
        try:
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.click()
        except Exception as e:
            print(f"Erro ao clicar no elemento: {e}")
            raise

    def digitar(self, xpath, texto):
        
        #digita um texto em um elemento identificado pelo xpath.
        self.stun
        try:
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.send_keys(texto)
        except Exception as e:
            print(f"Erro ao digitar no elemento: {e}")
            raise
    
    def limpar(self, xpath):

        #limpa o conteúdo de um elemento de entrada.
        self.stun
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            elemento.clear()
        except Exception as e:
            print(f"Erro ao limpar o elemento: {e}")
            raise
    
    def passar_mouse(self, xpath):
        
        #simula a ação de mover o cursor do mouse sobre o elemento (Hover).
        self.stun
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            actions = ActionChains(self.driver)
            actions.move_to_element(elemento).perform()
        except Exception as e:
            print(f"Erro ao passar o mouse sobre o elemento: {e}")
            raise
    
    def selecionar_texto(self, xpath, texto):

        #seleciona um texto dentro de um elemento.
        self.stun
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            Select(elemento).select_by_visible_text(texto)
        except Exception as e:
            print(f"Erro ao selecionar o texto {texto}: {e}")
            raise

    def selecionar_valor(self, xpath, valor):

        #seleciona um valor dentro de um elemento.
        self.stun
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            Select(elemento).select_by_value(valor)
        except Exception as e:
            print(f"Erro ao selecionar o valor {valor}: {e}")
            raise
    
    def obter_texto(self, xpath):

        #obtém o texto de um elemento.
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.text
        except Exception as e:
            print(f"Erro ao obter o texto do elemento: {e}")
            raise
    
    def obter_atributo(self, xpath, atributo):

        #obtém o atributo de um elemento.
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.get_attribute(atributo)
        except Exception as e:
            print(f"Erro ao obter o atributo do elemento: {e}")
            raise
    
    def rolar_ate_elemento(self, xpath):
        
        #rola a tela até que o elemento específico esteja visível.
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        except Exception as e:
            print(f"Erro ao rolar a tela até o elemento: {e}")
            raise
    
    def aguardar_elemento_sumir(self, xpath):
        
        #aguarda até que o elemento não esteja mais visível.
        try:
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            print(f"Erro ao aguardar o elemento sumir: {e}")
            raise
    
    def encontrar_elementos(self, xpath):
        
        #retorna uma lista com todos os elementos identificados pelo xpath.
        try:
            return self.driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            print(f"Erro ao encontrar elementos: {e}")
            raise

    def tirar_screenshot(self, nome_arquivo):
        
        #salva uma imagem da tela atual.
        try:
            self.driver.save_screenshot(f"{nome_arquivo}.png")
        except Exception as e:
            print(f"Erro ao tirar screenshot: {e}")
            raise
    
    def entrar_iframe(self, xpath):
        
        #muda o foco do driver para dentro de um iframe.
        try:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
        except Exception as e:
            print(f"Erro ao entrar no iframe: {e}")
            raise

    def sair_iframe(self):
        
        #volta o foco para a página principal.
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            print(f"Erro ao sair do iframe: {e}")
            raise
    
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
            raise
    
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
            raise

### VERIFICAÇÕES

    '''
    Em algumas das funções, como não dá pra passar o self.timeout no argumento da função,
    tem-se que passar como None e definir o timeout dentro da função. E se não for seleiconado
    um valor pro timeout ele usa o self.timeout.
    '''

    def verifica_selecionado(self, xpath):
        #verifica se um elemento está selecionado (Retorna True ou False).
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.is_selected()
        except Exception as e:
            print(f"Erro ao verificar se o elemento está selecionado: {e}")
            raise
    
    def verifica_habilitado(self, xpath):
        #verifica se um elemento está habilitado (Retorna True ou False).
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elemento.is_enabled()
        except Exception as e:
            print(f"Erro ao verificar se o elemento está habilitado: {e}")
            raise

    def verifica_clicavel(self, xpath, timeout):
        #verifica se um elemento é clicavel (Retorna True ou False).
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception:
            print(f"Erro ao verificar se o elemento é clicavel")
            return False
    
    def verifica_existe(self, xpath, timeout):
        #verifica se um elemento existe na página (Retorna True ou False).
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception:
            return False
    
    def verificar_texto_digitado(self, xpath, texto_esperado):
        #verifica se o texto digitado em um campo é igual ao texto esperado.
        try:
            valor_atual = self.obter_atributo(xpath, 'value')
            return valor_atual == texto_esperado
        except Exception as e:
            print(f"Erro ao verificar o texto digitado: {e}")
            raise
    
    def obter_texto_selecionado(self, xpath):
        #obtém o texto atualmente selecionado em um elemento select.
        try:
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            selecao = Select(elemento)
            opcao_selecionada = selecao.first_selected_option
            return opcao_selecionada.text
        except Exception as e:
            print(f"Erro ao obter o texto do select: {e}")
            raise
    
    def verificar_selecao(self, xpath, texto_esperado):
        #verifica se o texto atualmente selecionado em um select é igual ao texto esperado.
        try:
            texto_atual = self.obter_texto_selecionado(xpath)
            return texto_atual == texto_esperado
        except Exception as e:
            print(f"Erro ao verificar o select: {e}")
            raise
