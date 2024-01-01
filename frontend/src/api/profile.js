const baseUrl = `http://${window.location.hostname}:8000`;
import { getAccessToken } from '@/api/auth';
import { getCloudinaryPreset, getCloudinaryCloudName } from '@/api/cloudinary';

const updateProfile = async (formData) => {
	try {
		const uploadPreset = getCloudinaryPreset();
		const cloudName = getCloudinaryCloudName();

		formData.append('upload_preset', uploadPreset);

		const cloudinaryResponse = await fetch(`https://api.cloudinary.com/v1_1/${cloudName}/image/upload`, {
			method: 'POST',
			body: formData
		});

		if (!cloudinaryResponse.ok) {
			throw new Error(`Cloudinary upload failed: ${cloudinaryResponse.statusText}`);
		}

		const cloudinaryData = await cloudinaryResponse.json();
		const profilePictureUrl = cloudinaryData.secure_url;

		const accessToken = getAccessToken();
		const url = await fetch(`${baseUrl}/api/user/update-profile/`, {
			method: 'POST',
			headers: {
				'Authorization': `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ profilePictureUrl })
		});
		
		console.log(JSON.stringify({ profilePictureUrl }),'aaaaa')
		if (!url.ok) {
			throw new Error(`Backend update failed: ${url.statusText}`);
		}

		return await url.json();
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