import cv2
import numpy as np

# Carregar imagem
img = cv2.imread('grafico.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar detecção de bordas para melhorar a segmentação
edges = cv2.Canny(img, 50, 150)

# Detectar contornos
contornos, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Criar uma imagem colorida para desenhar
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# Garantir que temos ao menos dois contornos para preencher a histerese
if len(contornos) >= 2:
    # Ordenar contornos pelo tamanho (maiores primeiro)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
    contorno_externo, contorno_interno = contornos[:2]
    
    # Criar uma máscara e preencher entre os contornos
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, [contorno_externo], -1, 255, thickness=cv2.FILLED)
    cv2.drawContours(mask, [contorno_interno], -1, 0, thickness=cv2.FILLED)
    
    # Pintar a área dentro da histerese
    img_color[mask == 255] = [0, 0, 255]
    
    # Calcular a área interna da histerese
    area = np.sum(mask == 255)
    print(f"Área estimada: {area:.2f} pixels²")
else:
    print("Contornos insuficientes detectados para preencher a histerese.")

# Mostrar a imagem com a área pintada
cv2.imshow('Área da Histerese', img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
