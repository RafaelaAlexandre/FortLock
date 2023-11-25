// Copia o texto do input para a área de transferência
Array.from(document.getElementsByClassName('copiarSenha')).forEach(botao => {
    botao.addEventListener('click', (evento) => {
        let idBotao = evento.target.id;

        let senha = document.getElementById(`senhaCofre${idBotao}`);

        // Criar um elemento temporário (textarea)
        let textareaTemporario = document.createElement('textarea');

        // Configurar o valor do elemento temporário com o valor da senha
        textareaTemporario.value = senha.value;

        // Adicionar o elemento temporário ao DOM
        document.body.appendChild(textareaTemporario);

        // Selecionar e copiar o conteúdo do elemento temporário
        textareaTemporario.select();
        document.execCommand('copy');

        // Remover o elemento temporário
        document.body.removeChild(textareaTemporario);

        alert('Senha copiada para a área de transferência: ' + senha.value);
    });
});