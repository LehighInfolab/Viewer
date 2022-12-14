/* 
#######################################################
Utils for hydrogen bond file loading
#######################################################
*/

 /*
  *	Async function to load hydrogen bond files.
  *	
  * 	After loading, we make an array of vertices and
  * 	pair together the vertices that form each hydrogen bond.
  *		We then create a custom object composed of cylinders using
  *		the vertex pairs.
  */
async function loadHBond(file) {
	var bonds = []; var bondPairs = []; // array holds the coordinates for each bond and bond pairs
	var bondIndex = 0; var pairIndex = 0; // index for keeing track of bonds and pairs
	var totalPairs; var totalBonds;
    var readingBonds = false; var readingPair = false; // boolean to switch between reading bond vertices and bond pairs
	var temp; // temporary variable

	let data = await fetch("../uploads/"+file).then(response => response.text());
	var lines = data.toString().split("\n");

	for (var i = 0; i < lines.length; i++) {
		// Reading vertices
		if (!readingBonds) {
			if (lines[i].split(" ")[0] == "#NUMBER_OF_ATOMS") {
				totalBonds = parseInt(lines[i].split(" ")[1]);
				readingBonds = true;
			}
		} else {
			if (bondIndex < totalBonds) {
				temp = (lines[i].replace(/\s+/g, ' ').trim()).split(" ");
				x = parseFloat(temp[5]);
				y = parseFloat(temp[6]);
				z = parseFloat(temp[7]);
				bonds.push([x,y,z]);

				bondIndex++;
			} else {
				// Pairing together vertices that form bonds
				if (!readingPair) {
					if (lines[i].split(" ")[0] == "#NUMBER_OF_HBONDS") {
						totalPairs = parseInt(lines[i].split(" ")[1]);
						readingPair = true;
					}
				} else {
					if (pairIndex < totalPairs) {
						temp = (lines[i].replace(/\s+/g, ' ').trim()).split(" ");
						first = bonds[parseInt(temp[0])];
						second = bonds[parseInt(temp[1])];
						bondPairs.push([first, second]);

						pairIndex++;
					}
				}
			}
		}
	}
	// Render hydrogen bonds
    viewHBond(file, bonds, bondPairs);
}

/*
  *	Function to view hydrogen bonds after loading data
  *	
  * - Set colors and add objects to stage here.
  * 	This function is called at the end of loadHBond()	
  */
function viewHBond(file, bonds, bondPairs) {
	var mesh_vertex = [];
	var mesh_color = [];
	var mesh_normal = [];

	console.log("Updating viewer with " + file);
    var shape = new NGL.Shape(file);
	shape.addMesh(bonds, (0, 0, 0, 0), undefined, undefined);
	for (var i = 0; i < bondPairs.length; i++) {
		// Add each bond as a grey cylinder
		shape.addCylinder(bondPairs[i][0], bondPairs[i][1], [0.5, 0.5, 0.5], 0.2);
	}
	var shapeComp = stage.addComponentFromObject(shape);
	shapeComp.addRepresentation("buffer");
	shapeComp.setVisibility(true);
	shapeComp.autoView();
}