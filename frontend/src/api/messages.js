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
		 await response.json();
	} catch (error) {
		console.error('Error sending help SMS:', error);
		throw error;
	}
};

const verifyPhoneNumber = async (phoneNumber) => {
	try {
		const formattedPhoneNumber = phoneNumber.startsWith('+44') ? phoneNumber : `+44${phoneNumber}`;

		const response = await fetch(`${baseUrl}/api/verify-phone-number/?phoneNumber=${encodeURIComponent(formattedPhoneNumber)}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		});

		if (response.ok) {
			const data = await response.json();
			return data.phoneNumber || formattedPhoneNumber;
		} else {
			const errorBody = await response.json();
			throw new Error(`HTTP error ${response.status}: ${errorBody.error || 'Unknown error'}`);
		}
	} catch (error) {
		console.error('Error verifying phone number:', error);
		throw error;
	}
};




export { sendHelpSMS, verifyPhoneNumber };
