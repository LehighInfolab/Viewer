/* 
#######################################################
Utils for tree setup
#######################################################
 */

// TODO: NEED TO ADD DATA CHANGES AFTER EXPANSION
// function allows webserver to load for a second to retrieve data associated to a PDB (eg. maybe split into chains, cartoon view, stick view, etc.)
function expandPDB(tree) {
	tree.addEventListener("expand", function (event) {
		if (event.detail.children.length > 0) {
			return;
		}
		tree.select(event.detail.item)

		tree.displayLoadingIndicator = true;

		setTimeout(function () {
			const newItem1 = document.createElement('smart-tree-item'),
				newItem2 = document.createElement('smart-tree-item');

			newItem1.label = 'Cartoon';
			newItem2.label = 'Sticks';

			tree.addTo(newItem1, event.detail.item);
			tree.addTo(newItem2, event.detail.item);

			tree.displayLoadingIndicator = false;
		}, 1000);
	});
}

function makeTree(tree, pdb_files, SURF_files, hbond_files) {
	// let tree = document.querySelector('smart-tree');
	for (let i = 0; i < pdb_files.length; i++) {
		newItem = document.createElement('smart-tree-items-group');
		newItem.label = pdb_files[i];
		tree.addTo(newItem, 'PDB');
	}
	for (let i = 0; i < SURF_files.length; i++) {
		newItem = document.createElement('smart-tree-items');
		newItem.label = SURF_files[i];
		tree.addTo(newItem, 'SURF');
	}
	for (let i = 0; i < hbond_files.length; i++) {
		newItem = document.createElement('smart-tree-items');
		newItem.label = SURF_files[i];
		tree.addTo(newItem, 'HBOND');
	}
}


function parseSelectionIndex(selectedIndexes, oldSelectedIndexes, pdb_files, SURF_files, hbond_files) {
	let selected_diff = selectedIndexes.filter(x => !oldSelectedIndexes.includes(x));
	let unselected_diff = oldSelectedIndexes.filter(x => !selectedIndexes.includes(x));

	index = []
	isSelected = true
	if (selected_diff != "") {
		index = selected_diff[0].split(".")
		isSelected = true
	} else {
		index = unselected_diff[0].split(".")
		isSelected = false
	}

	target_file = ""
	isPDB = true;
	if (index[0] === "0") {
		target_file = pdb_files[index[1]]
		isPDB = true;
	}
	if (index[0] === "1") {
		target_file = SURF_files[index[1]]
		isPDB = false;
	}
	if (index[0] === "2") {
		target_file = hbond_files[index[1]]
		isPDB = false;
	}
	console.log("Item: " + target_file)
	console.log("Selected? " + isSelected)

	return [target_file, isSelected, isPDB];
}
