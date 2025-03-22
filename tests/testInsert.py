import sqlite3
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar ao banco de dados
conn = sqlite3.connect('HeartRateMonitoring.sqlite3')
cursor = conn.cursor()

# Definir a query de INSERT
insert_query = """
INSERT INTO session VALUES (?, 'testName2', 'testTeacher2', 'testDescription2', '18-03-2025', '16h', 100, 0);
"""

# Inicializar variáveis para medição de tempo
total_start_time = time.time()
individual_times = []

# Loop para inserir 1000 valores
for session_id in range(2, 102):  # IDs de 2 a 1001
    start_time = time.time()  # Iniciar medição de tempo para esta inserção

    # Executar a query de INSERT com o session_id atual
    cursor.execute(insert_query, (session_id,))

    # Commit da transação (necessário para INSERT)
    conn.commit()

    end_time = time.time()  # Finalizar medição de tempo para esta inserção
    insert_time = end_time - start_time
    individual_times.append(insert_time)  # Armazenar o tempo desta inserção

    print(f"INSERT para session_id={session_id} executado em {insert_time:.4f} segundos")

# Calcular o tempo total decorrido
total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time

# Calcular o tempo médio por inserção
average_time_per_insert = sum(individual_times) / len(individual_times)

# Fechar a conexão com o banco de dados
conn.close()

# Exibir os resultados
print(f"\nNúmero total de inserções: 10000")
print(f"Tempo total: {total_elapsed_time:.4f} segundos")
print(f"Tempo médio por inserção: {average_time_per_insert:.4f} segundos")

# Criar o gráfico de distribuição
plt.figure(figsize=(10, 6))
sns.histplot(individual_times, kde=True, color='blue', bins=30)  # Histograma com curva de densidade

# Adicionar a linha do tempo médio
plt.axvline(average_time_per_insert, color='red', linestyle='--', label=f'Average time: {average_time_per_insert:.4f} seconds')

# Personalizar o gráfico
plt.title(f'Total Insertions: 10000, Total Time: {total_elapsed_time:.4f} s')
plt.xlabel('Operation Time (in seconds)')
plt.ylabel('Frequency')
plt.legend(loc='upper right')  # Posicionar a legenda no canto superior direito
plt.show()