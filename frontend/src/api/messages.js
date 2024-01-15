import { getAccessToken } from '@/api/auth';
import loginApi from '@/api/login';

const baseUrl = `http://${window.location.hostname}:8000`;

const sendHelpSMS = async () => {
	try {
		const accessToken = getAccessToken();
		if (!accessToken) {
			throw new Error('Access token is missing or invalid');
		}

		const csrfToken = await loginApi.getCSRFToken();

		const response = await fetch(`${baseUrl}/api/send-help-sms/`, {
			method: 'POST',
			headers: {
				'Authorization': `Bearer ${accessToken}`,
				'X-CSRFToken': csrfToken,
			},
		});

		if (!response.ok) {
			const errorBody = await response.json();
			throw new Error(`HTTP error ${response.status}: ${errorBody.detail || 'Unknown error'}`);
		}

		const data = await response.json();
		console.log(data);
	} catch (error) {
		console.error('Error sending help SMS:', error);
		throw error;
	}
};

export { sendHelpSMS };
