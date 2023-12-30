import { getAccessToken } from '@/api/auth';

const baseUrl = `http://${window.location.hostname}:8000`;

const fetchFriends = async () => {
	try {
		const accessToken = getAccessToken();
		if (!accessToken) {
			throw new Error('Access token is missing or invalid');
		}
		const url = `${baseUrl}/api/friends/`;
		const response = await fetch(url, {
			headers: {
				'Authorization': `Bearer ${accessToken}`,
			},
		});
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		const friendsData = await response.json();
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
		console.log(response,'response')
		if (!response.ok) {
			const errorBody = await response.json();
			throw new Error(`HTTP error ${response.status}: ${errorBody.error || 'Unknown error'}`);
		}
		return await response.json();
	} catch (error) {
			throw new Error('Could not send friend request');
	}
};


const acceptFriendRequest = async (username) => {
	try {
		const accessToken = getAccessToken();
		const response = await fetch(`${baseUrl}/api/accept-friend-request/${username}/`, {
				method: 'POST',
				headers: {
						'Authorization': `Bearer ${accessToken}`,
				},
		});
		if (!response.ok) {
				const errorBody = await response.json();
				console.error('Error response:', errorBody);
				throw new Error(`HTTP error ${response.status}: ${errorBody.detail || 'Unknown error'}`);
		}
		return await response.json();
} catch (error) {
		console.error("Could not accept friend request:", error);
		throw error;
}
};



const rejectFriendRequest = async (username) => {
		try {
			const accessToken = getAccessToken();
			const response = await fetch(`${baseUrl}/api/reject-friend-request/${username}/`, {
				method: 'POST',
				headers: {
					'Authorization': `Bearer ${accessToken}`,
					},
			});
			if (!response.ok) {
				const errorBody = await response.json();
				throw new Error(`HTTP error ${response.status}: ${errorBody.detail || 'Unknown error'}`);
			}
			return await response.json();
	} catch (error) {
			throw new Error('Could not reject friend request', error);
	}
};


const removeFriend = async (username) => {
	try {
		const accessToken = getAccessToken();
		const response = await fetch(`${baseUrl}/api/remove-friend/${username}/`, {
			method: 'DELETE',
			headers: {
					'Authorization': `Bearer ${accessToken}`,
				},
		});
		if (!response.ok) {
			const errorBody = await response.json();
			throw new Error(`HTTP error ${response.status}: ${errorBody.detail || 'Unknown error'}`);
		}
		return await response.json();
	} catch (error) {
			throw new Error('Could not remove friend');
	}
};


const fetchFriendRequests = async () => {
	try {
		const accessToken = getAccessToken();
		if (!accessToken) {
			throw new Error('Access token not found');
		}
		const url = `${baseUrl}/api/friend-requests/`;
		const response = await fetch(url, {
			headers: {
				'Authorization': `Bearer ${accessToken}`,
			},
		});
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		const requestsData = await response.json();
		return requestsData;
	} catch (error) {
		console.error("Could not fetch friend requests:", error);
		throw error;
	}
};

export {
	fetchFriends,
	sendFriendRequest,
	acceptFriendRequest,
	rejectFriendRequest,
	removeFriend,
	fetchFriendRequests
};
