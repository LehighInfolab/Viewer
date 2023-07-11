/* all of our required variables for basic Node app things */
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var router = express.Router()

/* send the app to the correct router based on the URL */
var indexRouter = require('./routes/index');

// /* need spawn for running command line arguments on the server */
// const { spawn } = require('child_process');

// /* use multer for file uploads */
// const multer = require('multer');

require('dotenv').config()


var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '../public')));
app.use('/tree-scripts', express.static(path.join(__dirname, 'lib/smart-webcomponents-community/source/modules/')))
app.use('/tree-styles', express.static(path.join(__dirname, 'lib/smart-webcomponents-community/source/styles/')))

app.use('/', indexRouter); //all routes are in the index router, found in index.js

// const uploadsRouter = require('./routes/uploads')
// app.use('/uploads', uploadsRouter)

// const executablesRouter = require('./routes/executables')
// app.use('/executables', executablesRouter)


/* catch 404 and forward to error handler */
app.use(function (req, res, next) {
  next(createError(404));
});

/* error handler */
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});


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
