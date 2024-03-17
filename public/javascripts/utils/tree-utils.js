/** 
#######################################################
Utils for tree event handlers
#######################################################
* @param {smart-tree} tree
* @param {string} id 
} tree 
*/

/**
 * function allows webserver to load for a second to retrieve data associated to a PDB (eg. maybe split into chains, cartoon view, stick view, etc.)
 * TODO: NEED TO ADD DATA CHANGES AFTER EXPANSION
 * 
 * @param {smart-tree} tree 
 */
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

/**
 * treeSelectionEventHandler() handles visibility of objects when the associated index of the file tree is checked or unchecked using an eventListener().
 * 
 * @param {smart-tree} tree 
 * @returns {None}
 */
function treeSelectionEventHandler(tree) {
	tree.addEventListener('change', function (event) {
		var detail = event.detail,
			item = detail.item,
			oldSelectedIndexes = detail.oldSelectedIndexes,
			selectedIndexes = detail.selectedIndexes;

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
			stage.getComponentsByName(item.label).autoView(500);
			console.log("Showing", item.label)
		}
		if (!isSelected) {
			stage.getComponentsByName(item.label).setVisibility(false);
			console.log("Hiding", item.label)
		}
	})
	return;
}