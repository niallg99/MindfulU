<template>
	<div class="container mt-4">
		<div class="row justify-content-center">
			<div class="col-lg-12">
				<div class="card panel-card">
					<div class="card-header">
						Friends
					</div>
					<div class="card-body">
						<div v-if="friendRequests.length" class="incoming-requests mb-4">
							<h3>Incoming Friend Requests</h3>
							<ul class="list-group">
								<li v-for="request in friendRequests" :key="request.id" class="list-group-item d-flex justify-content-between align-items-center">
									{{ request.sender }}
									<span>
									<button class="btn btn-success btn-sm" @click="acceptRequest(request.username)">Accept</button>
									<button class="btn btn-danger btn-sm" @click="declineRequest(request.username)">Decline</button>
									</span>
								</li>
							</ul>
						</div>
						<div v-if="showAddFriendModal" class="modal fade show d-block" id="addFriendModal" tabindex="-1" aria-hidden="true">
							<div class="modal-dialog">
								<div class="modal-content">
									<div class="modal-header">
										<h5 class="modal-title" id="addFriendModalLabel">Add a Friend</h5>
										<button type="button" class="btn-close" @click="closeAddFriendModal"></button>
									</div>
									<div class="modal-body">
										<input type="text" class="form-control" placeholder="Enter friend's username" v-model="friendUsername">
									</div>
									<div class="modal-footer">
										<button type="button" class="btn btn-secondary" @click="closeAddFriendModal">Close</button>
										<button type="button" class="btn btn-primary" @click="addFriend">Add Friend</button>
									</div>
								</div>
							</div>
						</div>
						<div class="modal-backdrop fade show" v-if="showAddFriendModal"></div>
						<div v-if="!isLoading && !isError">
							<div class="row">
								<div class="col-md-4 friend-card-container" v-for="friend in limitedFriendsList" :key="friend.id">
									<div class="card friend-card mb-3">
										<div class="card-header text-center">
											<img :src="friend.profilePicture || '/src/images/person.svg'" class="img-fluid rounded-circle" :alt="friend.friend.first_name" style="width: 60px; height: 60px;">
										</div>
										<div class="card-body">
											<h5 class="card-title">Username: @{{ friend.friend.username }}</h5>
											<template v-if="friend.most_recent_mood">
												<img :src="moodImageUrl(friend.most_recent_mood)" alt="Mood Image" class="mood-image"/>
											</template>
										</div>
									</div>
								</div>
								<div class="col-md-4 friend-card-container" v-if="friendsList.length < 3">
									<div class="card friend-card mb-3">
										<div class="card-header text-center">
											<h5 class="card-title">Add a New Friend</h5>
										</div>
										<div class="card-body text-center">
											<p class="card-text">Expand your circle by adding more friends!</p>
											<button class="btn btn-primary" @click="openAddFriendModal">Add Friend</button>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div v-if="isLoading"><spinner /></div>
						<div v-if="isError">{{ errorMessage }}</div>
					</div>
					<div class="card-footer text-center">
						<button class="btn btn-primary" @click="navigateToAllFriends">See All Friends</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { fetchFriends, sendFriendRequest, acceptFriendRequest, rejectFriendRequest, fetchFriendRequests } from '@/api/friends';
import { useRouter } from 'vue-router';
import Spinner from './Spinner.vue';

export default {
	name: 'FriendsPanel',
	setup() {
		const router = useRouter();
		return {
			navigateToAllFriends() {
				router.push('/friends');
			},
		};
	},
	components: {
		Spinner,
	},
	data() {
		return {
			friendsList: [],
			isLoading: true,
			isError: false,
			errorMessage: '',
			showAddFriendModal: false,
			friendUsername: '',
			friendRequests: [],
		};
	},
	computed: {
		limitedFriendsList() {
			return this.friendsList ? this.friendsList.slice(0, 3) : [];
		},
	},
	methods: {
		async loadFriendsData() {
			try {
				this.isLoading = true;
				const friendsData = await fetchFriends();
				this.friendsList = friendsData;
			} catch (error) {
				console.error('Error fetching friends data:', error);
				this.isError = true;
				this.errorMessage = 'Failed to load friends. Please try again later.';
			} finally {
				this.isLoading = false;
			}
		},
		async fetchFriendRequests() {
			try {
				const requests = await fetchFriendRequests();
				this.friendRequests = requests;
			} catch (error) {
				console.error('Error fetching friend requests:', error);
			}
		},
		async acceptRequest(username) {
			try {
				const response = await acceptFriendRequest(username);
				console.log('Accept friend request response:', response);
				await this.fetchFriendRequests();
				await this.loadFriendsData();
			} catch (error) {
				console.error('Error accepting friend request:', error);
			}
		},
		async declineRequest(username) {
			try {
				await rejectFriendRequest(username);
				await this.fetchFriendRequests();
			} catch (error) {
				console.error('Error declining friend request:', error);
			}
		},
		openAddFriendModal() {
			this.showAddFriendModal = true;
		},
		closeAddFriendModal() {
			this.showAddFriendModal = false;
			this.friendUsername = '';
		},
		async addFriend() {
			try {
				await sendFriendRequest(this.friendUsername);
				alert('Friend request sent successfully to ' + this.friendUsername);
				this.closeAddFriendModal();
				// Refresh the list after adding a friend
				await this.loadFriendsData();
			} catch (error) {
				console.error('Error sending friend request:', error);
				alert('Failed to send friend request. Please try again.');
			}
		},
		moodImageUrl(moodType) {
			if (!moodType) return '';
			const moodTypeKey = moodType.split(' ')[0];
			return `/src/images/${moodTypeKey.toLowerCase()}.png`;
		},
	},
	mounted() {
		this.loadFriendsData();
		this.fetchFriendRequests();
	}
};
</script>


<style scoped>
  .friends-container {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .friend-card-container {
    flex: 1 1 30%;
    display: flex;
    flex-direction: column;
  }

  .card.friend-card {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .card-body {
    flex-grow: 1;
    text-align: center;
  }

  .card-footer {
    height: 4rem;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .mood-image {
    width: 40px;
    height: 40px;
    margin-top: 10px;
  }

  @media (max-width: 992px) {
    .friend-card-container {
      flex: 1 1 100%;
    }
  }
</style>

