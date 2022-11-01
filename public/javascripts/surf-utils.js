/* 
#######################################################
Utils for file loading
#######################################################
 */

/*
  *	Function to load surf files.
  *	
  * 	After loading, we make arrays of vertices, normals, and faces.
  *		We then create a custom object using these 3 arrays.
  *		This code essentially takes care of all the viewer loading
  *		and rendering that need to be done.
  */
function loadData(cnt) {
	var data = xmlhttp.responseText; // the downloaded data
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
	viewData(vertex, face, normal)
}


/*
  *	Function to view surf objects after loading
  *	
  * - Set colors and add objects to stage here.
  * 	This function is called at the end of loadData()	
  */
function viewData(vertex, face, normal) {
	var mesh_vertex = [];
	var mesh_color = [];
	var mesh_normal = [];
	color[0] = color_val / 256
	color[1] = (color_val + 256 * 3 / 7) / 256
	color[2] = (color_val + 256 * 6 / 7) / 256
	for (var i = 0; i < face.length; i++) {
		mesh_vertex.push(vertex[face[i]][0]);
		mesh_vertex.push(vertex[face[i]][1]);
		mesh_vertex.push(vertex[face[i]][2]);

		mesh_color.push(color[0]);
		mesh_color.push(color[1]);
		mesh_color.push(color[2]);
	}
	color_val = (color_val + (256 * 2 / 7)) % 256

	console.log("Surf object displayed.");
	var shape = new NGL.Shape("SURF file");
	shape.addMesh(mesh_vertex, mesh_color, undefined, undefined, cnt)
	var shapeComp = stage.addComponentFromObject(shape);
	shapeComp.addRepresentation("buffer");
	shapeComp.autoView();
}