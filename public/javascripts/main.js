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
var files = [], xmlhttp = new XMLHttpRequest(), method = "GET";

// Store all file variables. All_components to keep track of components created in viewer.
var SURF_files = []; var pdb_files = []; var hbond_files = [];
var visible_components = [];

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
	SURF_files, pdb_files, hbond_files = groupFileFormats(files);
	console.log("SURF files: " + SURF_files)
	console.log("PDB files: " + pdb_files)
	console.log("HBOND files: " + hbond_files)

	/*
	FILE TREE ONLOAD FUNCS
	*/
	// make file tree using PDB and SURF file split
	const tree = document.querySelector('smart-tree');
	makeTree(tree, pdb_files, SURF_files, hbond_files);


	/*
	VIEWER ONLOAD FUNCS
	*/
	// create a "stage" object attached to viewport
	stage = new NGL.Stage("viewport");

	// load files currently in upload folder for hbonds. Set visability to true
	hbond_files.forEach(element => {
		// readHBond(element)
		loadHBond(element);
	});

	// load in all files currently in uploads folder. All visibility are set to invisible
	pdb_files.forEach(element => {
		loadPDB(element);
		// loadPDB_stick(element);
	});
	getXML(SURF_files);



	/*
	FUNCS TO DETECT EVENT CHANGES
	*/
	// handles changes in selected values in tree
	treeSelectionEventHandler(tree, pdb_files, SURF_files, hbond_files);

	// take a second to load data associated with a PDB file if someone expands that selection - 
	// this is because there will be a lag when trying to get certain features from PDB, so loading animation already implemented
	expandPDB(tree);
};


function treeSelectionEventHandler(tree, pdb_files, SURF_file, hbond_files) {
	tree.addEventListener('change', function (event) {
		const detail = event.detail,
			item = detail.item,
			oldSelectedIndexes = detail.oldSelectedIndexes,
			selectedIndexes = detail.selectedIndexes;

		// event handling code goes here.
		let [target_file, isSelected, isPDB] = parseSelectionIndex(selectedIndexes, oldSelectedIndexes, pdb_files, SURF_files, hbond_files)

		if (isSelected) {
			console.log(target_file+" is checked");
			console.log("Label: "+ item.label);
			// handle representation tree (sticks and cartoon) for PDB files
			if (isPDB) {
				stage.loadFile("../uploads/" + target_file, {name: target_file}).then(function(component) {
					// add representation if sticks is selected
					if(item.label == "Sticks")
						component.addRepresentation("ball+stick");
					// add representation if cartoon is selected
					if(item.label == "Cartoon")
						component.addRepresentation("cartoon");
					component.setVisibility(true);
				});
				stage.getComponentsByName(target_file).autoView();
			}
			stage.getComponentsByName(target_file).setVisibility(true);
			stage.getComponentsByName(target_file).autoView();
		}
		if (!isSelected) {
			if(isPDB) {
				// stage.getComponentsByName(target_file).setVisibility(true);
				stage.loadFile("../uploads/" + target_file, {name: target_file}).then(component => {
					if(item.label == "Sticks")
						stage.getRepresentationsByName("ball+stick").setVisibility(false);
					if(item.label == "Cartoon")
						stage.getRepresentationsByName("cartoon").setVisibility(false);
					component.setVisibility(true);
				});
				stage.getComponentsByName(target_file).autoView();
			} else {
				stage.getComponentsByName(target_file).setVisibility(false);
			}
		}
	})
}