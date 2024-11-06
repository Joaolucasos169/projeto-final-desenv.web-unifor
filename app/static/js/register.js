document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const userData = {
        nome: document.getElementById('nome').value,
        sobrenome: document.getElementById('sobrenome').value,
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value,
        dataNascimento: document.getElementById('data_nascimento').value
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message); // Mostra mensagem de sucesso
            window.location.href = result.redirect; // Redireciona para a página de login
        } else {
            alert(result.error); // Mostra mensagem de erro
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao cadastrar. Tente novamente mais tarde.');
    }
});
