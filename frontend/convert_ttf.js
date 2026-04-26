const dz = document.getElementById('dz');
const fi = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const fileExtEl = document.getElementById('fileExt');
//const removeBtn = document.getElementById('removeBtn');
const convertBtn = document.getElementById('convertBtn');
const progress = document.getElementById('progress');
const progressBar = document.getElementById('progressBar');
const resultEl = document.getElementById('result');
const resultName = document.getElementById('resultName');
const dlBtn = document.getElementById('dlBtn');
const errorEl = document.getElementById('error');

function fmtSize(b) {
    if (b < 1024) return b + ' B';
    if (b < 1048576) return Math.round(b / 1024) + ' KB';
    return (b / 1048576).toFixed(1) + ' MB';
}

function setFile(f) {
    const ext = f.name.split('.').pop().toUpperCase();
    fileExtEl.textContent = ext;
    fileExtEl.style.background = ext === 'OTF' ? '#7F77DD' : '#1D9E75';
    fileExtEl.style.color = ext === 'OTF' ? '#EEEDFE' : '#E1F5EE';
    fileName.textContent = f.name;
    fileSize.textContent = fmtSize(f.size);
    fileInfo.classList.add('show');
    convertBtn.disabled = false;
    resultEl.classList.remove('show');
    errorEl.classList.remove('show');
}

function showError(msg) {
    errorEl.textContent = msg;
    errorEl.classList.add('show');
}

function startProgress() {
    progress.classList.add('show');
    let w = 0;
    return setInterval(() => {
        w = Math.min(w + Math.random() * 20, 88);
        progressBar.style.width = w + '%';
    }, 150);
}

function finishProgress(iv) {
    clearInterval(iv);
    progressBar.style.width = '100%';
    setTimeout(() => { progress.classList.remove('show'); progressBar.style.width = '0'; }, 400);
}

fi.addEventListener('change', e => { if (e.target.files[0]) setFile(e.target.files[0]); });

dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('drag'); });
dz.addEventListener('dragleave', () => dz.classList.remove('drag'));
dz.addEventListener('drop', e => {
    e.preventDefault(); dz.classList.remove('drag');
    const f = e.dataTransfer.files[0];
    if (f && /\.(ttf|otf)$/i.test(f.name)) {
        const dt = new DataTransfer();
        dt.items.add(f);
        fi.files = dt.files;
        setFile(f);
    } else {
        showError('Obsługiwane formaty: .ttf / .otf');
    }
});

/*removeBtn.addEventListener('click', e => {
    e.stopPropagation();
    fileInfo.classList.remove('show');
    convertBtn.disabled = true;
    resultEl.classList.remove('show');
    errorEl.classList.remove('show');
    fi.value = '';
});*/

async function convertFont() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('error');

    if (!fileInput.files.length) {
        showError('Wybierz plik');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    convertBtn.disabled = true;
    convertBtn.innerHTML = 'Konwertuję…';
    errorEl.classList.remove('show');
    resultEl.classList.remove('show');

    const iv = startProgress();

    try {
        const res = await fetch('http://localhost:8000/api/convert/ttf-to-woff2', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) throw new Error(`Serwer zwrócił ${res.status}`);

        const data = await res.json();

        finishProgress(iv);

        resultName.textContent = file.name.replace(/\.(ttf|otf)$/i, '.woff2');
        dlBtn.href = `http://localhost:8000${data.download_url}`;
        resultEl.classList.add('show');

    } catch (err) {
        finishProgress(iv);
        showError('Błąd konwersji: ' + err.message);
        console.error(err);
    }

    convertBtn.disabled = false;
    convertBtn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
      Konwertuj do WOFF2`;
}