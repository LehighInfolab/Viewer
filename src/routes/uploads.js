const express = require('express')
const router = express.Router()

/* use multer for file uploads */
const multer = require('multer');

const uploadsPath = {
	cwd: 'public/uploads/uploaded', // we'll perform our operations from within the uploads folder 
	env: process.env,
};

const storage = multer.diskStorage({
	destination: function (req, file, cb) {
		cb(null, 'public/uploads/uploaded')
	},
	filename: function (req, file, cb) {
		cb(null, file.originalname)
	}
})

const upload = multer({
	storage: storage,
	/* ensure that file uploaded is a .SURF file */
	fileFilter(req, file, cb) {
		// if (!file.originalname.match(/\.(SURF|pdb)$/)) { //idk if this syntax is right
		//   return cb(new Error('Input must be a .SURF file'))
		// }
		cb(undefined, true)
	}
})

/* GET upload page */
router.get('/uploads', function (req, res, next) {
	res.render('uploads', { title: 'Upload Page' });
});

/* GET drop page */
router.get('/drop', function (req, res, next) {
	res.render('drop', { title: 'Drop Container' });
});


/* POST files
 *this is the route that uses multer to upload files to the /uploads folder
 *assumes visual.pug has viewerFile as the name tag
*/
var visualUploads = upload.array('viewerFile');
router.post('/drop', visualUploads, function (req, res, next) {
	try {
		console.log('Successful file upload');
		res.redirect('/')
	} catch (error) {
		console.log("File failed to upload.")
		res.redirect('/')
	}
});

/* POST files 
 * this is the route that uses multer to upload files to the /uploads folder
 * assumes index.pug has fiels myFile1 and myFile2 for file uploads
 * DO WE WANT TO KEEP THIS IN THE FINAL VERSION??
*/
var fileUploads = upload.fields([{ name: 'myFile1', maxCount: 1 }, { name: 'myFile2', maxCount: 1 }])
router.post('/files', fileUploads, function (req, res, next) {
	console.log('Files uploaded successfully.');
	res.redirect('/');
}); //end of POST files route



module.exports = router