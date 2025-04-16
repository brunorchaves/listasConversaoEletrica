import matplotlib.pyplot as plt

# Dados fornecidos
B = [0.25, 0.4, 0.6, 0.75, 1.1, 1.25, 1.4]  # Valores de B (T)
H = [9, 10.5, 15, 20, 32, 48, 140]          # Valores de H (A/m)

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.plot(H, B, marker='o', linestyle='-', color='b', label='Curva de Magnetização')

# Adicionando título e rótulos
plt.title('Curva de Magnetização', fontsize=16)
plt.xlabel('Campo Magnético H (A/m)', fontsize=14)
plt.ylabel('Densidade de Fluxo Magnético B (T)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# Adicionando anotações para cada ponto
for i in range(len(B)):
    plt.annotate(f'({H[i]}, {B[i]})', (H[i], B[i]), textcoords="offset points", xytext=(5,5), ha='left')

# Ajustando os limites dos eixos
plt.xlim(0, max(H) + 10)
plt.ylim(0, max(B) + 0.2)

# Mostrando a legenda
plt.legend(fontsize=12)

# Exibindo o gráfico
plt.show()