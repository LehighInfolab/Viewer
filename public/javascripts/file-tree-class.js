class file_tree_dir {
	constructor(id) {
		this.id = id;
		this.files = this.files_in_dir();
		this.SURF_files = [];
		this.pdb_files = [];
	}

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
		var SURF_files = []; var pdb_files = []; var hbond_files = [];
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
			}
		}
		this.SURF_files = SURF_files;
		this.pdb_files = pdb_files;
		return this.SURF_files, this.pdb_files;
		// return SURF_files, pdb_files, hbond_files;
	}
}