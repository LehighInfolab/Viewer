/* 
#######################################################
Utils for PDB file loading
#######################################################
 */

function loadPDB(pdb_name) {
	console.log("Loading PDB file: " + pdb_name);

	// load a PDB structure and consume the returned `Promise`
	stage.loadFile("../uploads/" + pdb_name, { name: pdb_name }).then(function (component) {
		// add a "cartoon" representation to the structure component
		component.addRepresentation("cartoon");
		component.setVisibility(false)
		// provide a "good" view of the structure
		// component.autoView();
	});
	// stage.getComponentsByName(pdb_name).addRepresentation("cartoon", { color: "blue" });
	// visible_components.push(pdb_name)
}