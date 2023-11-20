<template>
  <div class="container mood-history">
    <h1>Mood History</h1>
    <div v-if="isLoading">Loading moods...</div>
    <div v-else-if="isError">{{ errorMessage }}</div>
    <div v-else>
      <div class="row">
        <div class="col-md-2 mood-item" v-for="mood in paginatedMoods" :key="mood.id" @click="openModal(mood)">
          <div class="card">
            <img :src="moodImageUrl(mood.mood_type)" class="card-img-top" :alt="mood.mood_type">
            <div class="card-body">
							<p class="card-text">{{ formatDate(mood.mood_date) }}</p> <!-- Use formatDate method here -->
            </div>
          </div>
        </div>
      </div>
      <nav>
        <ul class="pagination">
          <li v-for="page in totalPages" :key="page" class="page-item">
            <button class="page-link" @click="setCurrentPage(page)">{{ page }}</button>
          </li>
        </ul>
      </nav>
    </div>

   <!-- Mood Edit Modal -->
    <MoodHistoryModal
      :show="showModal"
      :mood="selectedMood"
      :moodChoices="moodChoices"
      @close-modal="showModal = false"
      @save="handleSave"
    />
  </div>
</template>

<script>
import { fetchUserMoods, fetchMoodChoices } from '@/api/moods';
import MoodHistoryModal from './MoodHistoryModal.vue';

export default {
  name: 'MoodHistory',
  components: {
    MoodHistoryModal
  },
  data() {
    return {
      moods: [],
      moodChoices: [], // Add moodChoices as a data property
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
				console.log("Mood choices response:", response);

				// Transform the response to a simple array of strings
				this.moodChoices = response.map(choiceArray => choiceArray[0]);
			} catch (error) {
				console.error('Error fetching mood choices:', error);
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
			this.$nextTick(() => {
				const modalElement = document.getElementById('moodModal');
				if (!this.modalInstance) {
					this.modalInstance = new bootstrap.Modal(modalElement);
				}
				this.modalInstance.show();
			});
		},
		formatDate(dateStr) {
			const date = new Date(dateStr);
			const options = { day: 'numeric', month: 'short', year: 'numeric' };
			return date.toLocaleDateString('en-GB', options);
		}
  },
  mounted() {
		this.loadMoods();
		this.loadMoodChoices();
  }
};
</script>

<style scoped>
.mood-history {
  text-align: center;
  margin-top: 20px;
}

.mood-item {
  margin-bottom: 20px;
}
</style>
