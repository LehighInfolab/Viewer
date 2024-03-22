const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
	username: { type: String, unique: true },
	uploadedFiles: [{ type: mongoose.Schema.Types.ObjectId, ref: 'File' }],
	submittedTasks: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Task' }]
});

module.exports = mongoose.model('User', userSchema);