"""
utils/dn2.py
Tanggung jawab:
  - Load komponen DN2 (FAISS index + config + backbone VGG16 PyTorch)
  - Ekstraksi fitur (VGG16)
  - Inferensi gatekeeper: lolos / ditolak
"""

import numpy as np
import faiss
import joblib
import torch
import cv2
from torchvision import models
from PIL import Image

from utils.transforms import dn2_transform


# ── Load ──────────────────────────────────────────────────

def load_dn2(model_dir: str) -> dict:
    """
    Load FAISS index, config, dan backbone VGG16 PyTorch.

    Parameters:
        model_dir : path ke folder dn2_model/

    Returns:
        dict berisi index, config, backbone, device
    """
    index  = faiss.read_index(f'{model_dir}/dn2_index.faiss')
    config = joblib.load(f'{model_dir}/config.pkl')

    device   = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    backbone = models.vgg16(weights=None).features
    backbone.load_state_dict(
        torch.load(f'{model_dir}/vgg16_backbone.pth', map_location=device)
    )
    backbone = backbone.to(device).eval()

    return {
        'index'   : index,
        'config'  : config,
        'backbone': backbone,
        'device'  : device,
    }


# ── Ekstraksi Fitur ───────────────────────────────────────

def _extract_vgg(pil_img: Image.Image, backbone, device) -> np.ndarray:
    t = dn2_transform(pil_img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = backbone(t).mean(dim=[2, 3])
    return feat.cpu().numpy().flatten().astype(np.float32)


def _extract_embedding(pil_img: Image.Image, backbone, device) -> np.ndarray:
    vgg = _extract_vgg(pil_img, backbone, device)
    vgg = vgg / (np.linalg.norm(vgg) + 1e-8)
    return vgg


# ── Inferensi ─────────────────────────────────────────────

def predict_dn2(pil_img: Image.Image, pc: dict) -> dict:
    """
    Jalankan gatekeeper dn2 pada gambar.

    Parameters:
        pil_img : PIL.Image RGB (sudah dipreproses)
        pc      : dict hasil load_dn2()

    Returns:
        {
            'lolos'    : bool,
            'score'    : float,
            'threshold': float,
        }
    """
    feat    = _extract_embedding(pil_img, pc['backbone'], pc['device']).reshape(1, -1)
    dist, _ = pc['index'].search(feat, k=pc['config']['k'])
    score   = float(np.mean(dist))
    lolos   = score <= pc['config']['threshold']

    return {
        'lolos'    : lolos,
        'score'    : round(score, 6),
        'threshold': round(pc['config']['threshold'], 6),
    }