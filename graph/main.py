import networkx as nx

filename = "as19991224.txt"

G = nx.read_edgelist(filename, delimiter='\t', comments='#', create_using=nx.Graph())

print(f"Файл: {filename}")
print(f"Всего вершин: {G.number_of_nodes()}, рёбер: {G.number_of_edges()}\n")

best_pair = None

for u, v in G.edges():
    if G.degree[u] >= 10 and G.degree[v] >= 10:
        # Проверяем наличие общих соседей
        common_neighbors = list(nx.common_neighbors(G, u, v))
        if len(common_neighbors) == 0:
            best_pair = (u, v)
            break

if best_pair:
    print(f"Лучшая пара слабо связанных графов: {best_pair}")