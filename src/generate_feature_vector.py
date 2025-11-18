import torch
import numpy as np
import pandas as pd
from PIL import Image
from torchvision import transforms
from pathlib import Path
from tqdm import tqdm

# Configuración
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando: {device}")

# Cargar modelo
print("Cargando DINOv2...")
model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
model = model.to(device)
model.eval()

# Transform
transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def load_images_from_folders(base_path):
    """
    Carga rutas de imágenes desde carpetas de categorías

    Returns:
        image_paths: lista de rutas
        labels: lista de etiquetas
        categories: lista de nombres de categorías
    """
    base_path = Path(base_path)
    image_paths = []
    labels = []
    categories = []

    # Obtener carpetas de categorías
    category_folders = sorted([d for d in base_path.iterdir() if d.is_dir()])

    print(f"\n📁 Categorías encontradas:")
    for idx, folder in enumerate(category_folders):
        cat_name = folder.name
        images = list(folder.glob("*.jpg")) + list(folder.glob("*.png"))

        print(f"   {idx}: {cat_name} - {len(images)} imágenes")

        for img_path in images:
            image_paths.append(str(img_path))
            labels.append(idx)
            categories.append(cat_name)

    print(f"\n✅ Total: {len(image_paths)} imágenes")
    return image_paths, labels, categories


def extract_features(image_paths, batch_size=32):
    """Extrae features"""
    n = len(image_paths)
    features = np.zeros((n, 768), dtype=np.float32)

    with torch.no_grad():
        for i in tqdm(range(0, n, batch_size), desc="Extrayendo features"):
            batch_paths = image_paths[i : i + batch_size]
            batch = []

            for path in batch_paths:
                try:
                    img = Image.open(path).convert("RGB")
                    batch.append(transform(img))
                except Exception as e:
                    print(f"\n⚠️  Error en {path}: {e}")
                    batch.append(torch.zeros(3, 224, 224))

            batch_tensor = torch.stack(batch).to(device)
            feat = model(batch_tensor).cpu().numpy()
            features[i : i + len(batch)] = feat

    return features


# ============ EJECUTAR ============

# Cargar datos
base_path = "images"  # Tu carpeta raíz
image_paths, labels, categories = load_images_from_folders(base_path)

# Extraer features
print("\n🚀 Extrayendo features...")
X = extract_features(image_paths, batch_size=32)

# Crear DataFrame con metadata
df = pd.DataFrame({"image_path": image_paths, "label": labels, "category": categories})

# Guardar
print("\n💾 Guardando archivos...")
np.save("X_features.npy", X)
df.to_csv("y_labels.csv", index=False)

print(f"\n✅ Completado!")
print(f"   Features: X_features.npy - Shape: {X.shape}")
print(f"   Labels: y_labels.csv - {len(df)} registros")
print(f"\nCategorías:")
print(df["category"].value_counts())
