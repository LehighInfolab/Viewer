const express = require('express')
const zip = require('express-zip')
const router = express.Router()
const path = require('path');

const { exec } = require("child_process");
const { spawn } = require('child_process');
var fs = require('fs');

const executablesController = require('../controllers/executablesController')

/* Get to render executables page
*/
router.get('/', function (req, res, next) {
	res.render('executables', { title: 'Execute' })
});


const executables_path = {
	cwd: 'src/executables',
	env: process.env,
}

const output_path = '../../../public/uploads/bonds'
const file_path = "../../public/uploads/"

exports.set_executable_call = function (req) {
	//! Reading inputs from frontend request - change these inputs according to your executable command line inputs
	var input1 = (req.body.executableFile1.endsWith('.pdb')) ? req.body.executableFile1 : req.body.executableFile1 + '.PDB';
	var input2 = (req.body.executableFile2.endsWith('.pdb')) ? req.body.executableFile2 : req.body.executableFile2 + '.PDB';
	var mode = req.body.mode;

	// print file names and variables to console for checking
	console.log('input files: ', input1, input2);
	console.log('Mode: ' + mode);


	//! Move output to outputs folder - this will always set uploads folder to be output_path. You may add additional output file name here or in executable command
	var output = req.body.output;
	if (output == "") {
		output = input1 + "_" + input2
	}

	// if (!fs.existsSync('./public/uploads/bonds')) {
	// 	fs.mkdirSync('./public/uploads/bonds');
	// }

	//! Change executable command line here using above inputs from request
	console.log("Running executable...")
	const executable = spawn('python', ['./DiffBond_v2.py', '-i', file_path + input1, file_path + input2, '-m', mode, '-o', output_path], executables_path);
	return executable;
}

router.post('/', executablesController.run_executable)

module.exports = router