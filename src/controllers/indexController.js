const fs = require('fs');

exports.send_public_files = (req, res) => {
	console.log("Request body")
	try {
		var files = fs.readdirSync('public/uploads/' + req.body.id);
	} catch (error) {
		console.log("Not a directory, reading file instead")
		var files = [req.body.id];
	}
	console.log(files)
	res.send(files)
};