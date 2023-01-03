/* 
#######################################################
Utils for hydrogen bond file loading
#######################################################
*/
function loadHBond(file) {
	console.log("Loading hbond file: " + file);
	var lines;
	fetch('file.txt')
  .then(response => response.text())
  .then(text => lines = text.toString().split("\n"))
  // outputs the content of the text file
	//var lines = fs.readFileSync(file).toString().split("\n"); // the downloaded data split into lines
	console.log(lines);

    var bonds = []; // array holds the coordinates for each bond
    var bondIndex = 0; // index for keeping track of bonds
	var totalBonds;
	var bondPairs = []; // array holds which bonds pair with each other
	var pairIndex = 0; // index for keeing track of bonds
	var totalPairs;
	var temp; // temporary variable
    var readingBonds = false; var readingPair = false; // boolean to switch between reading bond vertices and bond pairs

    for (var i = 0; i < lines.length; i++) {
        if (!readingBonds) {
			if (lines[i].split(" ")[0] == "#NUMBER_OF_ATOMS") {
				totalBonds = parseInt(lines[i].split(" ")[1]);
				readingBonds = true;
				console.log("Reading bonds: " + totalBonds)
			}
		} else {
			if (bondIndex < totalBonds) {
				temp = lines[i].split("\t");
				x = Number(temp[5]);
				y = Number(temp[6]);
				z = Number(temp[7]);
				bonds.push([x,y,z]);
				bondIndex++;
			} else {
				if (!readingPair) {
					if (lines[i].split(" ")[0] == "#NUMBER_OF_HBONDS") {
						totalPairs = parseInt(lines[i].split(" ")[1]);
						readingPairs = true;
						console.log("Reading pairs: " + totalPairs)
					}
				} else {
					if (pairIndex < totalPairs) {
						temp = lines[i].split("\t");
						first = parseInt(temp[0]);
						second = parseInt(temp[1]);
						bondPairs.push([bonds[first], bonds[second]]);
						pairIndex++;
					}
				}
			}
		}
    }
	console.log("bonds: " + bonds)
	console.log("bond pairs: " + bondPairs)
    viewHBond(file, bonds, bondPairs);
}

function viewHBond(file, bonds, bondPairs) {
	var mesh_vertex = [];
	var mesh_color = [];
	var mesh_normal = [];

	console.log("Updating viewer with " + file);
    var shape = new NGL.Shape(file);
	shape.addMesh(bonds, (0, 0, 0, 0), undefined, undefined);
	for (var i = 0; i < bondPairs.length; i++) {
		shape.addCylinder(bondPairs[i][0], bondPairs[i][1], [1, 0, 0], 5);
	}
	var shapeComp = stage.addComponentFromObject(shape);
	shapeComp.addRepresentation("buffer");
	shapeComp.setVisibility(true);

	// test to view object in viewport
	// add a single red sphere from a buffer to a shape instance
	var test = new NGL.Shape( "shape" );
	var sphereBuffer = new NGL.SphereBuffer( {
		position: new Float32Array( [ 10, 10, 0 ] ),
		color: new Float32Array( [ 1, 0, 0 ] ),
		radius: new Float32Array( [ 1 ] )
	} );
	test.addBuffer( sphereBuffer );
	var testShapeComp = stage.addComponentFromObject( test );
	testShapeComp.addRepresentation( "buffer" );

    // load a HBond structure and consume the returned `Promise`
	// stage.loadFile("../uploads/" + file, { name: hbond_name }).then(function (component) {
	// 	// add a "cartoon" representation to the structure component
	// 	component.addRepresentation("line");
	// 	component.setVisibility(false)
	// 	// provide a "good" view of the structure
	// 	// component.autoView();
	// });
	// stage.getComponentsByName(pdb_name).addRepresentation("cartoon", { color: "blue" });
	// visible_components.push(pdb_name)
}