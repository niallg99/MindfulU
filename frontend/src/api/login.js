const baseUrl = `http://${window.location.hostname}:8000`;

const getCSRFToken = async () => {
	try {
		const response = await fetch(`${baseUrl}/api/get-csrf-token/`);

		if (!response.ok) {
			throw new Error('Failed to fetch CSRF token');
		}
		const csrfToken = await response.json();
		return csrfToken.csrf_token;
	} catch (error) {
		console.error('Error fetching CSRF token:', error);
		throw error;
	}
};

const checkCSRFToken = async () => {
	try {
		const csrfToken = await getCSRFToken();
		return csrfToken;
	} catch (error) {
		console.error('Error checking CSRF token:', error);
		throw error;
	}
};

function loginUser(userData) {
	return checkCSRFToken()
		.then(csrfToken => {
			return fetch(`${baseUrl}/api/login/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrfToken,
				},
				body: JSON.stringify(userData),
			})
			.then(response => {
				if (!response.ok) {
					return response.json().then(data => {
						throw new Error('Login failed: ' + (data.error || 'Unknown error'));
					});
				}
				return response.json();
			});
		})
		.catch(error => {
			console.error('Error in loginUser:', error);
			throw error;
		});
}

async function resetUserPassword(email, newPassword) {
	try {
		const csrfToken = await getCSRFToken();

	const response = await fetch(`${baseUrl}/api/reset-password/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken,
			},
			body: JSON.stringify({ email, new_password: newPassword }),
});

		if (!response.ok) {
			if (response.headers.get("content-type")?.includes("application/json")) {
				const errorData = await response.json();
				throw new Error('Password reset failed: ' + (errorData.error || 'Unknown error'));
			} else {
				const errorText = await response.text();
				throw new Error('Password reset failed: ' + errorText);
			}
		}

	} catch (error) {
			console.error('Error in resetUserPassword:', error);
			throw error;
	}
}

async function verifyUserDetails(userData) {
	try {
		const csrfToken = await getCSRFToken();

		const response = await fetch(`${baseUrl}/api/verify-user-details/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken,
			},
			body: JSON.stringify(userData),
		});

		if (!response.ok) {
			const errorData = await response.json();
			throw new Error('Verification failed: ' + (errorData.error || 'Unknown error'));
		}

		return await response.json();
	} catch (error) {
		console.error('Error in verifyUserDetails:', error);
		throw error;
	}
}

async function checkStaffStatus() {
	try {
		const csrfToken = await getCSRFToken();
		const accessToken = localStorage.getItem('accessToken'); 

		const response = await fetch(`${baseUrl}/api/check-staff-status/`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken,
				'Authorization': `Bearer ${accessToken}`,
		},
});

		if (!response.ok) {
			const errorData = await response.json();
			throw new Error('Staff status check failed: ' + (errorData.detail || 'Unknown error'));
		}

		return await response.json();
	} catch (error) {
		console.error('Error in checkStaffStatus:', error);
		throw error;
	}
}

export default {
	getCSRFToken,
	checkCSRFToken,
	loginUser,
	resetUserPassword,
	verifyUserDetails,
	checkStaffStatus,
};
