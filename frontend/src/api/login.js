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
