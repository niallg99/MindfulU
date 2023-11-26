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

const updateMood = async (moodId, moodData) => {
  try {
    const accessToken = getAccessToken(); // Retrieve the access token
    const url = `${baseUrl}/api/moods/${moodId}/`;

    const response = await fetch(url, {
      method: 'PATCH', // or 'PUT', depending on your API
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(moodData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const updatedMood = await response.json();
    return updatedMood;
  } catch (error) {
    console.error("Could not update mood:", error);
    throw error;
  }
};


const fetchUserMoods = async (userId) => {
  try {
    const accessToken = getAccessToken();
    const response = await fetch(`${baseUrl}/api/user-moods/${userId}`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const userMoods = await response.json();
    return userMoods;
  } catch (error) {
    console.error("Could not fetch user moods:", error);
    throw error;
  }
};

const deleteMood = async (moodId) => {
  try {
    const response = await fetch(`[Your API Endpoint]/moods/${moodId}`, {
      method: 'DELETE',
      headers: {
        // Add necessary headers, e.g., for authorization
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return true; // Return true on successful deletion
  } catch (error) {
    console.error("Could not delete mood:", error);
    throw error;
  }
};

export { fetchMoodChoices, fetchMoodCauses, postMood, fetchUserMoods, updateMood, deleteMood};

