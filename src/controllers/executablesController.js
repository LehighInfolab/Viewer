// controllers/executablesController.js
exports.user_list = (req, res) => {
	res.send('User list');
};

exports.user_detail = (req, res) => {
	res.send(`User ${req.params.id}`);
};