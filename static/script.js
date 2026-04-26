document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const loading = document.getElementById('loading');
    const resultBox = document.getElementById('quizResult');
    const button = document.getElementById('generateBtn');

    resultBox.innerHTML = '';
    loading.classList.remove('hidden');
    button.disabled = true;
    button.innerText = "⏳ Generating...";

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        loading.classList.add('hidden');
        button.disabled = false;
        button.innerText = "🚀 Generate Quiz";
        resultBox.innerText = data.quiz || 'No quiz generated.';
    })
    .catch(error => {
        loading.classList.add('hidden');
        button.disabled = false;
        button.innerText = "🚀 Generate Quiz";
        console.error('Error:', error);
        alert("Something went wrong!");
    });
});
