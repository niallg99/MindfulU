// Dashboard.vue script section
<script>
import Navbar from './Navbar.vue';
import Footer from './Footer.vue';
import Mood from './Mood.vue';
import Card from './Card.vue';
import EventPanel from './EventPanel.vue'
import { fetchMoodChoices } from '../api/moods.js'; 
import SupportForYou from './SupportForYou.vue';

export default {
  name: 'Dashboard',
  components: {
    Navbar,
    Footer,
    Mood,
    Card,
    EventPanel,
    SupportForYou
},
  data() {
    return {
      moods: [],
      isLoading: true,
      isError: false,
      errorMessage: '',
      cardHeaders: ['Activities', 'Mood History', 'Support', 'Friends']
    };
  },
  async mounted() {
    try {
      this.moods = await fetchMoodChoices();
    } catch (error) {
      this.isError = true;
      this.errorMessage = 'Failed to load moods.';
    } finally {
      this.isLoading = false;
    }
  },
};
</script>
<!-- Dashboard.vue template section -->
<template>
  <Navbar :isLoggedIn="true" :isStaff="isStaff" @update:isStaffLogin="isLoggedIn" />
  
  <div class="container-fluid pt-4 pb-4">
    <div class="row mb-4">
      <div class="col-12 mood-container">
        <Mood 
          v-for="(mood, index) in moods"
          :key="index"
          :mood="mood[0]"
          :selectionCount="mood.count"
        />
      </div>
    </div>
    <div class="row">
      <div class="col-lg-6 col-md-6 col-sm-12 mb-4" v-for="(header, index) in cardHeaders.slice(0, 2)" :key="'top-row-' + index">
        <Card :header="header" :body="'This is the ' + header" />
      </div>
    </div>
    <div class="row">
      <div class="col-lg-6 col-md-6 col-sm-12 mb-4" v-for="(header, index) in cardHeaders.slice(2, 4)" :key="'bottom-row-' + index">
        <Card :header="header" :body="'This is the ' + header" />
      </div>
    </div>
  </div>
  <SupportForYou />
  <Footer />
</template>


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

@media (max-width: 992px) {
  .mood-component,
  .col-lg-6 {
    min-width: 100%; /* Full width on medium and small screens */
  }
}
</style>
