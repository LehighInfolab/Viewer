/* 
#######################################################
Setup for routes
#######################################################
 */

/* setup for express and child_process module */
const express = require('express');
const router = express.Router();
const { exec } = require("child_process");
const { spawn } = require('child_process');
const fs = require('fs');
const executables_path = {
  cwd: './executables',
  env: process.env,
}
// TODO: change to index.js from backend

/* setup for multer */
/* use multer for file uploads */
const multer = require('multer');

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'public/uploads/')
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

const defaults = {
  cwd: './public/uploads', // we'll perform our operations from within the uploads folder 
  env: process.env,
};


/* GET home page. */
/* renders the home page */
router.get('/', function (req, res, next) {
  /* Get names of files from public uploads folder and send to frontend as a div-data object */
  var files = fs.readdirSync('public/uploads/');
  res.render('viewer', { title: 'Front Page', data: JSON.stringify(files) });
});

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


/**
 * route to test file downlaods
 */
router.get('/files', function (req, res, next) {
  console.log('attempting to download hardcoded file from /outputs folder...');
  var base = process.env.PWD;
  console.log('output of pwd test: ');
  console.log(base);
  // prompt user to download appropraite file
  res.download(base + '/outputs/download.SURF', 'download.SURF')
})

/* GET TO RUN HARDCODED VASP */
/* runs vasp on the server but uses hardcoded filenames and arguments
 * assumes we have vasp executable in /executables
*  assumes files test1.SURF and test2.SURF are in the /uploads folder
*/
router.get('/vasp', function (req, res, next) {
  // var input1 = (req.body.executableFile1.endsWith('.SURF')) ? req.body.executableFile1 : req.body.executableFile1 + '.SURF';
	// var input2 = (req.body.executableFile2.endsWith('.SURF')) ? req.body.executableFile2 : req.body.executableFile2 + '.SURF';
	// var mode = req.body.mode;

  // // print file names and variables to console for checking
	// console.log('input files: ', input1, input2);
	// console.log('Mode: ' + mode);
  
  /* print a message to the console so we know this route has been entered */
  console.log('\n--------RUNNING VASP WITH HARDCODED COMMANDS--------'); //message printed to the console

  const child = spawn('../executables/vasp', ['-csg', '../public/uploads/test1.SURF', '../public/uploads/test2.SURF', 'I', '../public/uploads/output.SURF', '0.5'], executables_path);
  var out_msg = '', err_msg = '';
  child.stdout.on('data', (data) => {
    //copy stdout data to out_msg, will later be copied to out.log
    out_msg += data;
  });

  child.stderr.on('data', (data) => {
    //copy stderr data to err_msg, will later be copied to err.log
    err_msg += data;
  });

  child.on('close', (code) => {
    console.log(`\n VASP child process exited with code ${code}`);
    console.log('--------HARDCODED VASP RUN COMPLETE--------\n');
    //copy data to logs
    //TODO: add logs folder
    // fs.writeFile('console/out.log', out_msg, (err) => {
    //   if (err) { throw err; }
    // });
    // fs.writeFile('console/error.log', err_msg, (err) => {
    //   if (err) { throw err; }
    // });
    console.log(out_msg);
    console.log(err_msg);
    // return to visualization page
    res.redirect('/');
  });
});



/* POST vasp 
 * route to run vasp on the server using files that were just uploaded using multer
 * assumes index.pug has fields vaspFile1 and vaspFile2 for file uploads
*/
var secondUploads = upload.fields([{ name: 'vaspFile1', maxCount: 1 }, { name: 'vaspFile2', maxCount: 1 }])
router.post('/vasp', secondUploads, function (req, res, next) {
  console.log('\nENTERING VASP WITH FILE UPLOADS');
  var fileKeys = Object.keys(req.files);
  var fileNames = [];
  // adding filenames to array 
  let index = 0;
  fileKeys.forEach(function (file) {  //this would probably be better using map, but it works
    fileNames[index] = req.files[file][0].filename;
    index++;
  });

  // get other arguments 
  var output = (req.body.output.endsWith('.SURF')) ? req.body.output : req.body.output + '.SURF';
  //check to make sure output file name is correct file type
  var op = req.body.operation;
  var resolution = req.body.resolution;
  var file1 = fileNames[0];
  var file2 = fileNames[1];

  /* print file names and variables to console for checking */
  console.log('input files: ' + fileNames);
  console.log('output file: ' + output);
  console.log('operation: ' + op);
  console.log('resolution: ' + resolution);
  console.log('entire req.body:');
  console.log(req.body);

  console.log('--------RUNNING FILE UPLOAD VASP--------')
  var out_msg = '', err_msg = '';
  // move output to outputs folder
  output_path = '../outputs/' + output;
  /* running vasp with recently uploaded files and hardcoded arguments */
  const vasp = spawn('../executables/vasp', ['-csg', file1, file2, op, output_path, resolution], defaults);
  vasp.stdout.on('data', (data) => {
    //copy stdout data to out_msg, will later be copied to out.log
    out_msg += data;
  });

  vasp.stderr.on('data', (data) => {
    //copy stderr data to err_msg, will later be copied to err.log
    err_msg += data;
  });

  vasp.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    console.log('--------FILE UPLOAD VASP RUN COMPLETE--------\n');
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

    // send the output file to the user via download
    var base = process.env.PWD;
    console.log('output of pwd test: ');
    console.log(base);
    // prompt user to download appropraite file
    res.download(base + '/outputs/' + output, output);
    // what should I do here once the program is done running?
    // res.redirect('/test');
  });

}); //end of POST vasp route

/**
 * GET route to run hbond-finder executable
 */
router.get('/hbfinder', function(req, res, next){
  console.log('\n--------RUNNING HBOND FINDER WITH HARDCODED COMMANDS--------');
  // spawn parameters: <command to run python code>, [<python script path>, (optional) <any parameters required for python program>]
  const child = spawn('python3', ['./hbondfinder.py','-j', 'acceptors_donors_dict.json',
          '-b', '../public/uploads/'], executables_path);
  // if child has an error
  child.on('error', (err) => {
    console.log("\n\tERROR: [" + err + "]"); // print error message to console
  });
  // if child closes
  child.on('close', (data) => {
    console.log("\n\t HBFinder child closed: "+ data); // print data to console
    const fs = require("fs");
    var files = fs.readdirSync(executables_path.cwd);

    // move all .txt files to uploads
    for (var i = files.length - 1; i >= 0; i--) {
      var file = files[i];
      if (file.split('.')[1] === 'txt') {
        if (file.split('.')[0].charAt(0) == 'h') {
          fs.rename('executables/' + file, 'public/uploads/' + file, function(err) {
            if (err) throw err;
            console.log('Move to uploads complete.');
          });
        }
        if (file.split('.')[0].charAt(0) == 'H') {
          fs.rename('executables/' + file, 'logs/' + file, function(err) {
            if (err) throw err;
            console.log('Move to logs complete.');
          });
        }
      }
    }
    res.redirect('/');
  });
}); // end of GET hbond-finder route

module.exports = router; 