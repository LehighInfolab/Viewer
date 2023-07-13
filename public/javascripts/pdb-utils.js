/** 
#######################################################
Utils for PDB file loading
#######################################################
* @param {string} id - name to set object in NGL
* @param {string} pdb_file - file name in uploads folder
*/

function loadPDB(id, pdb_file) {
	console.log("From dir :", id, "--- Loading PDB file: ", pdb_file);
	// load a PDB structure and consume the returned `Promise`
	stage.loadFile("../uploads/" + id + "/" + pdb_file, { name: pdb_file }).then(function (component) {
		// add a "cartoon" representation to the structure component
		component.addRepresentation("cartoon");
		component.setVisibility(false)
		// provide a "good" view of the structure
		// component.autoView();
	});
	// stage.getComponentsByName(pdb_file).addRepresentation("cartoon", { color: "blue" });
	// visible_components.push(pdb_file)
	return;
}