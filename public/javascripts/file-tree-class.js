class file_tree_dir {
	constructor(id) {
		this.id = id;
		this.files = this.files_in_dir();
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
		var str = string.replace(/["*+?^${}()|[\]\\]/g, "");
		var str = str.split(",");
		return str;
	}
}