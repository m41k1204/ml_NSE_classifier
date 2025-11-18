import torch
import numpy as np
import pandas as pd
from PIL import Image
from torchvision import transforms
from pathlib import Path
from tqdm import tqdm
import os
import time

# Optimización CPU
torch.set_num_threads(12)
os.environ["OMP_NUM_THREADS"] = "12"

device = torch.device("cpu")
print(f"Usando: {device} con {torch.get_num_threads()} threads")

# Cargar modelo
print("Cargando DINOv2...")
model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
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
    """Carga rutas desde carpetas de categorías"""
    base_path = Path(base_path)
    image_paths = []
    labels = []
    categories = []

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


def extract_features(image_paths, batch_size=16):
    """Extrae features con contador detallado"""
    n = len(image_paths)
    features = np.zeros((n, 768), dtype=np.float32)

    start_time = time.time()
    errors = 0

    # Barra de progreso con detalles
    pbar = tqdm(
        total=n,
        desc="Extrayendo features",
        unit="img",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
    )

    with torch.no_grad():
        for i in range(0, n, batch_size):
            batch_start = time.time()
            batch_paths = image_paths[i : i + batch_size]
            batch = []

            for path in batch_paths:
                try:
                    img = Image.open(path).convert("RGB")
                    batch.append(transform(img))
                except Exception as e:
                    errors += 1
                    batch.append(torch.zeros(3, 224, 224))

            batch_tensor = torch.stack(batch)
            feat = model(batch_tensor).numpy()
            features[i : i + len(batch)] = feat

            # Actualizar progreso
            pbar.update(len(batch))

            # Calcular estadísticas cada 100 imágenes
            if (i + batch_size) % 100 == 0 or (i + batch_size) >= n:
                elapsed = time.time() - start_time
                processed = min(i + batch_size, n)
                imgs_per_sec = processed / elapsed
                remaining_imgs = n - processed
                eta_seconds = remaining_imgs / imgs_per_sec if imgs_per_sec > 0 else 0

                # Actualizar descripción
                pbar.set_postfix(
                    {
                        "img/s": f"{imgs_per_sec:.1f}",
                        "ETA": f"{eta_seconds/60:.1f}min",
                        "errors": errors,
                    }
                )

    pbar.close()

    # Resumen final
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"✅ Extracción completada!")
    print(f"   Tiempo total: {total_time/60:.1f} minutos ({total_time:.1f} segundos)")
    print(f"   Imágenes procesadas: {n}")
    print(f"   Velocidad promedio: {n/total_time:.2f} img/s")
    print(f"   Errores: {errors}")
    print(f"{'='*60}\n")

    return features


# ============ EJECUTAR ============

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("🏙️  EXTRACCIÓN DE FEATURES - NIVEL SOCIOECONÓMICO")
    print(f"{'='*60}\n")

    # Cargar datos
    base_path = "images"
    image_paths, labels, categories = load_images_from_folders(base_path)

    # Estimación de tiempo
    estimated_time = len(image_paths) * 0.5 / 60
    print(f"\n⏱️  Tiempo estimado: ~{estimated_time:.1f} minutos")
    print(f"⏳ Iniciando extracción...\n")

    # Extraer features
    X = extract_features(image_paths, batch_size=16)

    # Crear DataFrame
    df = pd.DataFrame(
        {"image_path": image_paths, "label": labels, "category": categories}
    )

    # Guardar
    print("💾 Guardando archivos...")
    np.save("X_features.npy", X)
    df.to_csv("y_labels.csv", index=False)

    print(f"\n{'='*60}")
    print("📊 ARCHIVOS GENERADOS:")
    print(f"{'='*60}")
    print(f"   ✓ X_features.npy - Shape: {X.shape}")
    print(f"   ✓ y_labels.csv - {len(df)} registros")
    print(f"\n📈 Distribución de categorías:")
    print(df["category"].value_counts().to_string())
    print(f"{'='*60}\n")
