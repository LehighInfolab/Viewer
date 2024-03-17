/**
#######################################################
Utils for file loading
#######################################################
*/

// Global variable to hold color value for objects in RGB. This is global so that each objects colors can be adjusted based on previous object color.
/**@global */
var color_val = 0; var color = [];

/**
*	Function to load surf files.
*	
* 	After loading, we make arrays of vertices, normals, and faces.
*		We then create a custom object using these 3 arrays.
*		This code essentially takes care of all the viewer loading
*		and rendering that need to be done.
*
*	@param {string} file
*/
function loadSurfData(file, data) {
	// console.log(file)
	// var data = xmlhttp.responseText; // the downloaded data
	var lines = data.split("\n"); // the downloaded data split into lines

	var vertex = []; var normal = []; var face = [];	// array for holding parsed data of each type

	var vert_index = 0; var face_index = 0;	// index for keeping track of how many verts/faces have been read

	var num_vertices = 0; var num_faces = 0;	// index for holding total number of verts/faces as provided in surf file.

	var readingVert = false; var readingFace = false;	// boolean to switch when we're done reading verts/faces

	var temp_line;

	for (var i = 0; i < lines.length; i++) {
		if (!readingVert) {
			if (lines[i].substr(0, "GEOMETRY:".length) == "GEOMETRY:") {
				num_vertices = lines[i].split(" ")[1];
				readingVert = true;
			}
		} else {
			if (vert_index < num_vertices) {
				temp_line = lines[i].split(" ");
				v1 = Number(temp_line[0]);
				v2 = Number(temp_line[1]);
				v3 = Number(temp_line[2]);
				vertex.push([v1, v2, v3]);

				var normals = [];
				n1 = temp_line[3];
				n2 = temp_line[4];
				n3 = temp_line[5];
				normals.push([n1, n2, n3])

				vert_index++;
			} else {
				if (!readingFace) {
					if (lines[i].substr(0, "TOPOLOGY:".length) == "TOPOLOGY:") {
						num_faces = lines[i].split(" ")[1];
						readingFace = true;
					}
				} else {
					if (face_index < num_faces) {
						temp_line = lines[i].split(" ");
						f1 = Number(temp_line[0]);
						f2 = Number(temp_line[1]);
						f3 = Number(temp_line[2]);
						face.push(f1);
						face.push(f2);
						face.push(f3);
						face_index++;
					}
				}
			}
		}
	}
	viewSurfData(file, vertex, face, normal)
}


/**
*	Function to view surf objects after loading
*	
*   Set colors and add objects to stage here.
* 	This function is called at the end of loadData()	
*	
* @param {int[]} face 
* @param {string} file 
* @param {int[]} normal 
* @param {int[]} vertex 
*/
function viewSurfData(file, vertex, face, normal) {
	var mesh_vertex = [];
	var mesh_color = [];
	var mesh_normal = [];

	var color = [];

	// Generate color components based on color_val
	color[0] = Math.sin(0.3 * color_val + 0) * 127 + 128; // Red
	color[1] = Math.sin(0.3 * color_val + 2) * 127 + 60; // Green
	color[2] = Math.sin(0.3 * color_val + 4) * 127 + 20; // Blue

	for (var i = 0; i < face.length; i++) {
		mesh_vertex.push(vertex[face[i]][0]);
		mesh_vertex.push(vertex[face[i]][1]);
		mesh_vertex.push(vertex[face[i]][2]);

		mesh_color.push(color[0] / 256);
		mesh_color.push(color[1] / 256);
		mesh_color.push(color[2] / 256);
	}
	color_val = (color_val + 1)

	// console.log("Surf object displayed.");

	console.log("Adding SURF to viewer: " + file)
	var shape = new NGL.Shape(file);
	shape.addMesh(mesh_vertex, mesh_color, undefined, undefined, file)
	var shapeComp = stage.addComponentFromObject(shape);
	shapeComp.addRepresentation("buffer");
	shapeComp.setVisibility(false)
	shapeComp.autoView();
}

/**
  *	Asynchronous load SURF files.
 * 
 * @param {string} id
 * @param {string} files
 * @param {int} cnt - index for surf object
*/
async function getSurfXML(dir, file) {
	if (file.split(".").pop() != "SURF") {
		return;
	}
	const url = "../uploads/" + dir + "/" + file;
	try {
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		// Here, you'd typically process the response depending on what you expect (e.g., text, JSON)
		const data = await response.text(); // Assuming the response is text
		console.log("Loading SURF file: " + file);

		// Assuming loadSurfData is a function that takes the response data as a parameter
		loadSurfData(file, data);

		// Optionally return the data in case the caller wants to use it
		return data;
	} catch (error) {
		console.error("Failed to fetch SURF file:", file, "Error:", error);
	}
}