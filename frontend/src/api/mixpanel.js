import mixpanel from 'mixpanel-browser';
import { getAccessToken } from '@/api/auth';

mixpanel.init('5c38781066bb02a9e39b83e91e8e7639');

export const trackEvent = (event_name, data) => {
  mixpanel.track(event_name, data);
};


export const trackEventBackend = async (event_name, data) => {
  const accessToken = getAccessToken();
  try {
    const response = await fetch('/api/track-event/', {
      method: 'POST',
      headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ event_name, data }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending event to backend:', error);
  }
};
