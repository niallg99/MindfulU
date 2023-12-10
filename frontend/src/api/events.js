const baseUrl = 'http://0.0.0.0:8000';

export function fetchEvents() {
	return fetch(`${baseUrl}/api/events/`)
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok')
			}
			return response.json()
	});
}
