const express   = require('express');
const app       = express();
const server    = require('http').Server(app);
const io        = require('socket.io')(server);
const fs        = require('fs');
const child     = require('child_process');
const jimp      = require('jimp');
const {exec}      = require('child_process');

//Get Image
function writeImage(data)
{
    console.log(data);
    fs.writeFile('client.png', data, function (err) {
        if (err) return console.log(err);
        console.log('Server written in client.png');
    });
}

//Linking root
app.use(express.static(__dirname + '/'));

app.use(express.static('public'));
// Drawer socket where come from picture
var drawer = io.of('/drawer');

// Socket getter from front
drawer.on('connection', function (socket) {
    console.log('socket ' + socket + ' connected.');
    socket.on('picture', function (pic) {
        //console.log(pic);
        console.log(pic.buffer);
	let data = pic.buffer.slice(22);
	fs.writeFile('client.png', data, 'base64', function (err) {
        if (err) return console.log(err);

	    //let dt = resizeImage.resize
        jimp.read("client.png", function (errr, img) {
            if (errr) throw console.log(errr);
            
            //delete old client
            fs.unlink('small-client.png', function (err) {
                if (err) throw console.log(err);
            });
	    
            img.resize(28, 28)
                .quality(100)
		.rgba(false)
		.greyscale()
		.contrast(1)
		.posterize(2)
                .write("small-client.png");

	    exec('python3 ia/tester.py 1', (errrr, stdout, stderr) => {
		//if (errrr) throw console.log(errrr);
		fs.readFile('./result', 'utf8', (lol, datass) => {
		    console.log(datass);
		    socket.emit("result", datass);
		});
	    });
        });
        console.log('Server written in client.png');
	});
        //writeImage(buff);
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
server.listen(3000, function () {
    console.log('Listenning to port ' + 3000 + '.');
});
