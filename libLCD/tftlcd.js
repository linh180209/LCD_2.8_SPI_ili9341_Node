var PythonShell = require('python-shell');
function tftlcd(bar) {
	this.pyshell = new PythonShell('./libLCD/lcd.py');
	this.pyshell.on('message', function (message) { 
		// received a message sent from the Python script (a simple "print" statement)  
		console.log("receive: " + message);
	});
}

tftlcd.prototype.begin = function begin() {
	this.pyshell.send("{\"command\":\"begin\"}")
};

tftlcd.prototype.clear = function clear(red, green, blue) {
	this.pyshell.send("{\"command\":\"clear\",\"red\":" + red + ", \"green\":" + green + ", \"blue\":" + blue +"}")
};

// if fontname = default, fontsize not avaiable
tftlcd.prototype.text = function text(message, x, y, rotate, fontname, fontsize, red, green, blue) {
	this.pyshell.send("{\"command\":\"text\",\"text\":\"" + message + "\",\"position\":{\"x\":" + x + ",\"y\":" + y + ",\"rotate\":" + rotate + "},\"font\":{\"name\":\"" +fontname+ "\",\"size\":"+fontsize+",\"red\":" + red + ",\"green\":" +green+ ",\"blue\":"+blue+"}}")
};

//position: HCENTER, VCENTER, HCENTER&VCENTER
tftlcd.prototype.text = function text(message, position , spaceline, rotate, fontname, fontsize, red, green, blue) {
	this.pyshell.send("{\"command\":\"text_position\",\"text\":\"" + message + "\",\"position\":{\"position\":\"" +position+ "\",\"spaceline\":" + spaceline + ",\"rotate\":" + rotate + "},\"font\":{\"name\":\"" +fontname+ "\",\"size\":"+fontsize+",\"red\":" + red + ",\"green\":" +green+ ",\"blue\":"+blue+"}}")
};

tftlcd.prototype.display = function display() {
	this.pyshell.send("{\"command\":\"display\"}")
};

tftlcd.prototype.detroy = function detroy() {
	this.pyshell.send("{\"command\":\"exit\"}")
};

tftlcd.prototype.displayImage = function displayImage(imagename, rotate, width, height) {
	this.pyshell.send("{\"command\":\"displayImage\",\"imagename\":\"" + imagename + "\",\"rotate\":" + rotate + ",\"width\":" + width + ",\"height\":" + height + "}")
};

module.exports = tftlcd;