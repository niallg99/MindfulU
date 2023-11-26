const baseUrl = 'http://0.0.0.0:8000';

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
            return response.json().then(data => {
                throw new Error('Registration failed');
            });
        }
        return response.json();
    });
}