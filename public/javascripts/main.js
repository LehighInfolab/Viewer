/**
#######################################################
All frontend code for visualization software
#######################################################
*/



//Global variables
/**@global */
var viewer = null; var stage = null;

// Store all file variables. All_components to keep track of components created in viewer.
/**@global */
// var visible_components = [];

/**
#######################################################
Onload Function - When browser starts
#######################################################
*	Onload function - runs when browser has loaded. This will run all functions that start when browser starts
*/
window.onload = async function () {
	// create a "stage" object attached to viewport
	stage = new NGL.Stage("viewport");

	// initialize smart-tree object
	const tree = document.querySelector('smart-tree');

	/*
	GET FILE ONLOAD FUNCS
	*/
	// get files that currently exist in uploads folder
	// TODO: ADD EVENT THAT CHECKS IF A NEW FILE GETS UPLOADED TO UPLOADS FOLDER AND UPDATE
	uploadsFolder = getFiles();
	console.log("Default dir in uploads folder:\n " + uploadsFolder);

	const fileTreeDir = new FileTreeDirectory(uploadsFolder, tree);
	await fileTreeDir.init()
	console.log("File hierarchy", fileTreeDir.fileHierarchy)

	// Load in all pdbs
	await fileTreeDir.callbackAllFiles(loadPDB)
	await fileTreeDir.callbackAllFiles(getSurfXML)
	await fileTreeDir.callbackAllFiles(loadHBond)
	await fileTreeDir.callbackAllFiles(loadGML)

	treeSelectionEventHandler(tree)
	expandPDB(tree);
	// // load files currently in upload folder for hbonds. Set visability to true
	// hbond_files.forEach(element => {
	// 	// readHBond(element)
	// 	loadHBond(element);
	// });
};

