<template>
	<div class="page-container">
			<navbar :is-logged-in="isLoggedIn" />
			<div class="container mt-4">
			<div class="row">
				<template v-if="friendsList && friendsList.length">
					<div class="col-md-4" v-for="friendship in friendsList" :key="friendship.id">
						<div class="card friend-card mb-3">
							<div class="card-body">
								<div class="row align-items-center">
									<div class="col-auto">
										<img 
											:src="getProfilePicture(friendship.friend)" 
											class="img-fluid rounded-circle" 
											:alt="`${friendship.friend.first_name} ${friendship.friend.last_name}`" 
											style="width: 60px; height: 60px;"
										>
									</div>
									<div class="col">
										<h5 class="card-title">
											@{{ friendship.friend.username }}
										</h5>
										<p class="card-text">
											{{ friendship.friend.first_name }}
										</p>
										<template v-if="friendship.most_recent_mood">
											Mood: <img :src="getMoodImageUrl(friendship.most_recent_mood)" class="mood-image" />
										</template>
									</div>
									<div class="col-auto">
										<button class="btn btn-danger" @click="removeFriend(friendship.friend.username)">
											Remove
										</button>
									</div>
								</div>
							</div>
						</div>
					</div>
				</template>
				<div v-if="showAddFriendModal" class="modal fade show d-block" tabindex="-1" aria-hidden="true">
					<div class="modal-dialog">
						<div class="modal-content">
							<div class="modal-header">
								<h5 class="modal-title">Add a Friend</h5>
								<button type="button" class="btn-close" @click="modalToggle"></button>
							</div>
							<div class="modal-body">
								<input type="text" class="form-control" placeholder="Enter friend's username" v-model="friendUsername">
							</div>
							<div class="modal-footer">
								<button type="button" class="btn btn-secondary" @click="modalToggle">Close</button>
								<button type="button" class="btn btn-primary" @click="addFriend">Add Friend</button>
							</div>
						</div>
					</div>
				</div>
				<template v-else>
					<div class="col-12">
						<div class="card text-center">
							<div class="card-body padding-top-1 padding-bottom-1">
								<p>Start connecting!</p>
								<button class="btn btn-primary" @click="modalToggle">Add Friend</button>
							</div>
						</div>
					</div>
				</template>
			</div>
			<nav aria-label="Page navigation" v-if="totalPages > 1">
				<ul class="pagination justify-content-center">
					<li class="page-item" :class="{ disabled: currentPage === 1 }">
						<a class="page-link" href="#" aria-label="Previous" @click.prevent="changePage(currentPage - 1)">
							<span aria-hidden="true">&laquo;</span>
						</a>
					</li>
					<li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
						<a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
					</li>
					<li class="page-item" :class="{ disabled: currentPage === totalPages }">
						<a class="page-link" href="#" aria-label="Next" @click.prevent="changePage(currentPage + 1)">
							<span aria-hidden="true">&raquo;</span>
						</a>
					</li>
				</ul>
			</nav>
		</div>
		<custom-footer />
	</div>
</template>


<script>
import { fetchFriends, sendFriendRequest, acceptFriendRequest, rejectFriendRequest, fetchFriendRequests, removeFriend} from '@/api/friends';
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';

export default {
	name: 'Friends',
	components: {
		Navbar,
		CustomFooter,
	},
	data() {
		return {
			friendsList: [],
			isLoading: false,
			isError: false,
			errorMessage: '',
			currentPage: 1,
			pageSize: 25,
			showAddFriendModal: false,
			friendUsername: '',
			friendRequests: [],
		};
	},
	computed: {
		totalPages() {
			return Math.ceil(this.friendsList.length / this.pageSize);
		},
		paginatedFriendsList() {
			const start = (this.currentPage - 1) * this.pageSize;
			const end = start + this.pageSize;
			return this.friendsList.slice(start, end);
		},
	},
	methods: {
		async loadFriendsData() {
			this.isLoading = true;
			try {
				const data = await fetchFriends();
				this.friendsList = data;
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
		async acceptRequest(requestId) {
			try {
				await acceptFriendRequest(requestId);
				await this.fetchFriendRequests();
				await this.loadFriendsData();
			} catch (error) {
				console.error('Error accepting friend request:', error);
			}
		},
		async declineRequest(requestId) {
			try {
				await rejectFriendRequest(requestId);
				await this.fetchFriendRequests();
			} catch (error) {
				console.error('Error declining friend request:', error);
			}
		},
		async addFriend() {
			try {
				await sendFriendRequest(this.friendUsername);
				alert('Friend request sent successfully to ' + this.friendUsername);
				this.modalToggle();
				await this.loadFriendsData();
			} catch (error) {
				console.error('Error sending friend request:', error);
				alert('Failed to send friend request. Please try again.');
			}
		},
		async removeFriend(username) {
			try {
				const response = await removeFriend(username);
				if (response.success) {
					this.friendsList = this.friendsList.filter(f => f.username !== username);
					alert('Friend removed successfully.');
				}
			} catch (error) {
				console.error('Error removing friend:', error);
				alert('Failed to remove friend. Please try again.');
			}
		},
		modalToggle() {
			this.showAddFriendModal = !this.showAddFriendModal;
		},
		changePage(page) {
			if (page < 1 || page > this.totalPages) {
				return;
			}
			this.currentPage = page;
		},
		getProfilePicture(friend) {
			return friend.profile_picture || 'src/images/person.svg';
		},
		getMood(mostRecentMood) {
			return mostRecentMood.split(' ')[0];
		},
		getMoodImageUrl(mostRecentMood) {
			const moodType = this.getMood(mostRecentMood);
			return `/src/images/${moodType.toLowerCase()}.png`;
		},
	},
	mounted() {
		this.loadFriendsData();
		this.fetchFriendRequests();
	}
};
</script>




<style scoped>
.page-container {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}

.container {
	flex: 1;
	padding-top: 1rem;
}

.friend-card .card-body {
	padding: 1rem;
}

.friend-card img {
	width: 100%;
	object-fit: cover;
}

.friend-card .card-title {
	margin-bottom: 0.5rem;
}

.pagination {
	display: flex;
	justify-content: center;
	margin-top: 1rem;
}

.custom-footer {
	margin-top: auto;
}

.friend-card .btn-danger {
	margin-top: 10px;
}

.mood-image {
	max-width: 24px;
	max-height: 24px;
}

</style>