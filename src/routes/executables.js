var express = require('express')
var zip = require('express-zip')
var router = express.Router()
var path = require('path');

const { exec } = require("child_process");
const { spawn } = require('child_process');
const fs = require('fs');


/* Get to render executables page
*/
router.get('/', function (req, res, next) {

	res.render('executables', { title: 'Execute' })
});


const executablesPath = {
	cwd: 'src/executables',
	env: process.env,
}

// output_path = "../../"
const output_path = '../../../public/uploads/bonds'


//! Change areas with ! marker in order to adjust executables input - you will also need to change executables.pug to accept the same inputs
function set_executable_call(req) {

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

	if (!fs.existsSync('./public/uploads/bonds')) {
		fs.mkdirSync('./public/uploads/bonds');
	}




	//! Change executable command line here using above inputs from request
	const executable = spawn('python', ['./DiffBond_v2.py', '-i', "../../public/uploads/" + input1, "../../public/uploads/" + input2, '-m', mode, '-o', output_path], executablesPath);
	return executable;
}

/* POST executable 
 * route to run executable on the server using files that were just uploaded using multer
 * assumes index.pug has fields executableFile1 and executableFile2 for file uploads
*/
router.post('/', async function (req, res, next) {
	console.log('\n--------ENTERING EXECUTABLE WITH FILE UPLOADS--------');
	try {
		const executable = await set_executable_call(req)

		console.log('--------RUNNING FILE UPLOAD EXECUTABLE--------')

		var out_msg = '', err_msg = '';

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
			console.log(out_msg)
			console.log(`child process exited with code ${code}`);
			console.log('--------EXECUTABLE RUN COMPLETE--------\n');
			//copy console data to appropriate files

			fs.writeFile('logs/out.log', out_msg, (err) => {
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
			fs.writeFile('logs/error.log', err_msg, (err) => {
				if (err) { throw err; }
			});

			// // prompt user to download appropraite file
			// var file_names = fs.readdirSync(path.join(__dirname, "../../public/uploads/bonds"));
			// var files = []
			// for (i = 0; i < file_names.length; i++) {
			// 	files.push({ path: path.join(__dirname, "../../public/uploads/bonds"), name: file_names[i] })
			// }
			// console.log(files)
			// res.zip(files)
		});

	} catch (error) {
		console.log("Error: " + error);

	}
	res.redirect("/")
}); //end of POST executables route

module.exports = router