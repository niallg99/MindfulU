export function getAccessToken() {
    // Retrieve the access token from localStorage
  console.log('getAccessToken', localStorage.getItem('accessToken'))
  return localStorage.getItem('accessToken');
}
