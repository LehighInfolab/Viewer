const User = require('../models/User');

exports.createUserOrUpdate = async (username) => {
	let user = await User.findOne({ username: username });

	if (!user) {
		user = await User.create({ username: username, uploadedFiles: [], submittedTasks: [] });
	}

	// user._id will be the identifier for the current user
	// You can return this ID or the whole user object as needed
	return user;
}

exports.addFileToUser = async (userId, fileId) => {
	await User.findByIdAndUpdate(userId, { $push: { uploadedFiles: fileId } });
}