/**
 * Parses a JSON response string, sanitizing and splitting it into an array.
 * @param {string} string JSON string to parse.
 * @returns {string[]} Parsed and sanitized file names.
 */
function JSON_response_parser(string) {
	return string.replace(/["*?^${}()|[\]\\]/g, "").split(",");
}