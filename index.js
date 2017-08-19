var express = require('express');
var path = require('path');
var app = express();
var http = require('http').Server(app);
var PythonShell = require('python-shell');
var sleep = require('sleep');

// setup path root
var publicPath = path.resolve(__dirname,'');
app.use(express.static(publicPath));

var tftlcd = require('./libLCD/tftlcd')
var LCD = new tftlcd()

app.use(function (req, res, next) {
    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', '*');
    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);
    // Pass to next layer of middleware
    next();
});

app.get('/command/:command', function(req, res){
	console.log("command: " + req.params.command)
	command = req.params.command
	if(command == "AddText"){
		AddText()
		res.writeHead(200, {'Content-Type': 'application/json'});
    	res.write(JSON.stringify({'Error': 0}));
    	res.end();
	}
	else if(command == "DisplayImage"){
		DisplayImage()
		res.writeHead(200, {'Content-Type': 'application/json'});
    	res.write(JSON.stringify({'Error': 0}));
    	res.end();
	}
	else if(command == "AddTextPosition"){
		AddTextPosition()
		res.writeHead(200, {'Content-Type': 'application/json'});
    	res.write(JSON.stringify({'Error': 0}));
    	res.end();
	}
	else {
		res.writeHead(200, {'Content-Type': 'application/json'});
    	res.write(JSON.stringify({'Error': 1}));
    	res.end();
	}
	
});

function AddText(){
	LCD.begin()
	LCD.clear(255,0,0)
	LCD.text("Hello",150,80,90,"default", 30, 0, 255, 0) // if fontname = "default", fontsize not avaibale
	LCD.text("Good Morning",150,120,90,"Mono.ttf", 30, 0, 0, 255)
	LCD.display()
}

//position: HCENTER, VCENTER, HCENTER&VCENTER
function AddTextPosition(){
	LCD.begin()
	LCD.clear(255,0,0)
	LCD.text("Hello Nice to meet you!","HCENTER&VCENTER", 10, 90, "Mono.ttf", 30, 0, 0, 255)
	LCD.display()
}

function DisplayImage(){
	LCD.displayImage("cat.jpg", 90, 240, 320)
}

http.listen(3000, function(){
  console.log('listening on *:3000');
});