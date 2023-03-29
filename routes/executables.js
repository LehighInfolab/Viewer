var express = require('express')
var router = express.Router()

const { exec } = require("child_process");
const { spawn } = require('child_process');
const fs = require('fs');


const executablesPath = {
	cwd: './executables',
	env: process.env,
}


/* GET TO RUN HARDCODED VASP */
/* runs vasp on the server but uses hardcoded filenames and arguments
 * assumes we have vasp executable in /executables
*  assumes files test1.SURF and test2.SURF are in the /uploads folder
*/
router.get('/', function (req, res, next) {

	res.render('executables', { title: 'Execute' })
});


/* POST executable 
 * route to run executable on the server using files that were just uploaded using multer
 * assumes index.pug has fields executableFile1 and executableFile2 for file uploads
*/
// var secondUploads = upload.fields([{ name: 'executableFile1', maxCount: 1 }])
router.post('/', function (req, res, next) {
	console.log('\nENTERING executable WITH FILE UPLOADS');
	console.log(req.body)

	var input = (req.body.executableFile.endsWith('.PDB')) ? req.body.executableFile : req.body.executableFile + '.PDB';
	var mode = req.body.mode;

	// /* print file names and variables to console for checking */
	console.log('input files: ' + input);
	console.log('Mode: ' + mode);

	console.log('--------RUNNING FILE UPLOAD EXECUTABLE--------')
	var out_msg = '', err_msg = '';

	// move output to outputs folder
	output_path = '../outputs/output.txt';

	/* running executable with recently uploaded files and hardcoded arguments */
	const executable = spawn('python', ['./DiffBond_v2.py', '-i', input, '-m', mode], executablesPath)


	executable.on('error', function (err) {
		console.log(err)
	});

	// const executable = spawn('../executables/DiffBond', ['-csg', file1, file2, op, output_path, resolution], defaults);
	executable.stdout.on('data', (data) => {
		//copy stdout data to out_msg, will later be copied to out.log
		out_msg += data;
	});

	executable.stderr.on('data', (data) => {
		//copy stderr data to err_msg, will later be copied to err.log
		err_msg += data;
	});

	executable.on('close', (code) => {
		console.log(`child process exited with code ${code}`);
		console.log('--------FILE UPLOAD executable RUN COMPLETE--------\n');
		//copy console data to appropriate files
		fs.writeFile('console/out.log', out_msg, (err) => {
			if (err) {
				throw err;
			}
			if (out_msg.includes('...WARN!') || err_msg.includes('...WARN!')) {
				console.log(out_msg);
				console.log(err_msg);
				router.get('/', function (req, res, next) {
					res.render("index", { warning: true });
				});
			}
		});
		fs.writeFile('console/error.log', err_msg, (err) => {
			if (err) { throw err; }
		});

		// // send the output file to the user via download
		// var base = process.env.PWD;
		// console.log('output of pwd test: ');
		// console.log(base);
		// // prompt user to download appropraite file
		// res.download(base + '/outputs/' + output, output);
		// // what should I do here once the program is done running?
		res.redirect('/');
	});
}); //end of POST executables route

module.exports = router