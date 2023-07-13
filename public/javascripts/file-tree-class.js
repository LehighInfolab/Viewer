/**
 * File Tree Directory class handles parsing of uploads folder and post request for file names.
 */
class file_tree_dir {
	/**
	 * 
	 * @param {string} id Id of the file to be parsed
	 */
	constructor(id) {
		/**
		 * @property {string} ID
		 */
		this.id = id;
		/**
		 * @property {string} files
		 */
		this.files = this.files_in_dir();
		/**
		 * array of surface files with .SURF extension in the uploads folder
		 * @property {string[]} ID with .SURF
		 */
		this.SURF_files = [];
		/**
		 * array of PDB files with .pdb extension in the uploads folder
		 * @property {string[]} ID with .pdb
		 */
		this.pdb_files = [];
		/**
		 * array of hbond files with .txt extension in the uploads folder
		 * @property {string[]} ID with .txt
		 */
		this.hbond_files = [];
		/**
		 * all other file types
		 * @property {string[]} ID
		 */
		this.other = [];

	}

	/**
	 * Async fetch of files in uploads directory to be parsed
	 * 
	 * @returns {Object} files
	 */
	async files_in_dir() {
		var file;
		console.log("-----Fetching files in dir-----")
		return await fetch('/files_in_dir', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ "id": this.id })
		})
			.then(response => response.json())
			.then(response => {
				file = JSON.stringify(response);
				this.files = this.JSON_response_parser(file);
				return this.files;
			})
	}

	JSON_response_parser(string) {
		var str = string.replace(/["*?^${}()|[\]\\]/g, "");
		var str = str.split(",");
		return str;
	}

	/**
	 * groupFileFormats function groups files by file format eg. pdb, SURF, etc. and returns each group as a separate list
	 * 
	 * @returns {string[]} SURF_files
	 * @returns {string[]} pdb_files
	 * @returns {string[]} hbond_files
	 * @returns {string[]} other
	 */
	groupFileFormats() {
		let files = this.files;
		var SURF_files = []; var pdb_files = []; var hbond_files = []; var other = [];
		for (let i = 0; i < files.length; i++) {
			var file_format = files[i].split(".")[1];
			switch (file_format) {
				case "SURF":
					SURF_files.push(files[i]);
					continue;
				case "pdb":
					pdb_files.push(files[i]);
					continue;
				case "txt":
					hbond_files.push(files[i]);
					break;
				default:
					other.push(files[i])
			}
		}
		this.SURF_files = SURF_files;
		this.pdb_files = pdb_files;
		this.hbond_files = hbond_files
		this.other = other
		return this.SURF_files, this.pdb_files, this.hbond_files, this.other;
		// return SURF_files, pdb_files, hbond_files;
	}
}