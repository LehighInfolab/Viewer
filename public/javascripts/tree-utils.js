/* 
#######################################################
Utils for tree setup
#######################################################
 */

// function starts the tree by adding a group item first
function startTree(tree, id) {
	newGroup = document.createElement('smart-tree-items-group');
	newGroup.id = id;
	newGroup.label = id;
	newGroup.expanded = true;
	newGroup.separator = false;
	// newGroup.level = -1;
	tree.addTo(newGroup)
	return;
}


function makeTree(tree, id, files) {
	for (let i = 0; i < files.length; i++) {
		newItem = document.createElement('smart-tree-items');
		newItem.label = files[i];
		tree.addTo(newItem, id);
	}
}

// function makeTree(tree, id, SURF_files, pdb_files) {
// 	for (let i = 0; i < pdb_files.length; i++) {
// 		newItem = document.createElement('smart-tree-items');
// 		newItem.label = pdb_files[i];
// 		tree.addTo(newItem, id);
// 	}
// 	for (let i = 0; i < SURF_files.length; i++) {
// 		newItem = document.createElement('smart-tree-items');
// 		newItem.label = SURF_files[i];
// 		tree.addTo(newItem, id);
// 	}
// }


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


// function parseSelectionIndex(selectedIndexes, oldSelectedIndexes) {
// 	let selected_diff = selectedIndexes.filter(x => !oldSelectedIndexes.includes(x));
// 	let unselected_diff = oldSelectedIndexes.filter(x => !selectedIndexes.includes(x));

// 	index = []
// 	isSelected = true
// 	if (selected_diff != "") {
// 		index = selected_diff[0].split(".")
// 		isSelected = true
// 	} else {
// 		index = unselected_diff[0].split(".")
// 		isSelected = false
// 	}
// 	console.log(index)

// 	// target_file = ""
// 	// isPDB = true;
// 	// if (index[0] === "0") {
// 	// 	target_file = pdb_files[index[1]]
// 	// 	isPDB = true;
// 	// }
// 	// if (index[0] === "1") {
// 	// 	target_file = SURF_files[index[1]]
// 	// 	isPDB = false;
// 	// }
// 	// console.log("Item: " + item)
// 	// console.log("Selected? " + isSelected)

// 	// return [item, isSelected];
// 	return index, isSelected;
// }
