// ── Upload & Preview
const fileInput   = document.getElementById('fileInput');
const uploadArea  = document.getElementById('uploadArea');
const previewWrap = document.getElementById('previewWrap');
const previewImg  = document.getElementById('previewImg');
const previewMeta = document.getElementById('previewMeta');
const btnReset    = document.getElementById('btnReset');
const btnClassify = document.getElementById('btnClassify');

// ── Result
const resultPlaceholder = document.getElementById('resultPlaceholder');
const topPred           = document.getElementById('topPred');
const resultWrap        = document.getElementById('resultWrap');
const resultImg         = document.getElementById('resultImg');
const resultImgLabel    = document.getElementById('resultImgLabel');
const topLabel          = document.getElementById('topLabel');
const topConf           = document.getElementById('topConf');
const probList          = document.getElementById('probList');
const spinner           = document.getElementById('spinner');

let currentFile = null;

function showPreview(file) {
  currentFile = file;
  const url = URL.createObjectURL(file);
  previewImg.src = url;
  previewMeta.textContent = `${file.name}  ·  ${(file.size/1024).toFixed(1)} KB`;
  uploadArea.style.display = 'none';
  previewWrap.classList.add('show');
  btnClassify.disabled = false;
}

function resetUpload() {
  currentFile = null;
  fileInput.value = '';
  previewImg.src = '';
  uploadArea.style.display = 'flex';
  previewWrap.classList.remove('show');
  btnClassify.disabled = true;
  document.getElementById('pesanDitolak').style.display = 'none';
  resetResult();
}

fileInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;

  if (file.size > 10 * 1024 * 1024) {
    alert('Ukuran file maksimal 10MB!');
    fileInput.value = '';
    return;
  }

  showPreview(file);
});

uploadArea.addEventListener('dragover', e => { e.preventDefault(); uploadArea.classList.add('dragover'); });
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
uploadArea.addEventListener('drop', e => {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
  const f = e.dataTransfer.files[0];
  if (!f) return;

  if (f.size > 10 * 1024 * 1024) {
    alert('Ukuran file maksimal 10MB!');
    return;
  }

  if (f.type.startsWith('image/')) showPreview(f);
});

btnReset.addEventListener('click', resetUpload);

function resetResult() {
  resultPlaceholder.style.display = 'flex';
  spinner.style.display = 'none';
  resultWrap.classList.remove('show');
}

function renderDitolak(data) {
  resetResult();

  // Tampilkan pesan error di bawah tombol
  const pesanDitolak = document.getElementById('pesanDitolak');
  pesanDitolak.style.display = 'block';
}

function renderResult(predictions, gateScore, threshold) {
  // Reset warna top-pred (jika sebelumnya ditolak)
  topPred.style.background   = '';
  topPred.style.borderColor  = '';
  topLabel.style.color       = '';
  topConf.style.color        = '';

  resultImg.src = previewImg.src;

  const top = predictions[0];
  topLabel.textContent = top.label;
  topConf.textContent  = (top.prob * 100).toFixed(2) + '%';
  resultImgLabel.textContent = top.label;

  const pct = (top.prob * 100).toFixed(2);
  probList.innerHTML = `
    <div class="prob-item">
      <div class="prob-row">
        <span class="prob-name">Confidence</span>
        <span class="prob-val">${pct}%</span>
      </div>
      <div class="prob-bar-bg">
        <div class="prob-bar top" style="width:0%" data-w="${pct}%"></div>
      </div>
    </div>`;

  requestAnimationFrame(() => {
    document.querySelectorAll('.prob-bar').forEach(b => b.style.width = b.dataset.w);
  });

  spinner.style.display = 'none';
  resultWrap.classList.add('show');
}

// ── Classify 
btnClassify.addEventListener('click', async () => {
  if (!currentFile) return;

  resultPlaceholder.style.display = 'none';
  resultWrap.classList.remove('show');
  spinner.style.display = 'block';
  btnClassify.disabled = true;

  try {
    const formData = new FormData();
    formData.append('file', currentFile);

    const res  = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();

    if (data.error) {
      alert('Error: ' + data.error);
      resetResult();
      return;
    }

    if (data.status === 'ditolak') {
      renderDitolak(data);
    } else {
      renderResult(data.all_probs, data.gate_score, data.threshold);
    }

  } catch (err) {
    alert('Gagal menghubungi server: ' + err.message);
    resetResult();
  } finally {
    btnClassify.disabled = false;
    spinner.style.display = 'none';
  }
});
