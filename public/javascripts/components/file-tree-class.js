/**
 * FileTreeDirectory class handles parsing of uploads folder and post request for file names.
 */
class FileTreeDirectory {
	/**
	 * Constructor for FileTreeDirectory class.
	 * @param {string} id ID of the directory to be parsed. This is usually uploads
	 * @param {'smart-tree'} tree
	 */
	constructor(id, tree) {
		this.id = id;
		this.tree = tree;
		this.fileHierarchy = []

		this.SURF_files = [];
		this.pdb_files = [];
		this.hbond_files = [];
		this.other = [];
	}

	// Call to asynchronously fetch and set files
	async init() {
		await this.initializeFiles();
		await this.initializeTree();
		return this;
	}

	async getFiles(id) {
		try {
			var response = await fetch('/files_in_dir', {
				method: 'POST',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ "id": id })
			});
			if (!response.ok) {
				throw new Error('Network response was not ok.');
			}
			var responseData = await response.json();
			var files = JSON_response_parser(JSON.stringify(responseData));
			return files
		} catch (error) {
			console.error("Failed fetching files:", error);
		}
	}

	async initializeFiles() {
		let hierarchy = {
			files: [], // Files in the root
			directories: {} // Directories with their respective files
		};
		for (const item of this.id) {
			if (item.includes('.')) {
				// It's a file, add it to the root files list
				hierarchy.files.push(item);
			} else {
				// It's a directory, need to fetch its contents
				try {
					// Assuming `getFiles` fetches the contents of the directory and returns a list of file names
					const directoryFiles = await this.getFiles(item);
					// Now, process the fetched files
					hierarchy.directories[item] = directoryFiles;
					// This filters out any subdirectories, assuming you only go one directory deep
					// and assuming `getFiles` returns filenames with dots for actual files
				} catch (error) {
					console.error(`Failed to fetch files for directory ${item}:`, error);
				}
			}
		}

		this.fileHierarchy = hierarchy; // Store the hierarchy structure
		console.log("File hierarchy", this.fileHierarchy); // Log the hierarchy structure
	}

	async initializeTree() {
		for (let rootDirs in this.fileHierarchy.directories) {
			this.startTree(this.tree, rootDirs)
			console.log(this.fileHierarchy.directories[rootDirs])
			for (let i = 0; i < this.fileHierarchy.directories[rootDirs].length; i++) {
				this.makeTree(this.tree, rootDirs, this.fileHierarchy.directories[rootDirs][i])
			}
		}
	}

	/**
	 * Groups files by file format (e.g., pdb, SURF) and updates the corresponding properties.
	 */
	groupFileFormats() {
		this.files.forEach(file => {
			var fileFormat = file.split(".").pop();
			switch (fileFormat) {
				case "SURF":
					this.SURF_files.push(file);
					break;
				case "pdb":
					this.pdb_files.push(file);
					break;
				case "txt":
					this.hbond_files.push(file);
					break;
				default:
					this.other.push(file);
			}
		});
	}

	// function starts the tree by adding a group item first
	startTree(tree, id) {
		var newGroup = document.createElement('smart-tree-items-group');
		newGroup.id = id;
		newGroup.label = id;
		newGroup.expanded = true;
		newGroup.separator = false;
		// newGroup.level = -1;
		tree.addTo(newGroup)
		return;
	}

	/**
	 * Creates tree from a list of files
	 * 
	 * @param {smart-tree} tree 
	 * @param {string} id 
	 * @param {string} files 
	 */
	makeTree(tree, parent_id, label) {
		var newItem = document.createElement('smart-tree-items');
		newItem.label = label
		tree.addTo(newItem, parent_id);
	}

	async callbackAllFiles(callback) {
		var files = [];
		var hierarchy = this.fileHierarchy
		// Loop through directories and their files
		for (let dir in hierarchy.directories) {
			if (hierarchy.directories.hasOwnProperty(dir)) {
				hierarchy.directories[dir].forEach(file => {
					callback(dir, file)
				});
			}
		}
		// Loop through files in the root
		this.fileHierarchy.files.forEach(file => {
			callback(dir, file)
		});
		return files
	}
}