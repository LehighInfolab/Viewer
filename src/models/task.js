const mongoose = require('mongoose');

const taskSchema = new mongoose.Schema({
	description: String,
	submissionDate: { type: Date, default: Date.now },
	submittedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }
});

module.exports = mongoose.model('Task', taskSchema);
