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
function loadData(file) {
	// console.log(file)
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
	viewData(file, vertex, face, normal)
}


/*
  *	Function to view surf objects after loading
  *	
  * - Set colors and add objects to stage here.
  * 	This function is called at the end of loadData()	
  */
function viewData(file, vertex, face, normal) {
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

	// console.log("Surf object displayed.");

	console.log("Updating viewer with " + file + "...")
	var shape = new NGL.Shape(file);
	shape.addMesh(mesh_vertex, mesh_color, undefined, undefined, file)
	var shapeComp = stage.addComponentFromObject(shape);
	shapeComp.addRepresentation("buffer");
	shapeComp.setVisibility(false)
	shapeComp.autoView();
}


// /*
//   *	Formatting XML to be used in xmlhttp requests. 
//   * - For now, nothing to format. Leaving it here so that it is available in the future.
//   */
// function formatXML(file, xmlDoc) {
// 	// var x = xmlDoc.getElementsByTagName("TAGNAME");
// 	console.log(file);
// }


// /*
//   *	Asynchronous load using XMLHttpRequest.
//   * - This function only loads one surf file at a time
//   * 
//   */
// async function getSURFXML(file) {
// 	console.log("Fetching surf data from " + file + "...");
// 	xmlhttp.open(method, "../uploads/" + file, true);
// 	xmlhttp.onreadystatechange = function () {
// 		if (xmlhttp.readyState === XMLHttpRequest.DONE && xmlhttp.status === 200) {
// 			formatXML(file, xmlhttp.responseText);
// 			console.log("Loading " + file + " into viewer...");
// 			loadData(file)
// 		}
// 	};
// 	xmlhttp.send();
// }

/*
  *	Asynchronous load using XMLHttpRequest.
  * 
  * - Setup xmlhttp with functions and requests to be called upon send().
  * 	First get list of files[] containing all files to be viewed, and open all.
  *		When a file is "ready", format XML and then load data. TODO: No need to format for now but left here just in case.
  *		Recursive getXML() call to loop through all files. TODO: Recursion isn't great but it works here, so I'll leave it.
  *		Finally, send() requests to server.
  */
// Global variables for setting up XML asynchronous file loading
var xmlhttp = new XMLHttpRequest(), method = "GET";

async function getXML(id, files, cnt) {
	console.log(files)
	console.log(files.length)
	if (files.length <= 0) {
		return;
	}

	let opened = await xmlhttp.open(method, "../uploads/" + id + "/" + files[cnt], true);	// open all files in files[cnt]
	console.log("From dir :", id, "--- Loading SURF file: ", files[cnt]);

	// onreadystatechange - when file loaded, check if file is ready and no errors thrown. If so, call function to formatXML, loadData and getXML() on next file
	xmlhttp.onreadystatechange = async function () {
		if (xmlhttp.readyState === XMLHttpRequest.DONE && xmlhttp.status === 200) {
			// formatXML(files[cnt], xmlhttp.responseText);
			console.log("Loading " + files[cnt] + " into viewer...");
			loadData(files[cnt])
			cnt++;
			if (cnt < files.length) getXML(id, files, cnt); // call again
		}
	};
	let sent = await xmlhttp.send();
	return;
}