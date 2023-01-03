/* 
#######################################################
Utils for hydrogen bond file loading
#######################################################
*/
function loadHBond(file) {
	var data = parseHBond(file);
	//var data = xmlhttp.responseText; // the downloaded data
	var lines = data.split("\n"); // the downloaded data split into lines
	console.log(lines);

    var bonds = []; var bondPairs = []; // array holds the coordinates for each bond and bond pairs
	var bondIndex = 0; var pairIndex = 0; // index for keeing track of bonds and pairs
	var totalPairs; var totalBonds;
    var readingBonds = false; var readingPair = false; // boolean to switch between reading bond vertices and bond pairs
	var temp; // temporary variable

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

}

function parseHBond(file) {
	var jqXHR = $.ajax({
		type: "POST",
		url: "python/parser_hbonds_file.py",
		async: false,
		data: {"method": "call", 
			   "param": {
					"method": "main",
					"args":file,
			   }},
	});
	console.log(jqXHR.responseText)
	return jqXHR.responseText;
}