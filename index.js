const express = require('express');
const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);
const child = require('child_process').spawn;

// Drawer socket where come from picture
var drawer = io.of('/drawer');

// Socket getter from front
drawer.on('connection', function (socket) {
    socket.on('picture', function (pic, buff) {
        console.log(pic);
        console.log(buff);
        //create_picture(data);
    });
});

// Print hello when getting root !
app.get('/', function (req, res) {
    res.send('Hello');
});

//Send html to the client when asking for drawer
app.get('/drawer', function (req, res) {
    res.sendFile(__dirname + "/views/index.html");
});

// Listening to port 3000
app.listen(3000, function () {
    console.log('Listenning to port ' + 3000 + '.');
});