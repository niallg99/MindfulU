<template>
  <div class="page-container">
    <navbar />
    <div class="container mood-history my-4">
      <div class="card shadow">
        <div class="card-header bg-light">
          <h2 class="card-title mb-0">Mood History</h2>
        </div>
        <div class="card-body">
          <p class="card-text mb-4">Track your mood over time to see how you're doing. Click on a mood to see more details or to edit it.</p>
          <div v-if="isLoading">
            <span>Loading moods...</span>
          </div>
          <div v-else-if="isError">
            <span>{{ errorMessage }}</span>
          </div>
          <div v-else-if="moods.length === 0" class="text-center py-5">
            <p class="lead">You have no moods yet. Start adding moods to see them here!</p>
          </div>
          <div v-else class="row g-3">
            <div class="col-4 col-md-6 col-lg-3" v-for="mood in paginatedMoods" :key="mood.id" @click="openModal(mood)">
              <div class="card h-100">
                <img :src="moodImageUrl(mood.mood_type)" class="card-img-top" :alt="mood.mood_type">
                <div class="card-body">
                  <p class="card-text">{{ formatDate(mood.mood_date) }}</p>
                </div>
              </div>
            </div>
          </div>
          <nav v-if="totalPages > 1" class="mt-4">
            <ul class="pagination justify-content-center">
              <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
                <button class="page-link" @click="setCurrentPage(page)">{{ page }}</button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      <mood-history-modal
        ref="moodModalRef"
        :mood="selectedMood"
        @update-mood="handleUpdateMood"
        :moodChoices="moodChoices"
        :moodCauses="moodCauses"
        @close-modal="showModal = false"
        @save="handleSave"
        @delete="handleDelete"
      />
    </div>
    <custom-footer />
  </div>
</template>



<script>
import { fetchUserMoods, fetchMoodChoices, fetchMoodCauses } from '@/api/moods';
import MoodHistoryModal from './MoodHistoryModal.vue';
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';

export default {
	name: 'MoodHistory',
	components: {
		MoodHistoryModal,
		Navbar,
		CustomFooter,
	},
	data() {
		return {
			moods: [],
			moodChoices: [],
			moodCauses: [],
			currentPage: 1,
			perPage: 25,
			isLoading: true,
			isError: false,
			errorMessage: '',
			showModal: false,
			selectedMood: null,
		};
	},
	computed: {
		paginatedMoods() {
			const start = (this.currentPage - 1) * this.perPage;
			return this.moods.slice(start, start + this.perPage);
		},
		totalPages() {
			return Math.ceil(this.moods.length / this.perPage);
		}
	},
	methods: {
		async loadMoods() {
			try {
				const userId = localStorage.getItem('userId');
				if (userId) {
					const response = await fetchUserMoods(userId);
					this.moods = response;
				}
			} catch (error) {
				console.error('Error fetching mood data:', error);
				this.isError = true;
				this.errorMessage = 'Failed to load moods.';
			} finally {
				this.isLoading = false;
			}
		},
		async loadMoodChoices() {
			try {
				const response = await fetchMoodChoices();
				this.moodChoices = response.map(choiceArray => choiceArray[0]);
			} catch (error) {
				console.error('Error fetching mood choices:', error);
			}
		},
		async loadMoodCauses() {
			try {
				const moodCausesResponse = await fetchMoodCauses();
				this.moodCauses = [...moodCausesResponse];
			} catch (error) {
				console.error('Error fetching mood causes:', error);
			}
		},
		setCurrentPage(page) {
			this.currentPage = page;
		},
		moodImageUrl(moodType) {
			return `/src/images/${moodType.toLowerCase()}.png`;
		},
		openModal(mood) {
			this.selectedMood = mood;
			this.$refs.moodModalRef.show();
		},
		formatDate(dateStr) {
			const date = new Date(dateStr);
			const options = { day: 'numeric', month: 'short', year: 'numeric' };
			return date.toLocaleDateString('en-GB', options);
		},
		handleDelete(deletedMoodId) {
			this.moods = this.moods.filter(mood => mood.id !== deletedMoodId);
		},
		handleUpdateMood(updatedMood) {
			const index = this.moods.findIndex(mood => mood.id === updatedMood.id);
			if (index !== -1) {
				this.moods[index] = updatedMood;
			}
		},
	},
	async mounted() {
		Promise.all([
		this.loadMoods(),
		this.loadMoodChoices(),
		this.loadMoodCauses(),
		]);
	}
};
</script>

