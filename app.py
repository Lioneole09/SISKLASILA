import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, render_template, request, jsonify, redirect, url_for
from PIL import Image
import io
import ast
import joblib

from predict import load_models, predict as run_predict

app = Flask(__name__)

# ── Load semua model SEKALI saat server start ──────────────
MODELS = load_models(
    dn2_dir       = 'model/gatekeeper_model',
    keras_path    = 'model/klasifikasi_model/AbdulKatsir-siputLaut-97.39.h5',
    label_path    = 'model/klasifikasi_model/siputLaut.txt',
)

PC_CONFIG  = joblib.load('model/gatekeeper_model/config.pkl')

with open('model/klasifikasi_model/klasifikasi_metrics.txt', 'r') as f:
    KL_METRICS = ast.literal_eval(f.read().strip())


# ── Halaman ────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('klasifikasi'))

@app.route('/klasifikasi')
def klasifikasi():
    return render_template('klasifikasi.html')

@app.route('/model-info')
def model_info():
    keras_model  = MODELS['kl']['model']
    total_params = keras_model.count_params()
    jumlah_kelas = len(MODELS['kl']['label_dict'])
    kelas_list   = list(MODELS['kl']['label_dict'].values())

    data_klasifikasi = {
        'nama_model'    : 'VGG16',
        'framework'     : 'TensorFlow / Keras',
        'input_size'    : '224 × 224 px',
        'jumlah_kelas'  : jumlah_kelas,
        'kelas'         : kelas_list,
        'total_params'  : f"{keras_model.count_params():,}",
        'trainable'     : f"{sum(w.numpy().size for w in keras_model.trainable_weights):,}",
        'accuracy'      : KL_METRICS['accuracy'],
        'classes'       : KL_METRICS['classes'],
        'best_epoch'    : KL_METRICS['best_epoch'],
    }

    return render_template('model_info.html',
                           klasifikasi=data_klasifikasi)

# ── API Predict ────────────────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict_route():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File kosong'}), 400

    try:
        pil_img = Image.open(io.BytesIO(file.read())).convert('RGB')
        result  = run_predict(pil_img, MODELS)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
