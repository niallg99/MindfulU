<template>
	<div class="container mt-4">
		<div class="row justify-content-center">
			<div class="col-lg-12">
				<div class="card panel-card">
					<div class="card-header">Friends</div>
					<div class="card-body">
						<!-- Incoming Friend Requests Section -->
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
						<div v-if="!isLoading && !isError" class="friends-list-container">
							<div v-for="friend in limitedFriendsList" :key="friend.id" class="friend-card-container mb-3">
								<div class="card friend-card">
									<table class="table-friend">
										<tr>
											<td class="cell-profile-picture">
												<img :src="friend.profilePicture || '/src/images/person.svg'" class="profile-picture" :alt="`Profile picture of ${friend.friend.first_name}`">
											</td>
											<td class="cell-username">
												<h5 class="card-title">@{{ friend.friend.username }}</h5>
											</td>
											<td class="cell-mood">
												<template v-if="friend.most_recent_mood">
													<img :src="moodImageUrl(friend.most_recent_mood)" alt="Mood Image" class="mood-image"/>
												</template>
											</td>
										</tr>
									</table>
								</div>
							</div>
							<div class="friend-card-container" v-if="friendsList.length < 3">
								<div class="card friend-card-add mb-3">
									<div class="card-body text-center">
										<p class="card-text">Expand your circle by adding more friends!</p>
										<button class="btn btn-primary" @click="openAddFriendModal">Add Friend</button>
									</div>
								</div>
							</div>
						</div>
						<div v-if="isLoading">
							<spinner />
						</div>
						<div v-if="isError">
							{{ errorMessage }}
						</div>
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
import { useRouter } from 'vue-router';
import Spinner from './Spinner.vue';
import { acceptFriendRequest, rejectFriendRequest, sendFriendRequest } from '@/api/friends';

export default {
	name: 'FriendsPanel',
	components: {
		Spinner,
	},
	props: {
		friendsList: Array,
		friendRequests: Array,
		isLoading: Boolean,
		isError: Boolean,
		errorMessage: String,
	},
	setup() {
		const router = useRouter();
		return {
			navigateToAllFriends() {
				router.push('/friends');
			},
		};
	},
	computed: {
		limitedFriendsList() {
			return this.friendsList ? this.friendsList.slice(0, 3) : [];
		},
	},
	data() {
		return {
			showAddFriendModal: false,
			friendUsername: '',
		};
	},
	methods: {
		async acceptRequest(username) {
			try {
				await acceptFriendRequest(username);
				this.$emit('update:requests');
			} catch (error) {
				console.error('Error accepting friend request:', error);
				
			}
		},
		async declineRequest(username) {
			try {
				await rejectFriendRequest(username);
				this.$emit('update:requests');
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
				this.$emit('update:requests');
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
};
</script>