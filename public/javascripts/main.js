/* 
#######################################################
All frontend code for visualization software
#######################################################
 */



/* 
#######################################################
GLOBAL VARIABLES
#######################################################
 */
// Global variables to initialize viewer
var viewer = null;
var stage = null;

// Global variables for setting up XML asynchronous file loading
var files = [], cnt = 0, xmlhttp = new XMLHttpRequest(), method = "GET";
var SURF_files = []; var pdb_files = [];

// Global variable to hold color value for objects in RGB. This is global so that each objects colors can be adjusted based on previous object color.
var color_val = 256 / 7; var color = [];

var structure_instances = []
var pdb_temp;

var global_index = 0;


/* 
#######################################################
Onload Function - When browser starts
#######################################################
 */
/*
 *	Onload function - runs when browser has loaded. This will run all functions that start when browser starts
 *	
 *	- Function initializes viewer viewport and starts loading objects to viewer from getXML()
 */
window.onload = function () {
	/*
	GET FILE ONLOAD FUNCS
	*/
	// get files that currently exist in uploads folder
	// TODO: ADD EVENT THAT CHECKS IF A NEW FILE GETS UPLOADED TO UPLOADS FOLDER AND UPDATE
	files = getFiles();
	console.log("Default files in uploads folder:\n " + files);

	// split all files in uploads folder into PDB or SURF files
	SURF_files, pdb_files = groupFileFormats(files);
	console.log("SURF files: " + SURF_files)
	console.log("PDB files: " + pdb_files)


	/*
	FILE TREE ONLOAD FUNCS
	*/
	// make file tree using PDB and SURF file split
	const tree = document.querySelector('smart-tree');
	makeTree(tree, pdb_files, SURF_files);

	// const result = tree.getSelectedValues();
	// console.log(result)


	/*
	VIEWER ONLOAD FUNCS
	*/
	// create a "stage" object attached to viewport
	stage = new NGL.Stage("viewport");



	/*
	FUNCS TO DETECT EVENT CHANGES
	*/
	// handles changes in selected values in tree
	treeSelectionEventHandler(tree, pdb_files, SURF_files);

	// take a second to load data associated with a PDB file if someone expands that selection - 
	// this is because there will be a lag when trying to get certain features from PDB, so loading animation already implemented
	expandPDB(tree);

	// for (let i = 0; i < pdb_files.length; i++) {
	// 	loadPDB("../uploads/" + pdb_files[i]);
	// }

	// loadPDB("rcsb://1BRS")
	// files = ["../uploads/F_chain_only+h+1.SURF"];
	// getXML(SURF_files);
};


function treeSelectionEventHandler(tree, pdb_files, SURF_files) {
	tree.addEventListener('change', function (event) {
		const detail = event.detail,
			item = detail.item,
			oldSelectedIndexes = detail.oldSelectedIndexes,
			selectedIndexes = detail.selectedIndexes;

		// event handling code goes here.
		let [target_file, isSelected, isPDB] = parseSelectionIndex(selectedIndexes, oldSelectedIndexes, pdb_files, SURF_files)

		if (isSelected) {
			if (isPDB) {
				loadPDB("../uploads/" + target_file, 10)
			} else { // is SURF file
				getSURFXML(target_file)
			}
		}

	})
}