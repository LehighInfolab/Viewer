class file_tree_dir {
	constructor(id) {
		this.id = id;
		this.files = [];
	}

	async files_in_dir() {
		var files;
		console.log("Inside files_in_dir")
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
				files = JSON.stringify(response);
				this.files = files;
				return files;
			})
	}
}