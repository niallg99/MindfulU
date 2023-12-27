const baseUrl = `http://${window.location.hostname}:8000`;
import loginApi from './login';
import { getAccessToken } from '@/api/auth';

const updateProfile = async (formData) => {
	const csrfToken = await loginApi.getCSRFToken();
	const accessToken = getAccessToken();

	try {
		const response = await fetch(`${baseUrl}/api/user/update-profile/`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrfToken,
				'Authorization': `Bearer ${accessToken}`,
			},
			body: formData,
		});

		if (!response.ok) {
			const error = await response.json();
			throw new Error(error.message);
		}

		const data = await response.json();

		if (data.newProfilePictureUrl && !data.newProfilePictureUrl.startsWith('http')) {
			data.newProfilePictureUrl = `${baseUrl}/${data.newProfilePictureUrl}?t=${Date.now()}`;
		}

		return data;
	} catch (error) {
		console.error('Error updating profile:', error);
		throw error;
	}
};



const saveShowMoodPreference = async (showMood) => {
	const accessToken = getAccessToken();
	const url = `${baseUrl}/api/user/update-preferences`;

	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${accessToken}`,
		},
		body: JSON.stringify({ showMood }),
	});

	if (!response.ok) {
		throw new Error(`HTTP error! Status: ${response.status}`);
	}

	return await response.json();
};


export { updateProfile, saveShowMoodPreference };