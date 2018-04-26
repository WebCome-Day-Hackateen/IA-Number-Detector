const express   = require('express');
const app       = express();
const server    = require('http').Server(app);
const io        = require('socket.io')(server);
const fs        = require('fs');
const child     = require('child_process');

//Get Image
function writeImage(data)
{
    fs.writeFile('client.png', data, function (err) {
        if (err) return console.log(err);
        console.log('Server written in client.png');
    });
}

//Linking root
app.use(express.static(__dirname + '/'));

// Drawer socket where come from picture
var drawer = io.of('/drawer');

// Socket getter from front
drawer.on('connection', function (socket) {
    console.log('socket ' + socket + ' connected.');
    socket.on('picture', function (pic, buff) {
        console.log(pic);
        console.log(buff);
        writeImage("salut");
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