"""
utils/transforms.py
Tanggung jawab:
  - Resize gambar ke ukuran input masing-masing model
  - Rescale / normalisasi nilai pixel

Dipanggil oleh dn.py dan klasifikasi.py masing-masing.
"""

import numpy as np
from PIL import Image
from torchvision import transforms


# ── Untuk DN2 (backbone VGG16 PyTorch) ──────────────
# Input: 224x224, normalisasi ImageNet
dn2_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])


# ── Untuk Klasifikasi (VGG16 Keras / TensorFlow) ──────────
# Input: 224x224, rescale 1./255
def prepare_for_keras(pil_img: Image.Image) -> np.ndarray:
    """
    Resize ke 224x224 dan rescale pixel ke [0, 1].

    Parameters:
        pil_img : PIL.Image RGB

    Returns:
        numpy array shape (1, 224, 224, 3), dtype float32
    """
    img = pil_img.resize((224, 224)).convert('RGB')
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0) # batch dimension
