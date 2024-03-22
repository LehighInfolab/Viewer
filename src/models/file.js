const mongoose = require('mongoose');

const fileSchema = new mongoose.Schema({
	filename: String,
	uploadDate: { type: Date, default: Date.now },
	uploader: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }
});

module.exports = mongoose.model('File', fileSchema);
