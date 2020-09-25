//CAPTURAMOS EL ENTER DEL CUADRO
document.addEventListener("DOMContentLoaded", () => {

var inputChat = document.getElementById('input-chat')
var buttonChat = document.getElementById('boton-chat')

inputChat.addEventListener("keyup", (e) => {
    if (e.code == 'Enter') {
        enviarMensaje(inputChat.value)
        inputChat.value = "";
    }
})

buttonChat.addEventListener('click', () => {
    enviarMensaje(inputChat.value)
    inputChat.value = "";
})

});

var enviarMensaje = (text) => {

    if(text == ''){
        return;
    }
    var divChat = document.getElementById("div-mensajes-chat")

    //Creamos el elemento en el chat
    var mensajeUser = document.createElement("div")
    mensajeUser.innerHTML = text
    mensajeUser.classList.add('mensaje-chat','user')
    divChat.appendChild(mensajeUser)

    //Realizamos la petición al servidor
    var req = new XMLHttpRequest();
    req.onreadystatechange = (response) => {
        if(req.readyState == 4 && req.status == 200) {
            console.log(req.responseText)
            var mensajepc = document.createElement("div")
            mensajepc.innerHTML = req.responseText
            mensajepc.classList.add('mensaje-chat','pc')
            divChat.appendChild(mensajepc)
        } else if(req.status == '404' || req.status == '405' ) {
            console.log('no hubo respuesta')
        }
    }
    req.open('POST', '/api/chatbot', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("text=" + text);
}