const baseUrl = 'http://0.0.0.0:8000';

// Function to fetch the CSRF token from the server
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

// Function to check if the CSRF token is valid
const checkCSRFToken = async () => {
  try {
    const csrfToken = await getCSRFToken();
    return csrfToken;
  } catch (error) {
    console.error('Error checking CSRF token:', error);
    throw error;
  }
};

// Function to log in a user
export function loginUser(userData) {
  return checkCSRFToken()
    .then(csrfToken => {
      return fetch(`${baseUrl}/api/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Include the CSRF token in the headers
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

// Function to reset a user's password
export async function resetUserPassword(email) {
  try {
    const csrfToken = await getCSRFToken(); // Fetch CSRF token

    const response = await fetch(`${baseUrl}/api/password-reset/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include the CSRF token in the headers
        },
        body: JSON.stringify({ email }),
    });

    if (!response.ok) {
      if (response.headers.get("content-type")?.includes("application/json")) {
        const errorData = await response.json();
        throw new Error('Password reset failed: ' + (errorData.error || 'Unknown error'));
      } else {
        // Here you can handle non-JSON responses, maybe the response is plain text
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

export default {
  getCSRFToken,
  checkCSRFToken,
  loginUser,
  resetUserPassword,
};
