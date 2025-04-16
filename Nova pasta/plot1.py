import matplotlib.pyplot as plt
import numpy as np

# Caminho para o arquivo CSV
file_path = "points.csv"  # Substitua com o caminho correto se necessário

# Etapa 1 – Ler e extrair valores brutos de y (parte após o ponto e vírgula)
with open(file_path, 'r') as f:
    raw_lines = f.readlines()

y_raw_values = []
for line in raw_lines:
    parts = line.strip().split(';')
    if len(parts) == 2:
        y_raw = parts[1].replace(',', '.')
        try:
            y_raw_values.append(float(y_raw))
        except ValueError:
            continue  # Ignorar linhas inválidas

# Ordenar os valores de y_raw
y_raw_values.sort()

# Etapa 2 – Ajustar os valores de Pc para [2, 100] W/kg (escala logarítmica)
raw_min = min(y_raw_values)
raw_max = max(y_raw_values)

def log_interp(value, old_min, old_max, new_min, new_max):
    scale = (np.log10(value) - np.log10(old_min)) / (np.log10(old_max) - np.log10(old_min))
    return 10 ** (np.log10(new_min) + scale * (np.log10(new_max) - np.log10(new_min)))

y_adjusted = [log_interp(v, raw_min, raw_max, 2, 100) for v in y_raw_values]

# Etapa 3 – Gerar eixo x (frequência) com espaçamento log entre 60 e 1100 Hz
x_values = np.logspace(np.log10(60), np.log10(1100), num=len(y_adjusted))

# Etapa 4 – Calcular Kh (assumindo B = 1)
kh_values = [pc / f for pc, f in zip(y_adjusted, x_values)]

# Etapa 5 – Plotar Pc em função da frequência
plt.figure(figsize=(10, 6))
plt.plot(x_values, y_adjusted, marker='o', linestyle='-')
plt.xscale('log')
plt.yscale('log')
plt.xlim(60, 1100)
plt.ylim(2, 100)
plt.xlabel('Frequência (Hz) [log]')
plt.ylabel('Pc (W/kg) [log]')
plt.title('Pc ajustado em função da Frequência')
plt.grid(True, which='both', ls='--')
plt.tight_layout()
plt.savefig("pc_vs_frequencia.png", dpi=300)
plt.show()

# Etapa 6 – Plotar Kh em função da frequência
plt.figure(figsize=(10, 6))
plt.plot(x_values, kh_values, marker='o', linestyle='-')
plt.xscale('log')
plt.xlabel('Frequência (Hz) [log]')
plt.ylabel('Kh')
plt.title('Kh em função da Frequência (com B = 1)')
plt.grid(True, which='both', ls='--')
plt.tight_layout()
plt.savefig("kh_vs_frequencia.png", dpi=300)
plt.show()

# Etapa 7 – Estatísticas de Kh
kh_mean = np.mean(kh_values)
kh_min = np.min(kh_values)
kh_max = np.max(kh_values)

print(f"\n--- Estatísticas de Kh ---")
print(f"Kh médio : {kh_mean:.6f}")
print(f"Kh mínimo: {kh_min:.6f}")
print(f"Kh máximo: {kh_max:.6f}")

# Etapa 8 – Cálculo de Ke para diferentes espessuras
f_base = 60  # Hz
B = 1        # T

# Lista de (espessura, Pc)
dados_ke = [
    (0.365, 1.8),
    (0.470, 2.5),
    (0.635, 3.0)
]

# Calcular Ke = Pc / ((2 * pi * f)^2 * B^2)
ke_results = []
for espessura, pc in dados_ke:
    ke = pc / ((2 * np.pi * f_base) ** 2 * B ** 2)
    ke_results.append((espessura, ke))

# Exibir resultados
print("\n--- Cálculo de Ke ---")
for esp, ke in ke_results:
    print(f"Espessura {esp:.3f} m → Ke = {ke:.6f}")

# Etapa 9 – Plot das perdas magnéticas

# Frequência de 60 a 1000 Hz
frequencias = np.linspace(60, 1000, 300)

# Perdas por histerese (mesmo para todas as espessuras)
perdas_histerese = kh_mean * frequencias

plt.figure(figsize=(12, 8))

# Plotar perdas por histerese uma vez
plt.plot(frequencias, perdas_histerese, 'k--', label='Perdas por Histerese (mesma para todas)')

# Para cada espessura, calcular perdas por correntes induzidas e totais
for espessura, ke in ke_results:
    perdas_correntes = ke * (2 * np.pi * frequencias) ** 2
    perdas_totais = perdas_histerese + perdas_correntes

    plt.plot(frequencias, perdas_correntes, ':', label=f'Perdas por Correntes Induzidas - {espessura:.3f} m')
    plt.plot(frequencias, perdas_totais, '-', label=f'Perdas Totais - {espessura:.3f} m')

# Finalizar gráfico
plt.title('Perdas Magnéticas em função da Frequência')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Perdas (W/kg)')
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("perdas_magneticas.png", dpi=300)
plt.show()
