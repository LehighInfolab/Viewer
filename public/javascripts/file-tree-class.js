/**
 * File Tree Directory
 */
class file_tree_dir {
	/**
	 * 
	 * @param {String} id Id of the file to be parsed
	 */
	constructor(id) {
		/**
		 * @property {string} ID
		 */
		this.id = id;
		/**
		 * @property {String} files
		 */
		this.files = this.files_in_dir();
		/**
		 * @property {array<SURF_files>} ID
		 */
		this.SURF_files = [];
		/**
		 * @property {array<pdb_files>} ID
		 */
		this.pdb_files = [];
		/**
		 * @property {array<hbond_files>} ID
		 */
		this.hbond_files = [];
		/**
		 * @property {array<other>} ID
		 */
		this.other = [];

	}

	/**
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

	/*
	*	groupFileFormats function
	*	- groups files by file format eg. pdb, SURF, etc.
	*	- and returns each group as a separate list
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