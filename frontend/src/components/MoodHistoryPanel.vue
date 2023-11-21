<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-header">
            Recent Mood
          </div>
          <div class="card-body">
            <div v-if="isLoading">
              <Spinner /> Loading mood history...
            </div>
            <div v-else-if="isError">
              {{ errorMessage }}
            </div>
            <div v-else>
              <div v-if="userMoods.length > 0" class="mood-card-container">
                <!-- Display only the most recent mood -->
                <div class="mb-3">
                  <img :src="moodImageUrl(userMoods[0].mood_type)" class="card-img-top" :alt="userMoods[0].mood_type">
                  <div class="card-body">
                    <h5 class="card-title">{{ userMoods[0].mood_type }}</h5>
                    <p class="card-text">{{ userMoods[0].description }}</p>
                    <p class="card-text" v-if="userMoods[0].mood_cause">Cause: {{ userMoods[0].mood_cause }}</p>
                  </div>
                </div>
              </div>
              <div v-if="userMoods.length === 0" class="no-data-state">No mood data available.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import Spinner from './Spinner.vue';

export default {
  name: 'MoodHistoryPanel',
  components: { Spinner },
  props: { userMoods: { type: Array, required: true } },
  data() {
    return { isLoading: false, isError: false, errorMessage: '' };
  },
  methods: {
    moodImageUrl(moodType) {
      return `/src/images/${moodType.toLowerCase()}.png`;
    },
  },
};
</script>

<style scoped>
.container.mt-4 .card {
  max-width: 1600px; /* Increased width */
  margin-bottom: 10px;
}

.mood-card-container {
  border-radius: 5px;
  display: flex;
  justify-content: center; /* Centers the card if it's smaller than the max-width */
}

.loading-state, .no-data-state {
  text-align: center;
  padding: 20px;
}

.no-data-state {
  color: #666;
}

@media (max-width: 992px) {
  .container.mt-4 .card {
    max-width: 100%; /* Full width on smaller screens */
  }
}

</style>







