/** 
* Utils for PDB file loading
* @param {string} dir - name to set object in NGL
* @param {string} pdb_file - file name in uploads folder
*/
function loadPDB(dir, pdb_file) {
	if (pdb_file.split(".").pop() != "pdb") {
		return;
	}
	console.log("Loading PDB file: ", pdb_file);
	// load a PDB structure and consume the returned `Promise`
	stage.loadFile("../uploads/" + dir + "/" + pdb_file, { name: pdb_file }).then(function (component) {
		// add a "cartoon" representation to the structure component
		component.addRepresentation("cartoon");
		component.setVisibility(false)
		// provide a "good" view of the structure
		// component.autoView();
	});
	return;
}