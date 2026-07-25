"""
predict.py — Pipeline utama inferensi
Memanggil semua fungsi dari utils/ secara berurutan:

  1. preprocessing.py  → remove background + crop center
  2. dn2.py      → gatekeeper (lolos / ditolak)
  3. klasifikasi.py    → klasifikasi kelas siput (jika lolos)
"""

from PIL import Image

from utils.preprocessing import remove_background
from utils.dn2     import load_dn2, predict_dn2
from utils.klasifikasi   import load_klasifikasi, predict_klasifikasi


# ── Load semua model ──────────────────────────────────────

def load_models(dn2_dir: str, keras_path: str, label_path: str) -> dict:
    """
    Load semua komponen model sekaligus.
    Dipanggil SEKALI saat app.py start.
    """
    pc = load_dn2(dn2_dir)
    kl = load_klasifikasi(keras_path, label_path)
    return {'pc': pc, 'kl': kl}


# ── Pipeline utama ────────────────────────────────────────

def predict(pil_img: Image.Image, models: dict) -> dict:
    """
    Jalankan pipeline lengkap pada gambar input.

    Returns dict:
      - status     : 'lolos' atau 'ditolak'
      - label      : nama kelas (None jika ditolak)
      - confidence : float (None jika ditolak)
      - all_probs  : list [{'label', 'prob'}] (kosong jika ditolak)
      - gate_score : anomaly score dari DN2
      - threshold  : batas threshold DN2
    """
    # Step 1 — Preprocessing
    processed = remove_background(pil_img)

    # Step 2 — Gatekeeper DN2
    gate = predict_dn2(processed, models['pc'])

    if not gate['lolos']:
        return {
            'status'    : 'ditolak',
            'label'     : None,
            'confidence': None,
            'all_probs' : [],
            'gate_score': gate['score'],
            'threshold' : gate['threshold'],
        }

    # Step 3 — Klasifikasi VGG16
    result = predict_klasifikasi(processed, models['kl'])

    return {
        'status'    : 'lolos',
        'label'     : result['label'],
        'confidence': result['confidence'],
        'all_probs' : result['all_probs'],
        'gate_score': gate['score'],
        'threshold' : gate['threshold'],
    }
