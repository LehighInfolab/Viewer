/* 
#######################################################
Setup for routes
#######################################################
 */

/* setup for express and child_process module */
const express = require('express');
const router = express.Router();
const fs = require('fs')

const indexController = require('../controllers/indexController')



/* Renders the home page */
router.get('/', function (req, res) {
	var files = fs.readdirSync('public/uploads/');
	res.render('viewer', { title: 'Front Page', data: JSON.stringify(files) });
});

/* Sends public files to front end */
router.post('/files_in_dir', indexController.send_public_files)


// /**
//  * route to test file downloads
//  */
// router.get('/files', function (req, res, next) {
//   console.log('attempting to download hardcoded file from /outputs folder...');
//   var base = process.env.PWD;
//   console.log('output of pwd test: ');
//   console.log(base);
//   // prompt user to download appropraite file
//   res.download(base + '/outputs/download.SURF', 'download.SURF')
// })


module.exports = router; 