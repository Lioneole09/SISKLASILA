"""
utils/klasifikasi.py
Tanggung jawab:
  - Load model VGG16 .keras dan label kelas dari .txt
  - Inferensi klasifikasi: kembalikan semua probabilitas kelas
"""

import ast
import numpy as np
import tensorflow as tf
from PIL import Image

from utils.transforms import prepare_for_keras


# ── Load ──────────────────────────────────────────────────

def load_klasifikasi(keras_path: str, label_path: str) -> dict:
    """
    Load model VGG16 Keras dan label kelas.

    Parameters:
        keras_path : path ke file .keras
        label_path : path ke file .txt berisi dict {0: 'nama', ...}

    Returns:
        dict berisi model dan label_dict
    """
    model = tf.keras.models.load_model(keras_path)

    with open(label_path, 'r') as f:
        label_dict = ast.literal_eval(f.read().strip())

    return {
        'model'     : model,
        'label_dict': label_dict,
    }


# ── Inferensi ─────────────────────────────────────────────

def predict_klasifikasi(pil_img: Image.Image, kl: dict) -> dict:
    """
    Klasifikasikan gambar menggunakan VGG16 Keras.

    Parameters:
        pil_img : PIL.Image RGB (sudah dipreproses)
        kl      : dict hasil load_klasifikasi()

    Returns:
        {
            'label'    : str,   <- kelas dengan probabilitas tertinggi
            'confidence: float,
            'all_probs': [{'label': str, 'prob': float}, ...],
        }
    """
    arr   = prepare_for_keras(pil_img)
    preds = kl['model'].predict(arr, verbose=0)[0]

    all_probs = [
        {'label': kl['label_dict'][i], 'prob': round(float(preds[i]), 6)}
        for i in range(len(preds))
    ]
    all_probs.sort(key=lambda x: x['prob'], reverse=True)

    return {
        'label'     : all_probs[0]['label'],
        'confidence': all_probs[0]['prob'],
        'all_probs' : all_probs,
    }
