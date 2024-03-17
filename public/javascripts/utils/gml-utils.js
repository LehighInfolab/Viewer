/**
#######################################################
Utils for bond gml file loading
#######################################################
*/

async function loadGML(dir, file) {
	if (file.split(".").pop() !== "gml") {
		return;
	}

	let nodeCoords = []; // Array to hold coordinates for each node by ID
	let edges = []; // Array to hold edge source and target indices

	let data = await fetch(`../uploads/${dir}/${file}`).then(response => response.text());
	let lines = data.split("\n");

	let coordCount = 0; // Counter for coordinates (3 per node)
	let edgePartsCount = 0; // Counter for edge parts (2 per edge: source and target)
	let currentCoords = []; // Temporary storage for current node coordinates
	let currentNodeId; // Temporary storage for current node ID
	let tempEdge = {}; // Temporary storage for current edge source and target

	lines.forEach((line, index) => {
		line = line.trim();
		const parts = line.split(/\s+/);

		if (line.startsWith("node [")) {
			coordCount = 0; // Reset coordinate counter for new node
			currentCoords = []; // Reset coordinate storage
		} else if (line.startsWith("id")) {
			currentNodeId = parseInt(parts[1], 10);
		} else if (line.startsWith("coord") && coordCount < 3) {
			currentCoords.push(parseFloat(parts[1]));
			coordCount++;
			if (coordCount === 3) { // Once 3 coordinates are read
				nodeCoords[currentNodeId] = currentCoords;
			}
		} else if (line.startsWith("edge [")) {
			edgePartsCount = 0; // Reset edge parts counter for new edge
		} else if ((line.startsWith("source") || line.startsWith("target")) && edgePartsCount < 2) {
			tempEdge[line.split(" ")[0]] = parseInt(parts[1], 10);
			edgePartsCount++;
			if (edgePartsCount === 2) { // Once source and target are read
				edges.push([tempEdge.source, tempEdge.target]);
			}
		}
	});

	const coordinatePairs = edges.map(edge => {
		const sourceCoords = nodeCoords[edge[0]];
		const targetCoords = nodeCoords[edge[1]];
		return [sourceCoords, targetCoords]; // Array of two coordinate sets
	});

	viewBond(file, coordinatePairs);
}


/**
 * Function to view hydrogen bonds after loading data.
 * 
 * @param {string} file Name of the file for reference.
 * @param {array[]} bonds Array of bond coordinates.
 * @param {array[]} bondPairs Array of bond pair coordinates.
 */
function viewBond(file, bondPairs) {
	console.log("Loading gml file: " + file);
	let shape = new NGL.Shape(file);

	bondPairs.forEach(([start, end]) => {
		// Add each bond as a grey cylinder
		shape.addCylinder(start, end, [0.5, 0.5, 0.5], 0.2);
	});

	let shapeComp = stage.addComponentFromObject(shape);
	shapeComp.addRepresentation("buffer");
	shapeComp.setVisibility(false);
	shapeComp.autoView();
}
