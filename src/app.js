/* all of our required variables for basic Node app things */

var createError = require('http-errors'); // for generating HTTP errors.
var express = require('express'); // for the Express framework functions.
var path = require('path'); // for handling and transforming file paths.
var cookieParser = require('cookie-parser'); // for parsing cookie header and populating req.cookies.
var logger = require('morgan'); // for logging request details.
var router = express.Router()
var app = express();

// // need spawn for running command line arguments on the server
// const { spawn } = require('child_process');

// // use multer for file uploads 
// const multer = require('multer');



// send the app to the correct router based on the URL
var indexRouter = require('./routes/index');



// Use environment config file
require('dotenv').config()



// view engine setup - views stored in the views directory
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');



// Use various middleware for request logging, parsing JSON and URL-encoded bodies, parsing cookies, and serving static files.
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '../public')));
app.use('/tree-scripts', express.static(path.join(__dirname, 'lib/smart-webcomponents-community/source/modules/')))
app.use('/tree-styles', express.static(path.join(__dirname, 'lib/smart-webcomponents-community/source/styles/')))


app.use('/', indexRouter); //all routes are in the index router, found in index.js


// Middleware - catch 404 and forward to error handler
app.use(function (req, res, next) {
	next(createError(404));
});

// Middleware error handler
app.use(function (err, req, res, next) {
	// set locals, only providing error in development
	res.locals.message = err.message;
	res.locals.error = req.app.get('env') === 'development' ? err : {};

	// render the error page
	res.status(err.status || 500);
	res.render('error');
});





// const uploadsRouter = require('./routes/uploads')
// app.use('/uploads', uploadsRouter)

const executablesRouter = require('./routes/executables')
app.use('/executables', executablesRouter)


/* set up mongodb to connect to database 
Mongodb has not been set up yet. Commented out for now until we need to use it.
*/
// const mongoose = require('mongoose');
// const uri = process.env.MONGODB_URI

// mongoose.connect(uri, { useNewUrlParser: true })
// const db = mongoose.connection
// db.on('error', (error) => console.error(error))
// db.once('open', () => console.log('Connected to database'))


module.exports = app;
