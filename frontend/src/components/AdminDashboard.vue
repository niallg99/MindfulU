<template>
	<div class="admin-dashboard">
		<navbar />
		<stats-overview 
			:average-mood="mostSelectedMood"
			:active-users="activeUsers"
			:most-provided-mood-cause="mostProvidedMoodCause">
		</stats-overview>
		<div class="broadcast-message-admin mt-4">
			<div class="card">
				<h5 class="card-header">Admin Broadcast Message</h5>
				<div class="card-body">
					<textarea class="form-control" v-model="broadcastMessage" placeholder="Enter message to broadcast"></textarea>
					<button class="btn btn-primary mt-3" @click="submitBroadcastMessage">Submit Message</button>
				</div>
			</div>
		</div>
		<div class="mood-analytics">>
		<mood-chart :mood-data="moodStats" />
		</div>
		<user-management 
			:users="users" 
			v-model:searchQuery="searchQuery" 
			@user-clicked="openUserModal"
		/>
		<user-details-modal 
			:user-details="selectedUser"
			:show="showUserModal"
			:phone="phone"
			@close="showUserModal = false"
		/>
	</div>
	<custom-footer />
</template>

<script>
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';
import MoodChart from './MoodChart.vue';
import { fetchUserProfile } from '../api/moods.js'; 
import UserManagement from './UserManagement.vue'
import { saveBroadcastMessage } from '../api/broadcastMessage';
import { fetchMoodStatistics } from '../api/chart';
import { fetchUsers, determineRiskLevel } from '../api/userManagement';
import StatsOverview from './StatsOverview.vue';
import UserDetailsModal from './UserDetailsModal.vue'

export default {
	components: {
		Navbar,
		CustomFooter,
		MoodChart,
		UserManagement,
		StatsOverview,
		UserDetailsModal
	},
	data() {
		return {
			broadcastMessage: '',
			searchQuery: '',
			moodStats: [],
			users: [],
			userProfile: {},
			selectedUser: null,
			showUserModal: false
		};
	},
	computed: {
		paginatedUsers() {
			const start = (this.currentPage - 1) * this.pageSize;
			const end = start + this.pageSize;
			return this.filteredUsers.slice(start, end);
		},
		 mostSelectedMood() {
			const moodCount = {};
			this.users.forEach(user => {
				user.moods.forEach(mood => {
					const moodType = mood.mood_type;
					if (moodType) {
						moodCount[moodType] = (moodCount[moodType] || 0) + 1;
					}
				});
			});
			let mostSelected = null;
			let maxCount = 0;
			for (const [moodType, count] of Object.entries(moodCount)) {
				if (count > maxCount) {
					mostSelected = moodType;
					maxCount = count;
				}
			}
			return mostSelected || 'N/A';
		},
	  activeUsers() {
      const oneWeekAgo = new Date();
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 30);
      return this.users.filter(user => 
        user.moods.some(mood => new Date(mood.mood_date) >= oneWeekAgo)
      ).length;
    },
    mostProvidedMoodCause() {
			const moodCauseCount = {};
			this.users.forEach(user => {
				user.moods.forEach(mood => {
					if (mood.mood_cause) {
						moodCauseCount[mood.mood_cause] = (moodCauseCount[mood.mood_cause] || 0) + 1;
					}
				});
			});
			const sortedMoodCauses = Object.entries(moodCauseCount).sort((a, b) => b[1] - a[1]);
			return sortedMoodCauses.length ? sortedMoodCauses[0][0] : 'N/A';
		},
		moodCauseStats() {
			const moodCauseCount = {};
			this.users.forEach(user => {
				user.moods.forEach(mood => {
					if (mood.mood_cause) {
						moodCauseCount[mood.mood_cause] = (moodCauseCount[mood.mood_cause] || 0) + 1;
					}
				});
			});
			return Object.entries(moodCauseCount).map(([cause, count]) => ({ cause, count }));
		},
  },
	methods: {
		async submitBroadcastMessage() {
			try {
				const response = await saveBroadcastMessage(this.broadcastMessage);
				console.log(response.message);
			} catch (error) {
				console.error('Error submitting broadcast message:', error);
			}
		},
		async fetchUsers() {
			try {
				const usersData = await fetchUsers();
				this.users = usersData.map(user => {
					const riskLevel = determineRiskLevel(user.moods);
					const mostSelectedMood = this.mostSelectedMood;
					const lastMoodDate = user.moods.length > 0 ? new Date(user.moods[user.moods.length - 1].mood_date).toLocaleDateString() : 'N/A';
					return { ...user, riskLevel, mostSelectedMood, lastMoodDate };
				});
			} catch (error) {
				console.error('Error fetching users:', error);
			}
		},
		openUserModal(user) {
				console.log("Selected user:", user);
				this.selectedUser = user;
				this.resetModal();
				this.fetchUserProfileData(user.username);
		},
		async fetchUserProfileData(username) {
				try {
						const userProfileData = await fetchUserProfile(username);
						this.phone = userProfileData.phone || 'No phone number available';
						this.showUserModal = true;
				} catch (error) {
						console.error('Failed to load user profile:', error);
						this.phone = 'Failed to load phone number';
						this.showUserModal = true;
				}
		},
		resetModal() {
				this.phone = '';
				this.showUserModal = false;
		},
	},
	async mounted() {
		try {
				this.moodStats = await fetchMoodStatistics();
				await this.fetchUsers();
		} catch (error) {
				console.error('Error:', error);
		}
	}
};
</script>

<style>
.admin-dashboard {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}

.broadcast-message {
	display: flex;
	justify-content: center;
	margin: 0 auto;
	width: 90%;
}

.custom-footer {
	width: 100%;
}

body {
	margin: 0;
}
</style>
