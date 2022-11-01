/* all of our required variables for basic Node app things */
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

/* need spawn for running command line arguments on the server */
const { spawn } = require('child_process');

/* use multer for file uploads */
const multer = require('multer');

/* multer definitions
 * these define storage and upload functions to be used for multer
 * aren't necessary in app.js since they have been moved to index.js
 * currently commented out to make sure the routes all work without them here
*/
/*
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname)
  }
})

const upload = multer({
  storage: storage,
  // ensure that file uploaded is a .SURF file 
  fileFilter(req, file, cb) {
    if (!file.originalname.match(/\.(SURF)$/)) {
      return cb(new Error('Input must be a .SURF file'))
    }
    cb(undefined, true)
  }
})
*/
//const upload = multer({ dest: path.join(__dirname, 'uploads') });

var indexRouter = require('./routes/index');
var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/tree-scripts', express.static(path.join(__dirname, '/node_modules/smart-webcomponents-community/source/modules/')))
app.use('/tree-styles', express.static(path.join(__dirname, '/node_modules/smart-webcomponents-community/source/styles/')))

/* send the app to the correct router based on the URL */
app.use('/', indexRouter); //all routes are in the index router, found in index.js

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


module.exports = app;
