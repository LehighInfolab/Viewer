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