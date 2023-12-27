const baseUrl = `http://${window.location.hostname}:8000`;

const getAccessToken = () => {
	return localStorage.getItem('accessToken');
};

const fetchMoodStatistics = async () => {
	try {
		const accessToken = getAccessToken();
		const url = `${baseUrl}/api/mood-statistics/`;
		const response = await fetch(url, {
			headers: {
				'Authorization': `Bearer ${accessToken}`,
			},
		});
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		const moodStats = await response.json();
		return moodStats;
	} catch (error) {
		console.error("Could not fetch mood statistics:", error);
		throw error;
	}
};

export { fetchMoodStatistics };
