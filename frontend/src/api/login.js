const baseUrl = 'http://0.0.0.0:8000';

const getCSRFToken = async () => {
	try {
		const response = await fetch(`${baseUrl}/api/get-csrf-token/`);
		console.log(response, 'responseS')
		console.log(baseUrl, 'baseUrl')

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

export function loginUser(userData) {
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

export async function resetUserPassword(email) {
	try {
		const csrfToken = await getCSRFToken();

		const response = await fetch(`${baseUrl}/api/password-reset/`, {
				method: 'POST',
				headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': csrfToken,
				},
				body: JSON.stringify({ email }),
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

		const data = await response.json();
		return data;
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

async function changeUserPassword(userData) {
  try {
    const csrfToken = await getCSRFToken();

    const response = await fetch(`${baseUrl}/api/change-user-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error('Password change failed: ' + (errorData.error || 'Unknown error'));
    }

    return await response.json();
  } catch (error) {
    console.error('Error in changeUserPassword:', error);
    throw error;
  }
}

export default {
	getCSRFToken,
	checkCSRFToken,
	loginUser,
	resetUserPassword,
	verifyUserDetails,
	changeUserPassword
};
