function limpiarArchivo() {
    document.querySelector('input[type="file"]').value = "";
    document.getElementById('progressContainer').style.display = 'none';
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressText').textContent = '0%';
    document.getElementById('progressBar').style.backgroundColor = '#4CAF50';
}

document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    const fileInput = document.querySelector('input[type="file"]');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const form = e.target;

    if (!fileInput.files.length) {
        alert('Selecciona un archivo primero');
        return;
    }

    progressContainer.style.display = 'block';

    // Usar FormData para la subida
    const formData = new FormData(form);
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', function (event) {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            progressBar.style.width = percentComplete + '%';
            progressText.textContent = Math.round(percentComplete) + '%';
        }
    });

    xhr.addEventListener('load', function () {
        if (xhr.status === 200) {
            // Obtenemos el nombre del archivo
<<<<<<< HEAD
           //const fileName = fileInput.files[0].name;
            const fileCount = fileInput.files.length;
            // Mostramos "Terminado!!" y el nombre del archivo
            progressText.innerHTML = 'Terminado!!<br><small>' + fileCount + '</small>';
=======
            const fileNames = Array.from(fileInput.files).map(file => file.name).join(', ');
            // const fileName = fileInput.files[0].name;
            // Mostramos "Terminado!!" y el nombre del archivo
            progressText.innerHTML = 'Terminado!!<br><small>' + fileNames + '</small>';
>>>>>>> 72b289b (archivos modificados)
        } else {
            progressBar.style.backgroundColor = '#f44336';
            progressText.textContent = 'Falló al subir!!';
        }
    });

    xhr.addEventListener('error', function () {
        progressBar.style.backgroundColor = '#f44336';
        progressText.textContent = 'Falló al subir!!';
    });

    xhr.open('POST', form.action);
    xhr.send(formData);
});
