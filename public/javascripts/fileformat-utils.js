/*
 *	getFiles function
 *	- get document element "fileData" sent by server which contains files from "Uploads" folder in public
 */
function getFiles() {
	var all_files = document.getElementById("fileData").getAttribute("data-files");
	all_files = all_files.replace(/[\/\\\[\]()'":*?]/g, '');
	all_files = all_files.split(",");
	return all_files;
}


/*
 *	groupFileFormats function
 *	- groups files by file format eg. pdb, SURF, etc.
 *	- and returns each group as a separate list
 */
function groupFileFormats(files) {
	for (let i = 0; i < files.length; i++) {
		file_format = files[i].split(".")[1];
		switch (file_format) {
			case "SURF":
				SURF_files.push(files[i]);
				break;
			case "pdb":
				pdb_files.push(files[i]);
				break;
<<<<<<< HEAD
			// case "txt":
			// 	hbond_files.push(files[i]);
			// 	break;
		}
	}
	return SURF_files, pdb_files;
	// return SURF_files, pdb_files, hbond_files;
=======
			case "txt":
				// verify it's an hbond file
				if (verifyHBondFile(files[i])) {
					console.log(files[i]+" is a valid hbond file");
					hbond_files.push(files[i]);
				} else {
					console.log("Error: not an hbond file");
				}
				break;
		}
	}
	return SURF_files, pdb_files, hbond_files;
}

async function verifyHBondFile(file) {
	console.log("Fetching "+file+" ...");
	let data = await fetch("../uploads/"+file).then(response => response.text());
	// console.log("Parsing "+file+" ...");
	var lines = data.toString().split("\n");
	//console.log(lines[0].split(" ")[0]);
	if ((lines[0].split(" ")[0] == "#NUMBER_OF_ATOMS"))
		return true;
	else
		return false;
>>>>>>> 89fbb5c (HBond support for getFileFormats())
}