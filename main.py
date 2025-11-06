import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt # Importamos o matplotlib

def carregar_grafo_do_csv(nome_arquivo):
    """
    Lê um arquivo CSV de conflitos (com cabeçalho) e monta um grafo
    diretamente usando Pandas e NetworkX.

    Argumentos:
        nome_arquivo (str): O caminho para o arquivo CSV (ex: "pequeno.csv").

    Retorna:
        nx.Graph: O grafo de conflitos montado.
    """
    if not os.path.exists(nome_arquivo):
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return nx.Graph() 

    try:
        df = pd.read_csv(nome_arquivo)
        coluna_origem = df.columns[0]
        coluna_destino = df.columns[1]

        G = nx.from_pandas_edgelist(
            df,
            source=coluna_origem,
            target=coluna_destino
        )
        
        return G

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo '{nome_arquivo}': {e}")
        return nx.Graph()

def visualizar_grafo(G):
    """
    Usa nx.draw e matplotlib para desenhar o grafo em uma nova janela.
    """
    if G.number_of_nodes() == 0:
        print("Grafo está vazio, nada para desenhar.")
        return
        
    print("Desenhando o grafo... (Pode demorar para grafos grandes)")
    
    if G.number_of_nodes() > 100:
        print("AVISO: O grafo é grande, a visualização pode ser lenta e poluída.")

    try:
        plt.figure(figsize=(10, 8)) # Define um tamanho de janela
        
        # nx.draw desenha o grafo
        # with_labels=True mostra o nome de cada disciplina (nó)
        nx.draw(G, with_labels=True, node_size=50, font_size=8)
        
        plt.title("Visualização do Grafo de Conflitos")
        plt.show() # Exibe a janela do matplotlib
        
    except Exception as e:
        print(f"Ocorreu um erro ao tentar desenhar o grafo: {e}")

def exibir_detalhes_grafo(G):

    if G.number_of_nodes() == 0:
        print("Grafo está vazio.")
        return

    print("\n--- Detalhes do Grafo ---")
    
    # Contar vértices e arestas
    num_vertices = G.number_of_nodes()
    num_arestas = G.number_of_edges()
    print(f"* Disciplinas (Vértices): {num_vertices}")
    print(f"* Conflitos (Arestas): {num_arestas}")

    # Checar se está conexo
    # Em um grafo de conflitos, ele pode ter vários "grupos" isolados
    if nx.is_connected(G):
        print("* Conectividade: O grafo é conexo.")
    else:
        num_componentes = nx.number_connected_components(G)
        print(f"* Conectividade: O grafo NÃO é conexo (possui {num_componentes} componentes).")

    # Medir densidade
    densidade = nx.density(G)
    print(f"* Densidade do grafo: {densidade:.4f}")
    
    # Medir graus (mínimo, máximo, médio)
    graus = [val for (node, val) in G.degree()]
    grau_min = min(graus)
    grau_max = max(graus)
    grau_med = sum(graus) / num_vertices
    print(f"* Grau (Conflitos por Disciplina):")
    print(f"  - Mínimo: {grau_min}")
    print(f"  - Máximo: {grau_max}")
    print(f"  - Médio: {grau_med:.2f}")

    # Validar/Exibir conflitos (amostra)
    #print("\n* Amostra de Conflitos (Arestas):")
    #amostra_arestas = list(G.edges())[:5] # Pega os 5 primeiros
    #for aresta in amostra_arestas:
    #    print(f"  - {aresta[0]} <--> {aresta[1]}")
    print("---------------------------------")


def exibir_menu(G):

    if G.number_of_nodes() == 0:
        print("O grafo não pôde ser carregado. Saindo.")
        return

    while True:
        print("\n--- Menu de Opções ---")
        print("1. Visualizar grafo")
        print("2. Exibir detalhes e métricas do grafo")
        print("0. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            visualizar_grafo(G)
        elif escolha == '2':
            exibir_detalhes_grafo(G)
        elif escolha == '0':
            print("Saindo do menu.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    
    # Lista os arquivos disponíveis na pasta
    # Vou organizar em outra pasta depois
    print("Arquivos .csv encontrados no diretório:")
    arquivos = [f for f in os.listdir() if f.endswith('.csv')]
    if not arquivos:
        print("Nenhum arquivo .csv encontrado.")
        exit()
        
    for i, f in enumerate(arquivos):
        print(f"{i+1}. {f}")
    
    escolha_arquivo = input(f"\nQual arquivo deseja carregar (1-{len(arquivos)})? ")
    
    try:
        # Pega o nome do arquivo com base na escolha
        nome_do_arquivo = arquivos[int(escolha_arquivo) - 1]
        #print(f"Carregando grafo do arquivo: '{nome_do_arquivo}'...")
        
        G = carregar_grafo_do_csv(nome_do_arquivo)
        
        if G.number_of_nodes() > 0:
            print(f"Grafo '{nome_do_arquivo}' carregado com sucesso!")
            # Passa o grafo carregado para o menu
            exibir_menu(G)
        
    except (ValueError, IndexError):
        print("Escolha inválida.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")