<template>
  <div class="mood-history">
    <h1>Mood History</h1>
    
    <!-- Date Picker -->
    <DatePicker v-model="selectedDate" :max-date="new Date()" />

    <!-- Display moods -->
    <div class="mood-list">
      <div class="mood-item" v-for="mood in filteredMoods" :key="mood.id">
        <h3>{{ mood.mood_type }}</h3>
        <p>Date: {{ mood.mood_date }}</p>
        <p>Description: {{ mood.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchUserMoods } from '@/api/moods';
import DatePicker from 'vue-datepicker';

export default {
  name: 'MoodHistory',
  components: { DatePicker },
  data() {
    return {
      moods: [],
      selectedDate: new Date(),
    };
  },
  computed: {
    filteredMoods() {
      const selectedDateString = this.selectedDate.toISOString().split('T')[0];
      return this.moods.filter(mood => mood.mood_date.startsWith(selectedDateString));
    },
  },
  methods: {
    async loadMoods() {
      try {
        const userId = localStorage.getItem('userId');
        if (userId) {
          const response = await fetchUserMoods(userId);
          this.moods = response.filter(mood => {
            // Filter moods for the last 7 days
            const moodDate = new Date(mood.mood_date);
            const sevenDaysAgo = new Date();
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
            return moodDate >= sevenDaysAgo;
          });
        }
      } catch (error) {
        console.error('Error fetching mood data:', error);
      }
    },
  },
  mounted() {
    this.loadMoods();
  },
};
</script>

<style scoped>
.mood-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
