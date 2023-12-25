<template>
	<navbar :isLoggedIn="true" :isStaff="isStaff" @update:isStaffLogin="isLoggedIn" @login-success="handleLoginSuccess" />
	<div class="main-container">
		<div class="col-auto padding-top-1">
			<div v-if="broadcastMessage" class="broadcast-message"> 
				<h1>{{ broadcastMessage }}</h1>
			</div>
		</div>
		<div class="welcome-message padding-top-1 padding-bottom-1">
			<div class="row">
				<div class="col-12 col-md-6">
					<h2 class="text-center padding-2">Hi {{ username }}! How are you feeling today?</h2>
					<h3 v-if="userProfile" class="text-center padding-sides-1">Your current mood streak: {{ userProfile.streak_count }} days</h3>
				</div>
				<div class="col-12 col-md-6">
					<div class="text-center">
						<img src="/src/images/mental.svg" alt="Logo" style="width: 200px; height: auto;">
					</div>
				</div>
			</div>
		</div>
		<div class="mood-container padding-top-1">
			<mood 
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
					@friend-request-accepted="handleFriendRequestAccepted"
					@friend-request-declined="handleFriendRequestDeclined"
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
import { fetchMoodChoices, fetchUserMoods, fetchUserProfile } from '../api/moods.js'; 
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
			username: '',
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
  methods: {
		async handleFriendRequestAccepted({ requestId }) {
			this.friendRequests = this.friendRequests.filter(request => request.id !== requestId);
			await this.fetchFriendRequests();
		},
    async handleFriendRequestDeclined(username) {
      this.friendRequests = this.friendRequests.filter(request => request.username !== username);
    },
    async fetchFriendRequests() {
			try {
				this.friendsList = await fetchFriends();
				this.friendRequests = await fetchFriendRequests();
			} catch (error) {
				this.handleError('Error fetching friends data.', error);
			}
			},
    async fetchMoodData() {
      try {
        this.moodChoices = await fetchMoodChoices();
        this.userMoods = await fetchUserMoods(this.userId);
      } catch (error) {
        this.handleError('Failed to load moods.', error);
      }
    },
    async fetchOtherData() {
      try {
        this.broadcastMessage = await getLatestBroadcastMessage();
        this.events = (await fetchEvents()).sort((a, b) => new Date(a.date) - new Date(b.date));
        this.supportSections = await fetchSupport();
      } catch (error) {
        this.handleError('Error fetching other data.', error);
      }
		},
		async fetchUserProfileData() {
      try {
        this.userProfile = await fetchUserProfile(this.username);
      } catch (error) {
        this.handleError('Failed to load user profile.', error);
      }
    },
    handleError(message, error) {
      console.error(message, error);
      this.isError = true;
      this.errorMessage = message;
      this.isLoading = false;
    }
  },
  async mounted() {
		this.userId = localStorage.getItem('userId');
		this.username = localStorage.getItem('username');
		this.isLoading = true;
  	try {
			await Promise.all([
				this.fetchMoodData(),
				this.fetchFriendRequests(),
				this.fetchOtherData(),
				this.fetchUserProfileData(),
    ]);
  } catch (error) {
    this.handleError('An error occurred while fetching data.', error);
  } finally {
    this.isLoading = false;
  }
}


};
</script>