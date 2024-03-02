const fs = require('fs')

exports.front_page = (req, res, next) => {
	// Get names of files from public uploads folder and send to frontend as a div-data object
	var files = fs.readdirSync('public/uploads/');
	res.render('viewer', { title: 'Front Page', data: JSON.stringify(files) });
};

exports.send_public_files = (req, res, next) => {
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