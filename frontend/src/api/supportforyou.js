const baseUrl = 'http://0.0.0.0:8000';

export function fetchSupport() {
    return fetch(`${baseUrl}/api/custom_support_links/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}
