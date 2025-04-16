import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# === PARTE 1: REGRESSÃO PARA OBTER kh E ke BASE ===

# Carregar o dataset
df = pd.read_csv("perdasPorFrequenciaDataset.csv", sep=';', decimal=',')
df.columns = ["Frequencia_Hz", "Pc_W_kg"]

# Regressão: Pc = a*f + b*f²
f = df["Frequencia_Hz"].values.reshape(-1, 1)
f_squared = (df["Frequencia_Hz"]**2).values.reshape(-1, 1)
X = np.hstack([f, f_squared])
y = df["Pc_W_kg"].values

model = LinearRegression()
model.fit(X, y)

a = model.coef_[0]  # kh
b = model.coef_[1]  # b = ke * 4*pi²
intercept = model.intercept_

kh = a
ke_base = b / (4 * np.pi**2)

print(f"Regressão: Pc = {a:.6f} * f + {b:.6f} * f² + {intercept:.6f}")
print(f"kh (histerese): {kh:.6e} W·s/kg")
print(f"ke base (da regressão): {ke_base:.6e} W·s²/kg\n")

# === PARTE 2: CÁLCULO DE ke ASSUMINDO SOMENTE Pe PARA CADA ESPESSURA ===

f_fixed = 60  # Hz
B = 1         # Tesla

perdas = {
    "0.356 mm": 1.44,
    "0.470 mm": 2.20,
    "0.634 mm": 2.64
}

ke_por_chapa = {}

print("\nCálculo de ke para cada chapa considerando apenas Pe = ke*(2πf)²*B\n")

for espessura, Pe in perdas.items():
    ke = Pe / ((2 * np.pi * f_fixed) ** 2 * B)
    ke_por_chapa[espessura] = ke
    print(f"{espessura}: ke = {ke:.6e} W·s²/kg")

# === PARTE 3: CURVAS DE Pe, Pc e Ph ===

f_plot = np.linspace(1, 200, 300)
Ph_curve = kh * f_plot * B  # mesma para todas as chapas

plt.figure(figsize=(10, 6))

for espessura, ke in ke_por_chapa.items():
    Pe_curve = ke * (2 * np.pi * f_plot)**2 * B
    Pc_curve = Ph_curve + Pe_curve
    plt.plot(f_plot, Pe_curve, '--', label=f"Pe - {espessura}")
    plt.plot(f_plot, Pc_curve, '-', label=f"Pc - {espessura}")

plt.plot(f_plot, Ph_curve, ':k', linewidth=2, label="Ph (comum)")
plt.title("Perdas Magnéticas: Pc, Pe e Ph")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Perda (W/kg)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("curvas_pe_pc_ph_por_espessura.png", dpi=300)
plt.close()

print("✅ Gráfico salvo: curvas_pe_pc_ph_por_espessura.png")
