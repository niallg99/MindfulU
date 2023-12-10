export function getAccessToken() {
  console.log('getAccessToken', localStorage.getItem('accessToken'))
  return localStorage.getItem('accessToken');
}
