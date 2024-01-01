<template>
	<nav class="navbar navbar-expand-lg navbar-custom">
		<div class="container-fluid">
			<template v-if="isLoggedIn">
				<router-link to="/dashboard" class="navbar-brand">MindfulU</router-link>
			</template>
			<template v-else>
				<a class="navbar-brand" href="#">MindfulU</a>
			</template>
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" @click="toggleNavbarCollapse">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div v-if="isLoggedIn"
				class="collapse navbar-collapse" id="navbarSupportedContent">
				<ul class="navbar-nav ms-auto mb-2 mb-lg-0">
					<li class="nav-item">
						<router-link to="/dashboard" class="nav-link">Home</router-link>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="#" @click="openProfileModal">Profile</a>
					</li>
					<li class="nav-item">
						<router-link to="/events" class="nav-link">Events</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/support" class="nav-link">Support</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/friends" class="nav-link">Friends</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/mood-history" class="nav-link">Mood History</router-link>
					</li>
					<li v-if="isLoggedIn && isStaff" class="nav-item">
						<router-link to="/admin_dashboard" class="nav-link">Admin</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/login" class="nav-link">Logout</router-link>
					</li>
					<li v-if="!isLoggedIn" class="nav-item">
						<router-link to="/login" class="nav-link">Login</router-link>
					</li>
					<li v-else class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="notificationsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
						<img src="/src/images/bell.svg" alt="Notifications" class="notification-icon"> <!-- Added class -->
						<span v-if="friendRequests.length">({{ friendRequests.length }})</span>
					</a>
					<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationsDropdown">
						<li v-for="request in friendRequests" :key="request.id" class="dropdown-item d-flex justify-content-between notification-item"> <!-- Added class -->
							{{ request.sender }} wants to be friends.
							<span>
								<button @click="acceptRequest(request.id)">✓</button>
								<button @click="declineRequest(request.id)">✗</button>
							</span>
						</li>
						<li v-if="!friendRequests.length">
							<a class="dropdown-item" href="#">No new notifications</a>
						</li>
					</ul>
				</li>
					<!-- /** Used for testing and easy navigation while developing */ -->
					<!-- <li class="nav-item dropdown">
						<a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
							Pages
						</a>
						<ul class="dropdown-menu" aria-labelledby="pagesDropdown">
							<li v-for="route in router.getRoutes()" :key="route.path">
								<router-link :to="route.path" class="dropdown-item">{{ route.name }}</router-link>
							</li>
						</ul>
					</li> -->
				</ul> 
			</div>
		</div>
	</nav>
	 <profile-modal
  ref="profileModalRef"
  :userProfilePicture="userProfilePicture"
  :showMood="showMood"
  @update:showMood="handleShowMoodUpdate"
  @profile-updated="handleProfileUpdated"
/>

</template>


<script>
import { fetchFriendRequests, acceptFriendRequest, rejectFriendRequest } from '@/api/friends';
import { fetchUserProfile } from '../api/moods.js';
import APILogin from '@/api/login.js';
import ProfileModal from './ProfileModal.vue';
import router from '../router';

export default {
	name: 'Navbar',
	components: {
		ProfileModal,
	},
	data() {
		return {
			notifications: [],
			friendRequests: [],
			router: router,
			isStaff: false,
			showMood: localStorage.getItem('showMood') === 'true',
			userProfilePicture: localStorage.getItem('userProfilePicture') || '/src/images/person.svg',
		};
	},
	computed: {
		isLoggedIn() {
			return !!localStorage.getItem('accessToken');
		},
		username() { 
      return localStorage.getItem('username');
		},
	},
	methods: {
		async fetchFriendRequests() {
			try {
				const requests = await fetchFriendRequests();
				this.friendRequests = requests;
			} catch (error) {
				throw new Error('Error fetching friend requests:', error);
			}
		},
		async acceptRequest(username) {
			try {
				const response = await acceptFriendRequest(username);
				console.log('Accept friend request response:', response);
				await this.fetchFriendRequests();
				await this.loadFriendsData();
			} catch (error) {
				throw new Error('Error accepting friend request:', error);
			}
		},
		async declineRequest(username) {
			try {
				await rejectFriendRequest(username);
				await this.fetchFriendRequests();
			} catch (error) {
				throw new Error('Error declining friend request:', error);
			}
		},
		async fetchStaffStatus() {
			try {
				const response = await APILogin.checkStaffStatus();
				this.isStaff = response.is_staff;
			} catch (error) {
				throw new Error('Error fetching staff status:', error);
			}
		},
		logout() {
			localStorage.removeItem('accessToken');
			localStorage.removeItem('username');
			localStorage.removeItem('userProfilePicture');
			this.$router.push('/login');
		},
		toggleNavbar() {
			const navbarCollapse = this.$refs.navbarCollapse;
			navbarCollapse.classList.toggle('show');
		},
		toggleNavbarCollapse() {
			const navbarCollapse = document.getElementById('navbarSupportedContent');
			const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
				toggle: false
			});
			bsCollapse.toggle();
		},
		async fetchAndSetUserProfile() {
			if (!this.isLoggedIn || !this.username) {
				return;
			}
			try {
				const userData = await fetchUserProfile(this.username);
				this.userProfilePicture = userData.picture || '/src/images/person.svg';
				localStorage.setItem('userProfilePicture', this.userProfilePicture);
			} catch (error) {
				throw new Error('Error fetching user profile:', error);
			}
		},
		handleProfileUpdated(newProfilePictureUrl) {
			this.userProfilePicture = newProfilePictureUrl;
			localStorage.setItem('userProfilePicture', newProfilePictureUrl);
		},
		async openProfileModal() {
			if (!this.isLoggedIn || !this.username) {
				return;
			}
			try {
				await this.fetchAndSetUserProfile();
				if (this.$refs.profileModalRef) {
					this.$refs.profileModalRef.show();
				}
			} catch (error) {
				throw new Error('Error fetching user profile:', error);
			}
		},
     handleShowMoodUpdate(newShowMoodValue) {
      this.showMood = newShowMoodValue;
      localStorage.setItem('showMood', newShowMoodValue);
    }
  },
	mounted() {
		if (this.isLoggedIn) {
			Promise.all([
				this.fetchStaffStatus(),
				this.fetchFriendRequests(),
				this.fetchAndSetUserProfile(),
			]);
		}
		const dropdownElements = document.querySelectorAll('.dropdown-toggle');
		dropdownElements.forEach(dropdown => {
			new bootstrap.Dropdown(dropdown);
		});
	},
};
</script>