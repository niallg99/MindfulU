const baseUrl = `http://${window.location.hostname}:8000`;

export function fetchSupport() {
	return fetch(`${baseUrl}/api/custom_support_links/`)
		.then(response => {
			if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	});
}
