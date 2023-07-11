/* 
#######################################################
Setup for routes
#######################################################
 */

/* setup for express and child_process module */
var express = require('express');
var app = require("../app.js")
var router = express.Router();
const fs = require('fs');

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


/* GET home page. */
/* renders the home page */
router.get('/', function (req, res, next) {
  /* Get names of files from public uploads folder and send to frontend as a div-data object */
  var files = fs.readdirSync('public/uploads/');
  res.render('viewer', { title: 'Front Page', data: JSON.stringify(files) });
});

router.post('/files_in_dir', function (req, res, next) {
  console.log("Request body")
  try {
    var files = fs.readdirSync('public/uploads/' + req.body.id);
  } catch (error) {
    console.log("Not a directory, reading file instead")
    var files = [req.body.id];
  }
  console.log(files)
  res.send(files)
})

/* GET test page */
/* renders test page, just to check if routes work */
router.get('/test', function (req, res, next) {
  res.render('test', { title: 'Test Page' });
});

/* GET upload page */
router.get('/upload', function (req, res, next) {
  res.render('upload', { title: 'Upload Page' });
});

/* GET drop page */
router.get('/drop', function (req, res, next) {
  res.render('drop', { title: 'Drop Container' });
});

// router.post('/visual', (req, res) => {
//   var files = fs.readdirSync('uploads/');
//   res.render('index', { title: 'Front Page', data: JSON.stringify(files) });
// })

/* GET documentation page*/
router.get('documentation', function (req, res, next) {
  res.render('documentation', { title: 'Documentation' });
});

/**
 * route to test file downloads
 */
router.get('/files', function (req, res, next) {
  console.log('attempting to download hardcoded file from /outputs folder...');
  var base = process.env.PWD;
  console.log('output of pwd test: ');
  console.log(base);
  // prompt user to download appropraite file
  res.download(base + '/outputs/download.SURF', 'download.SURF')
})


/* POST files
 *this is the route that uses multer to upload files to the /uploads folder
 *assumes visual.pug has viewerFile as the name tag
*/
var visualUploads = upload.array('viewerFile');
router.post('/drop', visualUploads, function (req, res, next) {
  console.log('Successful file upload');
  res.redirect('/drop')
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




module.exports = router; 