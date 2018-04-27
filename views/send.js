//Script sender

var socket = io();

function sendFileById(context) {
    let data = context.getImageData(0, 0, 280, 280);

    socket.emit('picture', { image: true, buffer: data.value });
}
