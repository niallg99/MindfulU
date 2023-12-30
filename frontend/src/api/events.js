const baseUrl = `http://${window.location.hostname}:8000`;
import { getAccessToken } from '@/api/auth';

export function fetchEvents() {
	const accessToken = getAccessToken();
	return fetch(`${baseUrl}/api/events/`, {
		headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${accessToken}`,
			},
	})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok')
			}
			return response.json()
	});
}
