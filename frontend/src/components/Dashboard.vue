<template>
	<navbar :isLoggedIn="true" :isStaff="isStaff" @update:isStaffLogin="isLoggedIn" @login-success="handleLoginSuccess" />
	<div class="main-container">
		<div class="padding-top-1">
			<div v-if="broadcastMessage"
				class="broadcast-message"
			>
				{{ broadcastMessage }}
			</div>
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
				<event-panel
					:events="events"
					:is-loading="isLoading"
					:is-error="isError"
					:error-message="errorMessage"
				/>
			</div>
			<div class="panel">
				<support-panel
					:support-sections="supportSections"
					:is-loading="isLoading"
				/>
			</div>
			<div class="panel">
				<mood-history-panel
					:user-moods="userMoods"
				/>
			</div>
			<div class="panel">
				<friends-panel 
					:friends-list="friendsList" 
					:friend-requests="friendRequests" 
					:is-loading="isLoading"
				/>
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
import { fetchEvents } from '@/api/events';
import { fetchSupport } from '@/api/supportforyou.js';
import { fetchFriends, fetchFriendRequests } from '@/api/friends';


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
			events: [],
			supportSections: [],
			friendsList: [],
			friendRequests: [],
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
		try {
			const eventsData = await fetchEvents();
			this.events = eventsData.sort((a, b) => new Date(a.date) - new Date(b.date));
		} catch (error) {
			console.error('There was a problem fetching the events:', error);
			this.isError = true;
			this.errorMessage = 'Failed to load events.';
		} finally {
			this.isLoading = false;
		}
		try {
			const supportData = await fetchSupport();
			this.supportSections = supportData;
		} catch (error) {
			console.error('Error fetching support data:', error);
		} finally {
			this.isLoading = false;
		}
		try {
			const friendsData = await fetchFriends();
			this.friendsList = friendsData;
			const requestsData = await fetchFriendRequests();
			this.friendRequests = requestsData;
		} catch (error) {
			console.error('Error fetching friends data:', error);
		} finally {
			this.isLoading = false;
		}
	},
};
</script>
