const baseUrl = `http://${window.location.hostname}:8000`;

const getAccessToken = () => {
		return localStorage.getItem('accessToken');
};

export const getLatestBroadcastMessage = async () => {
		try {
				const response = await fetch(`${baseUrl}/api/get-latest-broadcast-message/`);
				if (!response.ok) {
						throw new Error('Failed to fetch the latest broadcast message');
				}
				const data = await response.json();
				return data.message;
		} catch (error) {
				throw new Error('Error fetching latest broadcast message', error);
		}
};

export const saveBroadcastMessage = async (message) => {
		const accessToken = getAccessToken();
		if (!accessToken) {
				throw new Error('Access token not found');
		}
		try {
				const response = await fetch(`${baseUrl}/api/save-broadcast-message/`, {
						method: 'POST',
						headers: {
								'Content-Type': 'application/json',
								'Authorization': `Bearer ${accessToken}`
						},
						body: JSON.stringify({ message })
				});
				if (!response.ok) {
						throw new Error('Failed to save broadcast message');
				}
				return await response.json();
		} catch (error) {
				throw new Error('Error saving broadcast message', error);
		}
};
