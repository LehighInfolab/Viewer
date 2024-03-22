/* 
all of our required variables for basic Node app things 
*/

const express = require('express'); // for the Express framework functions.
const path = require('path'); // for handling and transforming file paths.
const createError = require('http-errors'); // for generating HTTP errors.
const cookieParser = require('cookie-parser'); // for parsing cookie header and populating req.cookies.
const logger = require('morgan'); // for logging request details.

const router = express.Router()
const app = express();

// // need spawn for running command line arguments on the server
// const { spawn } = require('child_process');

// use multer for file uploads 
const mongoose = require('mongoose');
const multer = require('multer');

// Use environment config file
require('dotenv').config()



// view engine setup - views stored in the views directory
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');



// Use various middleware for request logging, parsing JSON and URL-encoded bodies, parsing cookies, and serving static files.
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '../public')));
app.use('/tree-scripts', express.static(path.join(__dirname, 'lib/smart-webcomponents-community/source/modules/')))
app.use('/tree-styles', express.static(path.join(__dirname, 'lib/smart-webcomponents-community/source/styles/')))



/* set up mongodb to connect to database 
Mongodb has not been set up yet. Commented out for now until we need to use it.
*/
const uri = process.env.MONGODB_URL
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })

const db = mongoose.connection
db.on('error', (error) => console.error(error))
db.once('open', () => console.log('Connected to database'))



// send the app to the correct router based on the URL
const indexRouter = require('./routes/index');
const uploadsRouter = require('./routes/uploads')
const viewerRouter = require('./routes/viewer')

// ##### MAKE CHANGES HERE TO ADD EXECUTABLES #####
// set up executables routers
const executablesRouter = require('./routes/executables')
const exeNullRouter = require('./routes/exe-nullification')

// Use route modules
app.use('/', indexRouter);
app.use('/uploads', uploadsRouter);
app.use('/viewer', viewerRouter);

// executable routes
app.use('/executables', executablesRouter);
app.use('/exe-nullification', exeNullRouter);



// load models
const User = require('./models/User');
const File = require('./models/file');
const Task = require('./models/Task');

const userRoutes = require('./routes/userRoutes')
const fileRoutes = require('./routes/fileRoutes')
const taskRoutes = require('./routes/taskRoutes')


// Use the routes
app.use('/users', userRoutes);
app.use('/files', fileRoutes);
app.use('/tasks', taskRoutes);



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




module.exports = app;