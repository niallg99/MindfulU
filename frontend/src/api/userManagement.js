const baseUrl = `http://${window.location.hostname}:8000`;

const fetchUsers = async (searchQuery) => {
  const url = new URL(`${baseUrl}/api/users/`);
  if (searchQuery) {
    url.searchParams.append('search', searchQuery);
  }

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const usersData = await response.json();
  return usersData;
};


const determineRiskLevel = (userMoods) => {
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  const recentMoods = userMoods.filter(mood => new Date(mood.mood_date) >= thirtyDaysAgo);

  const moodCounts = recentMoods.reduce((counts, mood) => {
    counts[mood.mood_type] = (counts[mood.mood_type] || 0) + 1;
    return counts;
  }, {});

  const totalMoods = recentMoods.length;
  const nonHappyMoods = totalMoods - (moodCounts['Happy'] || 0);

  if (nonHappyMoods / totalMoods >= 0.6) {
    return 'High';
  } else if (nonHappyMoods / totalMoods >= 0.4) {
    return 'Medium';
  } else {
    return 'Low';
  }
};

const calculateAverageMood = (moods) => {
  if (moods.length === 0) {
    return 'N/A'; // Return 'N/A' if there are no moods
  }

  const moodCounts = moods.reduce((counts, mood) => {
    counts[mood.mood_type] = (counts[mood.mood_type] || 0) + 1;
    return counts;
  }, {});

  let mostFrequentMood = '';
  let maxCount = 0;

  for (const mood in moodCounts) {
    if (moodCounts[mood] > maxCount) {
      maxCount = moodCounts[mood];
      mostFrequentMood = mood;
    }
  }

  return mostFrequentMood;
};


export { fetchUsers, determineRiskLevel, calculateAverageMood };