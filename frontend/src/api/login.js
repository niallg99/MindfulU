const baseUrl = 'http://0.0.0.0:8000';

export function loginUser(userData) {
    return fetch(`${baseUrl}/api/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error('Login failed: ' + (data.error || 'Unknown error'));
            });
        }
        return response.json();
    });
}

export async function resetUserPassword(email) {
  try {
    const response = await fetch(`${baseUrl}/api/password-reset/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email })
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


