<template>
  <navbar :isLoggedIn="true" :isStaff="isStaff" @update:isStaffLogin="isLoggedIn" @login-success="handleLoginSuccess" />
  <div class="container-fluid pt-4 pb-4">
    <div class="row mb-4">
      <div class="col-12 mood-container">
        <Mood 
          v-for="(mood, index) in moodChoices"
          :key="index"
          :mood="mood[0]"
          :user-id="userId || ''"
        />
      </div>
    </div>
  </div>
  <div class="container-fluid">
    <div class="row justify-content-center">
      <div class="col-lg-6 col-md-8 col-sm-12 mb-4">
				<event-panel />
      </div>
      <div class="col-lg-6 col-md-8 col-sm-12 mb-4">
        <support-panel />
      </div>
    </div>
  </div>
  <mood-history-panel :user-moods="userMoods" />
	<support-for-you />
	<mood-history />	
  <custom-footer />
</template>

<script>
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';
import Mood from './Mood.vue';
import { fetchMoodChoices, fetchUserMoods } from '../api/moods.js'; 
import SupportForYou from './SupportForYou.vue';
import MoodHistoryPanel from './MoodHistoryPanel.vue';
import EventPanel from './EventPanel.vue';
import SupportPanel from './SupportPanel.vue';
import MoodHistory from './MoodHistory.vue';

export default {
  name: 'Dashboard',
  components: {
    Navbar,
    Mood,
    SupportForYou,
    CustomFooter,
    MoodHistoryPanel,
		EventPanel,
		SupportPanel,
		MoodHistory,
},
  data() {
    return {
      userId: null, 
      moodChoices: [],
      userMoods: [],
      isLoading: true,
      isError: false,
      errorMessage: '',
    };
  },
  async mounted() {
    this.userId = localStorage.getItem('userId');
    try {
      this.moodChoices = await fetchMoodChoices();
      this.userMoods = await fetchUserMoods(this.userId);
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
.mood-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: stretch;
  gap: 1rem;
}

.mood-component {
  flex-grow: 1;
  min-width: 250px;
}

/* Style for the SupportForYou container */
.container-fluid:last-child {
  margin-top: 2rem; /* Adjust the top margin as needed */
  margin-bottom: 2rem; /* Adjust the bottom margin as needed */
}

/* Adjust the width of the SupportForYou component on smaller screens if needed */
@media (max-width: 576px) {
  .col-md-8 {
    min-width: 100%; /* Full width on extra small screens */
  }
}
@media (max-width: 992px) {
  .mood-component,
  .col-lg-6 {
    min-width: 100%; /* Full width on medium and small screens */
  }
}
</style>
