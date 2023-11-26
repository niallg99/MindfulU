<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-12">
        <div class="card panel-card">
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
              <div v-if="userMoods.length > 0" class="mood-carousel-container">
                <div id="moodCarousel" class="carousel slide" data-bs-ride="carousel">
									<div class="carousel-inner">
										<div class="carousel-item" :class="{ active: index === 0 }" v-for="(mood, index) in recentUserMoods" :key="mood.id">
											<img :src="moodImageUrl(mood.mood_type)" class="d-block w-100" :alt="mood.mood_type">
											<div class="carousel-caption d-none d-md-block">
												<h5>{{ mood.mood_type }}</h5>
												<p>{{ mood.description }}</p>
												<p v-if="mood.mood_cause">Cause: {{ mood.mood_cause }}</p>
											</div>
										</div>
									</div>
									<button class="carousel-control-prev" type="button" data-bs-target="#moodCarousel" data-bs-slide="prev">
										<span class="carousel-control-prev-icon" aria-hidden="true"></span>
										<span class="visually-hidden">Previous</span>
									</button>
									<button class="carousel-control-next" type="button" data-bs-target="#moodCarousel" data-bs-slide="next">
										<span class="carousel-control-next-icon" aria-hidden="true"></span>
										<span class="visually-hidden">Next</span>
									</button>
								</div>
              </div>
              <div v-if="userMoods.length === 0" class="no-data-state">No mood data available.</div>
            </div>
          </div>
          <div class="card-footer text-center">
            <button class="btn btn-primary" @click="navigateToMoodHistory">See All Moods</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'; 
import Spinner from './Spinner.vue';

export default {
	name: 'MoodHistoryPanel',
	setup() {
    const router = useRouter();
    return {
      navigateToMoodHistory() {
        router.push('/mood-history');
      },
    };
  },
	components: { Spinner },
	props: { userMoods: { type: Array, required: true } },
	data() {
		return { isLoading: false, isError: false, errorMessage: '' };
	},
	computed: {
		recentUserMoods() {
			return this.userMoods.slice(-3);
		},
	},
	methods: {
		moodImageUrl(moodType) {
			return `/src/images/${moodType.toLowerCase()}.png`;
		},
	},
};
</script>

<style scoped>
.mood-carousel-container .carousel-item {
	max-height: 400px;
	overflow: hidden;
	text-align: center;
}

.mood-carousel-container img {
	width: auto;
	max-height: 50%;
	max-width: 30%;
	margin: auto;
}

.carousel-caption {
	background-color: rgba(0, 0, 0, 0.5);
	border-radius: 5px;
}

@media (max-width: 992px) {
	.container.mt-4 .card {
		max-width: 100%;
	}

	.mood-carousel-container .carousel-item {
		max-height: 250px;
	}

	.mood-carousel-container img {
		max-width: 80%;
	}
}
</style>

