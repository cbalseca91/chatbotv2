var handlerEdit = (id, titulo, frase, urlImagen, source_imagen) => {
    document.getElementById('idpregunta').value = id
    document.getElementById('pregunta').value = titulo
    document.getElementById('url_imagen').value = urlImagen
    document.getElementById('source_imagen').value = source_imagen
    document.getElementById('respuesta').value = frase
}