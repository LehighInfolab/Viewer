const express = require('express');
const router = express.Router();

// // Example route for creating a new user
// router.post('/files', async (req, res) => {
// 	const { username } = req.body;
// 	try {
// 		const newUser = await User.create({ username });
// 		res.json(newUser);
// 	} catch (error) {
// 		res.status(500).json({ error: error.message });
// 	}
// });

module.exports = router; 