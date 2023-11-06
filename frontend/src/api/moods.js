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

export { fetchMoodChoices };