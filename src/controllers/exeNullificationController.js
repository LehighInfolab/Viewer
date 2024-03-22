const exeNull = require('../routes/exe-nullification')
const fs = require('fs');
const { spawn } = require('child_process');
const { task_queue_concurrency_limit } = require('../config')

class TaskQueue {
	constructor(concurrency) {
		this.concurrency = concurrency;
		this.running = 0;
		this.queue = [];
	}

	// Function to add tasks to the queue
	enqueueTask(task) {
		this.queue.push(task);
		this.runNext();
	}

	// Function to run the next task if we haven't reached concurrency limit
	runNext() {
		if (this.running < this.concurrency && this.queue.length) {
			const task = this.queue.shift();
			this.running++;
			task().then(() => {
				this.running--;
				this.runNext();
			});
		}
	}
}

const executableQueue = new TaskQueue(task_queue_concurrency_limit);

exports.send_queue_length = (req, res) => {
	const length = executableQueue.queue.length;
	res.json({ length });
}

/* POST executable 
 * route to run executable on the server using files that were just uploaded using multer
 * assumes index.pug has fields executableFile1 and executableFile2 for file uploads
*/
exports.run_executable = function (req, res, next) {
	const process_task = () => new Promise(async (resolve, reject) => {
		try {
			const executable = await exeNull.process_files(req)
		} catch (error) {
			console.log("Error: " + error);
		}
	});
	executableQueue.enqueueTask(process_task);

	// const task = () => new Promise(async (resolve, reject) => {
	// 	console.log('\n--------ENTERING EXECUTABLE WITH FILE UPLOADS--------');
	// 	try {
	// 		const executable = await exeNull.set_executable_call(req)

	// 		console.log('--------RUNNING FILE UPLOAD EXECUTABLE--------')

	// 		var out_msg = '', err_msg = '';

	// 		executable.on('error', function (err) {
	// 			console.log(err)
	// 		});

	// 		// const executable = spawn('../executables/DiffBond', ['-csg', file1, file2, op, output_path, resolution], defaults);
	// 		executable.stdout.on('data', (data) => {
	// 			//copy stdout data to out_msg, will later be copied to out.log
	// 			out_msg += data;
	// 		});

	// 		executable.stderr.on('data', (data) => {
	// 			//copy stderr data to err_msg, will later be copied to err.log
	// 			err_msg += data;
	// 		});

	// 		executable.on('close', (code) => {
	// 			console.log(out_msg)
	// 			console.log(`child process exited with code ${code}`);
	// 			console.log('--------EXECUTABLE RUN COMPLETE--------\n');
	// 			//copy console data to appropriate files

	// 			fs.writeFile('logs/out.log', out_msg, (err) => {
	// 				if (err) {
	// 					throw err;
	// 				}
	// 				if (out_msg.includes('...WARN!') || err_msg.includes('...WARN!')) {
	// 					console.log(out_msg);
	// 					console.log(err_msg);
	// 					router.get('/', function (req, res, next) {
	// 						res.render("index", { warning: true });
	// 					});
	// 				}
	// 			});
	// 			fs.writeFile('logs/error.log', err_msg, (err) => {
	// 				if (err) { throw err; }
	// 			});

	// 			// // prompt user to download appropraite file
	// 			// var file_names = fs.readdirSync(path.join(__dirname, "../../public/uploads/bonds"));
	// 			// var files = []
	// 			// for (i = 0; i < file_names.length; i++) {
	// 			// 	files.push({ path: path.join(__dirname, "../../public/uploads/bonds"), name: file_names[i] })
	// 			// }
	// 			// console.log(files)
	// 			// res.zip(files)

	// 		});

	// 	} catch (error) {
	// 		console.log("Error: " + error);
	// 	}
	// 	// res.redirect("/")

	// }); //end of POST executables route
	// executableQueue.enqueueTask(task);
	// res.send(`
	// <html>
	//     <head>
	//         <title>Success</title>
	//         <meta http-equiv="refresh" content="5;url=/" />
	//         <script type="text/javascript">
	//             // Redirect after 3 seconds
	//             setTimeout(function() {
	//                 window.location.href = '/';
	//             }, 3000);
	//         </script>
	//         <style>
	//             body {
	//                 background-color: black;
	//                 color: white;
	//                 font-family: Arial, sans-serif;
	//             }
	//         </style>
	//     </head>
	//     <body>
	//         <p>Your task was successfully sent. Redirecting to the main page in 3 seconds...</p>
	//     </body>
	// </html>
	// `);
};