import { getAccessToken } from '@/api/auth';

const baseUrl = 'http://0.0.0.0:8000';

const fetchFriends = async (userId) => {
  try {
    console.log('Fetching friends for user ID:', userId);
    const accessToken = getAccessToken();
    const url = `${baseUrl}/api/friends/${userId}`;

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const friendsData = await response.json();
    console.log('Friends data received:', friendsData);
    return friendsData;
  } catch (error) {
    console.error("Could not fetch friends:", error);
    throw error;
  }
};

const sendFriendRequest = async (username) => {
  try {
    const accessToken = getAccessToken();
    const response = await fetch(`${baseUrl}/api/send-friend-request/${username}/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Could not send friend request:", error);
    throw error;
  }
};

const acceptFriendRequest = async (friendId) => {
  try {
    const accessToken = getAccessToken();
    const response = await fetch(`${baseUrl}/api/accept-friend-request/${friendId}/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Could not accept friend request:", error);
    throw error;
  }
};

const rejectFriendRequest = async (friendId) => {
  try {
    const accessToken = getAccessToken();
    const response = await fetch(`${baseUrl}/api/reject-friend-request/${friendId}/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Could not reject friend request:", error);
    throw error;
  }
};

const removeFriend = async (friendId) => {
  try {
    const accessToken = getAccessToken();
    const response = await fetch(`${baseUrl}/api/remove-friend/${friendId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Could not remove friend:", error);
    throw error;
  }
};

export { fetchFriends, sendFriendRequest, acceptFriendRequest, rejectFriendRequest, removeFriend };
