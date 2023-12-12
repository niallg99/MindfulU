const baseUrl = `http://${window.location.hostname}:8000`;

export function registerUser(userData, csrfToken) {
    return fetch(`${baseUrl}/api/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            return { success: true, data };
        } else {
            return { success: false, message: data.message || 'Registration failed.' };
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        return { success: false, message: error.message };
    });
}
