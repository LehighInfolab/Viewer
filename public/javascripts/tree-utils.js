/* 
#######################################################
Utils for tree setup
#######################################################
 */


function treeSelectionEventHandler(tree) {
	tree.addEventListener('change', function (event) {
		const detail = event.detail,
			item = detail.item,
			oldSelectedIndexes = detail.oldSelectedIndexes,
			selectedIndexes = detail.selectedIndexes;

		// event handling code goes here.
		console.log("handling event")
		console.log(item)
		console.log(selectedIndexes)
	})
}


// TODO: NEED TO ADD DATA CHANGES AFTER EXPANSION
// function allows webserver to load for a second to retrieve data associated to a PDB (eg. maybe split into chains, cartoon view, stick view, etc.)
function expandPDB(tree) {
	tree.addEventListener("expand", function (event) {
		if (event.detail.children.length > 0) {
			return;
		}

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

function makeTree(tree, pdb_files, SURF_files) {
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
}