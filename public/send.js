//Script sender

var socket = io('/drawer');

function sendFileById(context) {
    //let data = context.getImageData(0, 0, 280, 280);
    let crx = document.getElementById("canvas");
    let data = crx.toDataURL("image/png");
    console.log(data);
    socket.emit('picture', { image: true, buffer: data });
    socket.on('result', (sok) => {
	alert("Le nombre détecté est " + sok);
    });
}
