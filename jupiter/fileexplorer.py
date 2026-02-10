"""
biblioteca destinada à automatização de tarefas na web
bem como interações com o gerenciamento de arquivos no computador
"""
    
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
            print("Erro", f"Erro ao selecionar arquivo: {e}")
            return None
    
    def selecionar_multiplos_arquivos(self, titulo="Selecione os arquivos"):
        
        #permite selecionar vários arquivos de uma vez.
        #retorna uma lista de caminhos.
        try:
            arquivos = filedialog.askopenfilenames(title=titulo)
            return list(arquivos) if arquivos else []
        except Exception as e:
            print("Erro", f"Erro ao selecionar arquivos: {e}")
            return []

    def renomear_arquivo(self, caminho_atual, novo_nome):
        
        #renomeia um arquivo mantendo-o na mesma pasta.
        #'caminho_atual' deve ser o path completo.
        #'novo_nome' deve ser apenas o nome do arquivo com extensão (ex: "relatorio_final.pdf").
        try:
            diretorio = os.path.dirname(caminho_atual)
            novo_caminho = os.path.join(diretorio, novo_nome)
            
            os.rename(caminho_atual, novo_caminho)
            print(f"Arquivo renomeado para: {novo_nome}")
            return novo_caminho # Retorna o novo path para uso futuro
        except Exception as e:
            print(f"Erro ao renomear arquivo {caminho_atual}: {e}")

    def mover_arquivo(self, origem, destino):
        
        #move um arquivo de 'origem' para 'destino'.
        #o destino pode ser uma pasta ou um novo caminho completo de arquivo.
        try:
            shutil.move(origem, destino)
            print(f"Arquivo movido de {origem} para {destino}")
        except Exception as e:
            print(f"Erro ao mover arquivo: {e}")

    def copiar_arquivo(self, origem, destino):
        
        #copia um arquivo mantendo os metadados (datas de criação, etc).
        try:
            shutil.copy2(origem, destino)
            print(f"Arquivo copiado para {destino}")
        except Exception as e:
            print(f"Erro ao copiar arquivo: {e}")

    def excluir_arquivo(self, caminho):
        
        #remove um arquivo permanentemente.
        try:
            if os.path.exists(caminho):
                os.remove(caminho)
                print(f"Arquivo excluído: {caminho}")
            else:
                print(f"Arquivo não encontrado para exclusão: {caminho}")
        except Exception as e:
            print(f"Erro ao excluir arquivo: {e}")

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
            print("Erro", f"Erro ao selecionar pasta: {e}")
            return None

    def criar_pasta(self, caminho_pasta):
        
        #cria uma pasta (e subpastas se necessário). 
        #exist_ok=True evita erro se a pasta já existir.
        try:
            os.makedirs(caminho_pasta, exist_ok=True)
            print(f"Pasta garantida: {caminho_pasta}")
        except Exception as e:
            print(f"Erro ao criar pasta: {e}")

    def listar_arquivos(self, diretorio, extensao=None):
        
        #retorna uma lista com os nomes dos arquivos no diretório.
        #se 'extensao' for informado (ex: '.pdf'), filtra a lista.
        try:
            arquivos = os.listdir(diretorio)
            if extensao:
                arquivos = [f for f in arquivos if f.endswith(extensao)]
            return arquivos
        except Exception as e:
            print(f"Erro ao listar arquivos em {diretorio}: {e}")
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
            print("Erro", f"Erro na busca recursiva: {e}")
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
            print("Erro", f"Erro ao excluir pasta: {e}")

    def compactar_para_zip(self, caminho_origem, nome_zip):
        
        #cria um arquivo .zip de uma pasta ou arquivo
        #nome_zip não deve conter a extensão .zip ao final
        try:
            shutil.make_archive(nome_zip, 'zip', caminho_origem)
            messagebox.showinfo("Sucesso", f"Arquivo {nome_zip}.zip criado!")
        except Exception as e:
            print("Erro", f"Erro ao compactar: {e}")

    def descompactar_zip(self, arquivo_zip, destino):
        
        #extrai o conteúdo de um arquivo .zip
        try:
            shutil.unpack_archive(arquivo_zip, destino)
            messagebox.showinfo("Sucesso", f"Extraído em: {destino}")
        except Exception as e:
            print("Erro", f"Erro ao descompactar: {e}")

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
            print(f"Erro ao buscar arquivo recente: {e}")
            return None