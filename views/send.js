//Script sender

function sendFileById(id) {
    let data = getElementById(id);

    socket.emit('picture', { image: true, buffer: data.value });
}