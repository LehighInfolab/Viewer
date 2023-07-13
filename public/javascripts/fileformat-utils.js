/**
 * getFiles function -  gets document element "fileData" sent by server which contains files from "uploads" folder in public. Initial packet sent by server via json for file locations.
 * @returns {string[]}
 */
/*
 *	
 *	
 */
function getFiles() {
	var all_files = document.getElementById("fileData").getAttribute("data-files");
	all_files = all_files.replace(/[\/\\\[\]()'":*?]/g, '');
	all_files = all_files.split(",");
	return all_files;
}
