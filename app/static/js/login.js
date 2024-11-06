document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message); // Exibe mensagem de sucesso
            window.location.href = "/home"; // Ajuste a URL conforme necessário
        } else {
            alert(result.error); // Exibe mensagem de erro
        }
    } catch (error) {
        console.error("Erro ao fazer login:", error);
        alert("Erro ao conectar com o servidor.");
    }
});
