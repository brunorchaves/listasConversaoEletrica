import matplotlib.pyplot as plt
import numpy as np

# Dados fornecidos
B = [0.25, 0.4, 0.6, 0.75, 1.1, 1.25, 1.4]  # Valores de B (T)
H = [9, 10.5, 15, 20, 32, 48, 140]          # Valores de H (A/m)


# Pontos selecionados para a reta
p1 = (H[0], B[0])  # (9, 0.25)
p2 = (H[4], B[4])  # (32, 1.1)

# Cálculo da inclinação (constante μ = ΔB / ΔH)
delta_B = p2[1] - p1[1]
delta_H = p2[0] - p1[0]
mu = delta_B / delta_H  # Permeabilidade magnética aproximada

# Equação da reta: B = μ * H + interceptação
# Usando o ponto p1 para encontrar a interceptação:
intercept = p1[1] - mu * p1[0]

# Gerando pontos para a reta
H_line = np.linspace(0, max(H) + 10, 100)
B_line = mu * H_line + intercept

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.plot(H, B, marker='o', linestyle='-', color='b', label='Curva de Magnetização')
plt.plot(H_line, B_line, 'r--', label=f'Reta de Aproximação (μ = {mu:.4f} T·m/A)')

# Adicionando título e rótulos
plt.title('Curva de Magnetização com Aproximação Linear', fontsize=16)
plt.xlabel('Campo Magnético H (A/m)', fontsize=14)
plt.ylabel('Densidade de Fluxo Magnético B (T)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# Destacando os pontos usados para a reta
plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='red', s=100, zorder=5, label='Pontos para a Reta')

# Ajustando os limites dos eixos
plt.xlim(0, max(H) + 10)
plt.ylim(0, max(B) + 0.2)

# Mostrando a legenda
plt.legend(fontsize=12)

# Exibindo o gráfico
plt.show()

print(f"Constante μ (permeabilidade magnética aproximada): {mu:.4f} T·m/A")