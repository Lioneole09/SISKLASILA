"""
utils/preprocessing.py
Tanggung jawab:
  - Hapus background dengan rembg
  - Crop objek + center di canvas putih (square 1:1)
"""

import numpy as np
from PIL import Image, ImageOps
from rembg import remove
from io import BytesIO


def _crop_object_center(img_rgba: Image.Image, padding: int = 20) -> Image.Image:
    """Crop ketat ke objek berdasarkan alpha channel, lalu center di canvas putih square."""
    alpha = np.array(img_rgba.split()[3])
    mask  = alpha > 10
    rows  = np.any(mask, axis=1)
    cols  = np.any(mask, axis=0)

    if not rows.any() or not cols.any():
        bg = Image.new('RGB', img_rgba.size, (255, 255, 255))
        bg.paste(img_rgba, mask=img_rgba.split()[3])
        return bg

    h, w   = alpha.shape
    top    = max(0, np.argmax(rows) - padding)
    bottom = min(h, len(rows) - np.argmax(rows[::-1]) + padding)
    left   = max(0, np.argmax(cols) - padding)
    right  = min(w, len(cols) - np.argmax(cols[::-1]) + padding)

    bg      = Image.new('RGB', img_rgba.size, (255, 255, 255))
    bg.paste(img_rgba, mask=img_rgba.split()[3])
    cropped = bg.crop((left, top, right, bottom))

    cw, ch = cropped.size
    size   = max(cw, ch)
    square = Image.new('RGB', (size, size), (255, 255, 255))
    square.paste(cropped, ((size - cw) // 2, (size - ch) // 2))
    return square


def remove_background(pil_img: Image.Image, padding: int = 20) -> Image.Image:
    """
    Hapus background gambar menggunakan rembg, lalu crop + center objek.

    Parameters:
        pil_img : PIL.Image input (dari upload)
        padding : jarak tepi crop ke objek (pixel)

    Returns:
        PIL.Image RGB dengan background putih, objek di tengah
    """
    pil_img = ImageOps.exif_transpose(pil_img)

    buf = BytesIO()
    pil_img.save(buf, format='PNG')
    result_bytes = remove(buf.getvalue())

    img_rgba  = Image.open(BytesIO(result_bytes)).convert('RGBA')
    final_img = _crop_object_center(img_rgba, padding=padding)
    return final_img  # RGB

# def remove_background(pil_img: Image.Image, padding: int = 20) -> Image.Image:
#     pil_img = ImageOps.exif_transpose(pil_img)

#     buf = BytesIO()
#     pil_img.save(buf, format='PNG')
#     result_bytes = remove(buf.getvalue())

#     img_rgba  = Image.open(BytesIO(result_bytes)).convert('RGBA')
#     final_img = _crop_object_center(img_rgba, padding=padding)
    
#     # ── Debug: simpan hasil preprocessing ──
#     final_img.save('debug_preprocessing.png')
    
#     return final_img
