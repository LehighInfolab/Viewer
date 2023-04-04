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
