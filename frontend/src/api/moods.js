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

const postMood = async (moodData) => {
  try {
    const response = await fetch(`${baseUrl}/api/moods/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.accessToken}`, // Access the accessToken from the component's data
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

export { fetchMoodChoices, postMood };


