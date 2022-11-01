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
	TREE ONLOAD FUNCS
	*/
	// make file tree using PDB and SURF file split
	const tree = document.querySelector('smart-tree');
	makeTree(tree, pdb_files, SURF_files);

	const result = tree.getSelectedValues();
	console.log(result)

	// handles changes in selected values in tree
	treeSelectionEventHandler(tree)

	// take a second to load data associated with a PDB file if someone expands that selection
	expandPDB(tree)


	/*
	VIEWER ONLOAD FUNCS
	*/
	// create a "stage" object attached to viewport
	stage = new NGL.Stage("viewport");



	/*
	FUNCS TO DETECT EVENT CHANGES
	*/
	for (let i = 0; i < pdb_files.length; i++) {
		loadPDB("../uploads/" + pdb_files[i]);
	}

	// loadPDB("rcsb://1BRS")
	// files = ["../uploads/F_chain_only+h+1.SURF"];
	getXML(SURF_files);
};


function loadPDB(pdb_name, index) {
	console.log("Loading PDB file: " + pdb_name);

	// load a PDB structure and consume the returned `Promise`
	stage.loadFile(pdb_name, { name: "mol" }).then(function (component) {
		global_index++;
		// add a "cartoon" representation to the structure component
		component.addRepresentation("cartoon");
		// provide a "good" view of the structure
		component.autoView();
	});
	stage.getComponentsByName("mol").addRepresentation("cartoon", { color: "red" });
}


/*
  *	Formatting XML to be used in xmlhttp requests. 
  * - For now, nothing to format. Leaving it here so that it is available in the future.
  */
function formatXML(file, xmlDoc) {
	// var x = xmlDoc.getElementsByTagName("TAGNAME");
	console.log(file);
}


/*
  *	Asynchronous load using XMLHttpRequest.
  * 
  * - Setup xmlhttp with functions and requests to be called upon send().
  * 	First get list of files[] containing all files to be viewed, and open all.
  *		When a file is "ready", format XML and then load data. TODO: No need to format for now but left here just in case.
  *		Recursive getXML() call to loop through all files. TODO: Recursion isn't great but it works here, so I'll leave it.
  *		Finally, send() requests to server.
  */
async function getXML(files) {
	xmlhttp.open(method, "../uploads/" + files[cnt], true);	// open all files in files[cnt]

	// onreadystatechange - when file loaded, check if file is ready and no errors thrown. If so, call function to formatXML, loadData and getXML() on next file
	console.log("Fetching surf data from " + files[cnt]) + "...";
	xmlhttp.onreadystatechange = function () {
		if (xmlhttp.readyState === XMLHttpRequest.DONE && xmlhttp.status === 200) {
			formatXML(files[cnt], xmlhttp.responseText);
			console.log("Loading data into viewer...");
			loadData(cnt)
			cnt++;
			if (cnt < files.length) getXML(); // call again
		}
	};
	xmlhttp.send();
}
