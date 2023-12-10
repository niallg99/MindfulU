<template>
	<navbar :isLoggedIn="true" :isStaff="isStaff" @update:isStaffLogin="isLoggedIn" @login-success="handleLoginSuccess" />
	<div class="main-container">
		<div v-if="broadcastMessage" class="broadcast-message">
      {{ broadcastMessage }}
    </div>
		<div class="mood-container">
			<Mood 
				v-for="(mood, index) in moodChoices"
				:key="index"
				:mood="mood[0]"
				:user-id="userId || ''"
			/>
		</div>
		<div class="panels-container">
			<div class="panel">
				<event-panel />
			</div>
			<div class="panel">
				<support-panel />
			</div>
			<div class="panel">
				<mood-history-panel :user-moods="userMoods" />
			</div>
			<div class="panel">
				<friends-panel />
		</div>
		</div>
	</div>
	<custom-footer />
</template>

<script>
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';
import Mood from './Mood.vue';
import { fetchMoodChoices, fetchUserMoods } from '../api/moods.js'; 
import MoodHistoryPanel from './MoodHistoryPanel.vue';
import EventPanel from './EventPanel.vue';
import SupportPanel from './SupportPanel.vue';
import FriendsPanel from './FriendsPanel.vue';
import { getLatestBroadcastMessage } from '../api/broadcastMessage.js';


export default {
	name: 'Dashboard',
	components: {
		Navbar,
		Mood,
		CustomFooter,
		MoodHistoryPanel,
		EventPanel,
		SupportPanel,
		FriendsPanel,
},
	data() {
		return {
			userId: null, 
			moodChoices: [],
			userMoods: [],
			isLoading: true,
			isError: false,
			errorMessage: '',
			broadcastMessage: '',
		};
	},
	async mounted() {
		this.userId = localStorage.getItem('userId');
		try {
			this.moodChoices = await fetchMoodChoices();
			this.userMoods = await fetchUserMoods(this.userId);
			this.broadcastMessage = await getLatestBroadcastMessage();
		} catch (error) {
			this.isError = true;
			this.errorMessage = 'Failed to load moods.';
		} finally {
			this.isLoading = false;
		}
	},
};
</script>

<style scoped>
.main-container {
	max-width: 80%;
	margin: auto;
	padding-bottom: 3rem;
}

.broadcast-message {
  background-color: #f8d7da; /* Example background color */
  color: #721c24; /* Example text color */
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 0.25rem;
  text-align: center;
}

.mood-container {
	padding: 2rem 0;
	display: flex;
	flex-wrap: wrap;
	justify-content: space-around;
	gap: 1rem;
}

.panel {
	flex: 1 1 50%;
	max-width: 50%;
}

.panels-container {
	display: flex;
	flex-wrap: wrap;
	margin-top: 2rem;
}

@media (max-width: 992px) {
	.panel {
		max-width: 100%;
	}
}
</style>
