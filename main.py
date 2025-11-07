import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt
import gcol
import time

def carregar_grafo_do_csv(nome_arquivo):
    """
    Lê um arquivo CSV de conflitos (com cabeçalho) e monta um grafo
    diretamente usando Pandas e NetworkX.
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

def selecionar_e_carregar_grafo():
    """
    Exibe os arquivos CSV disponíveis na pasta, 
    permite escolher um e retorna o grafo NetworkX carregado.
    """
    print("\n------ Seleção de Arquivo ------")
    
    arquivos = [f for f in os.listdir() if f.endswith('.csv')]
    if not arquivos:
        print("Nenhum arquivo .csv encontrado no diretório.")
        return None
        
    for i, f in enumerate(arquivos):
        print(f"{i+1}. {f}")
    
    try:
        escolha_arquivo = input(f"\nQual arquivo deseja carregar (1-{len(arquivos)})? ")
        nome_do_arquivo = arquivos[int(escolha_arquivo) - 1]
        
        G = carregar_grafo_do_csv(nome_do_arquivo)
        
        if G.number_of_nodes() > 0:
            print(f"Grafo '{nome_do_arquivo}' foi carregado com sucesso!")
            return G
        else:
            print("Falha ao carregar o grafo ou o grafo está vazio.")
            return None
        
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return None
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")
        return None


def exibir_detalhes_grafo(G):
    """
    Exibe as métricas e detalhes do grafo.
    """
    if G.number_of_nodes() == 0:
        print("Grafo está vazio.")
        return

    print("\n-------- Detalhes do Grafo --------")
    num_vertices = G.number_of_nodes()
    num_arestas = G.number_of_edges()
    print(f"* Disciplinas (Vértices): {num_vertices}")
    print(f"* Conflitos (Arestas): {num_arestas}")

    if nx.is_connected(G):
        print("* Conectividade: O grafo é conexo.")
    else:
        num_componentes = nx.number_connected_components(G)
        print(f"* Conectividade: O grafo NÃO é conexo (possui {num_componentes} componentes).")

    densidade = nx.density(G)
    print(f"* Densidade do grafo: {densidade:.4f}")
    
    graus = [val for (node, val) in G.degree()]
    grau_min = min(graus)
    grau_max = max(graus)
    grau_med = sum(graus) / num_vertices
    print(f"* Grau (Conflitos por Disciplina):")
    print(f"  - Mínimo: {grau_min}")
    print(f"  - Máximo: {grau_max}")
    print(f"  - Médio: {grau_med:.2f}")
    print("-----------------------------------")

def visualizar_grafo(G, c=None):
    """
    Usa nx.draw para desenhar o grafo.
    Se um dicionário de coloração 'c' for fornecido, desenha o grafo colorido.
    """
    if G.number_of_nodes() == 0:
        print("Grafo está vazio, nada para desenhar.")
        return
        
    print("Desenhando o grafo...")
    
    if G.number_of_nodes() > 100:
        print("AVISO: O grafo é grande, a visualização pode ser lenta e poluída.")

    try:
        plt.figure(figsize=(10, 8))
        
        node_color_param = "skyblue"
        titulo = "Visualização do Grafo de Conflitos (Sem Cor)"

        if c:
            print("Aplicando coloração à visualização...")
            node_color_param = gcol.get_node_colors(G, c)
            num_cores = max(c.values()) + 1
            titulo = f"Grafo Colorido com {num_cores} Cores/Horários"

        pos = nx.spring_layout(G, seed=42)
        
        nx.draw(G, 
                pos=pos,
                with_labels=True, 
                node_color=node_color_param,
                node_size=400, 
                font_size=15,
                edge_color="#cccccc")
        
        plt.title(titulo)
        plt.show() 
        
    except Exception as e:
        print(f"Ocorreu um erro ao tentar desenhar o grafo: {e}")

def rodar_algoritmo_gcol(G, nome_algoritmo, strategy=None, opt_alg=None):
    """
    Executa um algoritmo de coloração da GCol, mede o tempo 
    e imprime os resultados no formato exigido pelo trabalho.
    
    Argumentos:
        G (nx.Graph): O grafo a ser colorido.
        nome_algoritmo (str): O nome amigável do algoritmo (para impressão).
        strategy (str, opcional): A heurística inicial ('random', 'welsh_powell', etc.).
        opt_alg (int, opcional): O algoritmo de otimização (1 a 5).

    Retorna:
        dict: O dicionário de coloração.
    """
    print(f"\n------ Executando: {nome_algoritmo} ------")
    
    try:
        start_time = time.time()
        
        c = gcol.node_coloring(G, strategy=strategy, opt_alg=opt_alg)

        execution_time = time.time() - start_time
        
        num_cores = max(c.values()) + 1
        print(f"Resultado Encontrado:")
        print(f"  - Número de cores (horários): {num_cores}")
        print(f"  - Tempo de execução: {execution_time:.4f} segundos")
        print(f"  - Mapeamento Disciplina -> Horário (Cor):")

        for disciplina, cor in c.items():
            print(f"    - {disciplina}: Cor {cor}")
        
        # Alternativa caso a lista fosse muito grande mas descartei por enquanto

        #count = 0
        #for disciplina, cor in c.items():
        #    if count < 10:
        #        print(f"    - {disciplina}: Cor {cor}")
        #    count += 1
        #if count > 10:
        #    print(f"     ... (e mais {count - 10} disciplinas)")
        
        print("---------------------------------------")
        return c 

    except Exception as e:
        print(f"Falha ao executar o algoritmo {nome_algoritmo}: {e}")
        return None

def menu_coloracao(G, c_anterior):
    """
    Sub-menu para escolher qual algoritmo da GCol rodar.
    Retorna o dicionário de coloração 'c' mais recente.
    """
    while True:
        print("\n------ Escolha o Algoritmo de Coloração ------\n")
        #print("--- Estratégias de Heurística ---")
        print("1. Random Sequential")
        print("2. Welsh-Powell")
        print("3. DSATUR (Padrão GCol)")
        print("4. Recursive Largest First")
        #print("--- Algoritmo de Otimização ---")
        print("5. Algoritmo Exato (baseado no DSATUR + opt_alg=1)")
        print("0. Voltar ao menu principal")
        
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            c_novo = rodar_algoritmo_gcol(G, 
                                          nome_algoritmo="Random Sequential",
                                          strategy='random',
                                          opt_alg=None)
            return c_novo if c_novo is not None else c_anterior
        
        elif escolha == '2':
            c_novo = rodar_algoritmo_gcol(G, 
                                          nome_algoritmo="Welsh-Powell",
                                          strategy='welsh_powell',
                                          opt_alg=None)
            return c_novo if c_novo is not None else c_anterior
        
        elif escolha == '3':
            c_novo = rodar_algoritmo_gcol(G, 
                                          nome_algoritmo="DSATUR (Padrão)",
                                          strategy='dsatur', 
                                          opt_alg=None)
            return c_novo if c_novo is not None else c_anterior

        elif escolha == '4':
            c_novo = rodar_algoritmo_gcol(G, 
                                          nome_algoritmo="Recursive Largest First (RLF)",
                                          strategy='rlf',
                                          opt_alg=None)
            return c_novo if c_novo is not None else c_anterior

        elif escolha == '5':
            c_novo = rodar_algoritmo_gcol(G, 
                                          nome_algoritmo="Exato (DSATUR + opt_alg=1)", 
                                          strategy='dsatur', 
                                          opt_alg=1)
            return c_novo if c_novo is not None else c_anterior
                
        elif escolha == '0':
            print("Voltando ao menu principal...")
            return c_anterior 
        
        else:
            print("Opção inválida. Tente novamente.")

def exibir_menu(G):
    """
    Menu principal de opções para interagir com o grafo.
    """
    coloracao_recente = None 

    while True:
        print("\n------ Menu Principal ------\n")
        #print(f"Grafo atual: {len(G.nodes())} disciplinas, {len(G.edges())} conflitos\n")
        print("1. Visualizar grafo (mostra a última coloração, se houver)")
        print("2. Exibir detalhes e métricas do grafo")
        print("3. Rodar Algoritmo de Coloração (GCol)")
        print("4. Carregar outro grafo")
        print("0. Sair")
        
        escolha = input("\nEscolha uma opção: ")
        
        if escolha == '1':
            visualizar_grafo(G, coloracao_recente)
            
        elif escolha == '2':
            exibir_detalhes_grafo(G)
            
        elif escolha == '3':
            coloracao_recente = menu_coloracao(G, coloracao_recente)
            if coloracao_recente:
                 print("\nColoração armazenada. Use '1. Visualizar' para ver o resultado gráfico.")
        
        elif escolha == '4':
            novo_G = selecionar_e_carregar_grafo()
            if novo_G:
                G = novo_G # Substitui o grafo atual pelo novo
                coloracao_recente = None # Reseta a coloração
                print("--- Grafo atualizado. Coloração anterior foi resetada. ---")
                 
        elif escolha == '0':
            print("Encerrando o programa.")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

# Colocar o main em um arquivo separado depois
if __name__ == "__main__":
    
    print("------------------------------------------")
    print("Trabalho de coloração em Grafos \n" \
    "utilizando as bibliotecas NetworkX e GCol")
    print("------------------------------------------")
    
    G_inicial = selecionar_e_carregar_grafo()
    
    if G_inicial:
        exibir_menu(G_inicial)
    else:
        print("Não foi possível carregar um grafo inicial. Encerrando.")