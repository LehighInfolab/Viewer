const express = require('express');
const router = express.Router();
const { createUserOrUpdate } = require("../controllers/userController");

// Example route for creating a new user
router.post('/', async (req, res) => {
	const { username } = req.body;
	console.log(username)
	try {
		const newUser = await createUserOrUpdate(username);
		res.json(newUser);
	} catch (error) {
		res.status(500).json({ error: error.message });
	}
});

module.exports = router; 