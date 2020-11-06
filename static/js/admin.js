var handlerEdit = (id, titulo, frase, urlImagen) => {
    document.getElementById('idpregunta').value = id
    document.getElementById('pregunta').value = titulo
    document.getElementById('url_imagen').value = urlImagen
    document.getElementById('respuesta').value = frase
}