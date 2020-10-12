//CAPTURAMOS EL ENTER DEL CUADRO
//CREAMOS UNA VARIBLE GLOBAL
//Almacenamos la pregunta actual, para medir satisfacción.
var _satisfaccion = null
var preguntaOriginal = null
document.addEventListener("DOMContentLoaded", () => {

var inputChat = document.getElementById('input-chat')
var buttonChat = document.getElementById('boton-chat')

inputChat.addEventListener("keyup", (e) => {
    if (e.code == 'Enter') {
        enviarMensaje(inputChat.value,false)
        inputChat.value = "";
    }
})

buttonChat.addEventListener('click', () => {
    enviarMensaje(inputChat.value,false)
    inputChat.value = "";
})

});

var enviarMensaje = (text, saludar) => {

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
            //Se crea elemento de respuesta
            var mensajepc = document.createElement("div")
            mensajepc.innerHTML = req.responseText
            mensajepc.classList.add('mensaje-chat','pc')
            divChat.appendChild(mensajepc)
            //Cambiamos el estado de satisfacción, para la siguiente respuesta
            if( req.responseText.includes("[Si/No]") ){
                _satisfaccion = req.responseText
                preguntaOriginal = text //Almacenamos la pregunta original.
            }
        } else if(req.status == '404' || req.status == '405' ) {
            console.log('no hubo respuesta')

        }
    }
    req.open('POST', '/api/chatbot', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    //Evaluamos si es satisfacción
    if(_satisfaccion){
        req.send("satisfaccion=" + text + "&pregunta=" + _satisfaccion + "&original=" + preguntaOriginal)
    }else{
        req.send("text=" + text);
    }
    _satisfaccion = null
}