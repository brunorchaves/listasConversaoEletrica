import pandas as pd
import matplotlib.pyplot as plt

# Lê o CSV com o separador correto
df = pd.read_csv("points.csv", delimiter=';', header=None)

# Extrai o valor de y da primeira coluna (parte após a vírgula)
y_values = df[0].str.split(',', expand=True)[1].astype(float)

# Plota y em função do índice
plt.figure(figsize=(10, 5))
plt.plot(range(1, len(y_values) + 1), y_values, marker='o', color='orange')
plt.title('Valores de y em função do índice da amostra')
plt.xlabel('Índice da amostra')
plt.ylabel('Valor de y')
plt.grid(True)
plt.tight_layout()
plt.show()
