import { getAccessToken } from '@/api/auth'; // Import the getAccessToken function
const baseUrl = 'http://0.0.0.0:8000';

const fetchMoodChoices = async () => {
  try {
    const response = await fetch(`${baseUrl}/api/mood-choices/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const moodChoices = await response.json();
    return moodChoices;
  } catch (error) {
    console.error("Could not fetch mood choices:", error);
    throw error;
  }
};

const fetchMoodCauses = async () => {
  try {
    const response = await fetch(`${baseUrl}/api/get-mood-causes/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const moodCauses = await response.json();
    return moodCauses;
  } catch (error) {
    console.error("Could not fetch mood causes:", error);
    throw error;
  }
};

const postMood = async (moodData) => {
  try {
    const accessToken = getAccessToken(); // Call getAccessToken to retrieve the access token
    console.log('Access Token:', accessToken); // Add this line to print the access token
    const tokenPayload = JSON.parse(atob(accessToken.split('.')[1]));
    console.log('Token Payload:', tokenPayload);
    const response = await fetch(`${baseUrl}/api/moods/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(moodData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const newMood = await response.json();
    return newMood;
  } catch (error) {
    console.error("Could not post mood:", error);
    throw error;
  }
};

export { fetchMoodChoices, fetchMoodCauses, postMood };
