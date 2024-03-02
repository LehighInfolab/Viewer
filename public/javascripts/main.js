/**
#######################################################
All frontend code for visualization software
#######################################################
*/



/** 
#######################################################
GLOBAL VARIABLES
#######################################################
*/
// Global variables to initialize viewer
/** @global */
var viewer = null;
/**@global */
var stage = null;



// Store all file variables. All_components to keep track of components created in viewer.
// var SURF_files = []; var pdb_files = []; var hbond_files = [];
/**@global */
var visible_components = [];

// Global variable to hold color value for objects in RGB. This is global so that each objects colors can be adjusted based on previous object color.
/**@global */
var color_val = 256 / 7; var color = [];

var structure_instances = []
var pdb_temp;

var global_index = 0;



/**
#######################################################
Onload Function - When browser starts
#######################################################
*	Onload function - runs when browser has loaded. This will run all functions that start when browser starts
*	
*	Function initializes viewer viewport and starts loading objects to viewer from getXML()
*/


window.onload = async function () {
	// create a "stage" object attached to viewport
	stage = new NGL.Stage("viewport");

	// get file tree
	const tree = document.querySelector('smart-tree');


	/*
	GET FILE ONLOAD FUNCS
	*/
	// get files that currently exist in uploads folder
	// TODO: ADD EVENT THAT CHECKS IF A NEW FILE GETS UPLOADED TO UPLOADS FOLDER AND UPDATE
	uploads = getFiles();
	console.log("Default dir in uploads folder:\n " + uploads);
	// const dir = new file_tree_dir(uploads[0])
	// console.log("Dir", dir)

	console.log(uploads)
	var dir_list = [];
	for (let i = 0; i < uploads.length - 0; i++) {
		var dir = new file_tree_dir(uploads[i]);
		console.log("Current working dir:", dir);
		const d1 = await set_up_tree(dir);
		// const d2 = await load_files(dir);
		// load in all files currently in uploads folder. All visibility are set to invisible
		for (let i = 0; i < dir.pdb_files.length; i++) {
			await loadPDB(dir.id, dir.pdb_files[i])
		}
		let cnt = 0;
		await getXML(dir.id, dir.SURF_files, cnt);
		// console.log(d1)
		dir_list.push(dir)
	}

	// // load files currently in upload folder for hbonds. Set visability to true
	// hbond_files.forEach(element => {
	// 	// readHBond(element)
	// 	loadHBond(element);
	// });



	/*
	FUNCS TO DETECT EVENT CHANGES
	*/
	// handles changes in selected values in tree
	treeSelectionEventHandler(tree, dir_list);

	// // take a second to load data associated with a PDB file if someone expands that selection - 
	// // this is because there will be a lag when trying to get certain features from PDB, so loading animation already implemented
	// expandPDB(tree);
};

/**
 * Sets up the file tree
 * @param {string} dir - Directory where files are located
 */
async function set_up_tree(dir) {
	let files = await dir.files
	// var files = await set_up_dir(dir)
	dir.groupFileFormats(files)
	// var SURF_files = dir.SURF_files
	// var pdb_files = dir.pdb_files

	// console.log(SURF_files, pdb_files)

	// get file tree
	const tree = document.querySelector('smart-tree');

	console.log(dir.SURF_files)
	console.log(dir.pdb_files)
	console.log(dir.hbond_files)
	console.log(dir.other)

	//Creates a group in the tree for the current item
	console.log("Setting up current tree group with ID:", dir.id)
	startTree(tree, dir.id)
	makeTree(tree, dir.id, dir.SURF_files);
	makeTree(tree, dir.id, dir.pdb_files);
	makeTree(tree, dir.id, dir.hbond_files);
	makeTree(tree, dir.id, dir.other);
	return;
}


// async function load_files(dir) {

// 	// load in all files currently in uploads folder. All visibility are set to invisible
// 	for (let i = 0; i < dir.pdb_files.length; i++) {
// 		await loadPDB(dir.id, dir.pdb_files[i])
// 	}
// 	let cnt = 0;
// 	await getXML(dir.id, dir.SURF_files, cnt);
// }

/**
 * treeSelectionEventHandler() handles visibility of objects when the associated index of the file tree is checked or unchecked using an eventListener().
 * 
 * @param {smart-tree} tree 
 * @param {string[]} dir_list 
 * @returns {None}
 */
function treeSelectionEventHandler(tree, dir_list) {
	tree.addEventListener('change', function (event) {
		var detail = event.detail,
			item = detail.item,
			oldSelectedIndexes = detail.oldSelectedIndexes,
			selectedIndexes = detail.selectedIndexes;

		console.log("hello")
		console.log(detail)
		console.log(item.label)

		let selected_diff = selectedIndexes.filter(x => !oldSelectedIndexes.includes(x));
		let unselected_diff = oldSelectedIndexes.filter(x => !selectedIndexes.includes(x));

		index = []
		isSelected = true;
		if (selected_diff != "") {
			index = selected_diff[0].split(".")
			isSelected = true
		} else {
			index = unselected_diff[0].split(".")
			isSelected = false
		}
		if (index.length == 1) {
			return;
		}

		if (isSelected) {
			stage.getComponentsByName(item.label).setVisibility(true);
			stage.getComponentsByName(item.label).autoView();
			console.log("Showing", item.label)
		}
		if (!isSelected) {
			stage.getComponentsByName(item.label).setVisibility(false);
			console.log("Hiding", item.label)
		}
	})
	return;
}