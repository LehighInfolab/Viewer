// var express = require('express')
// var router = express.Router()

// /* setup for multer */
// /* use multer for file uploads */
// const multer = require('multer');



// const storage = multer.diskStorage({
// 	destination: function (req, file, cb) {
// 		cb(null, 'public/uploads/')
// 	},
// 	filename: function (req, file, cb) {
// 		cb(null, file.originalname)
// 	}
// })

// const upload = multer({
// 	storage: storage,
// 	/* ensure that file uploaded is a .SURF file */
// 	fileFilter(req, file, cb) {
// 		// if (!file.originalname.match(/\.(SURF|pdb)$/)) { //idk if this syntax is right
// 		//   return cb(new Error('Input must be a .SURF file'))
// 		// }
// 		cb(undefined, true)
// 	}
// })






module.exports = router