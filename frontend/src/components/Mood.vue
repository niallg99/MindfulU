<script>
import { postMood, fetchMoodCauses } from '@/api/moods';

export default {
  name: 'Mood',
  props: {
    mood: {
      type: String,
      required: true
    },
    selectionCount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      isModalVisible: false,
      isCauseInputVisible: false,
      selectedCause: '',
      feedback: '',
      causeChoices: [],
    };
  },
  computed: {
    backgroundStyle() {
      const imageUrl = `/src/images/${this.mood.toLowerCase()}.png`;
      return {
        backgroundImage: `url(${imageUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      };
    }
  },
  methods: {
    toggleModal() {
      this.isModalVisible = !this.isModalVisible;
      // Check if the mood is NOT "meh" to show/hide the cause input
      this.isCauseInputVisible = this.mood !== "meh";
    },
    async submitForm() {
      try {
        const moodData = {
          mood_type: this.mood,
          description: this.feedback,
					mood_cause: this.selectedCause,
					user: this.user,
        };
        const response = await postMood(moodData);
        console.log('Mood posted successfully:', response);
        this.resetForm();
      } catch (error) {
        console.error('Error posting mood:', error);
      }
    },
    async mounted() {
      try {
        this.causeChoices = await fetchMoodCauses();
      } catch (error) {
        console.error('Error fetching mood causes:', error);
      }
    }
  }
};
</script>
<template>
	<div class="card mood-card">
		<div class="card-body p-0" :style="backgroundStyle">
			<div class="mood-overlay" @click="toggleModal">
				<button class="btn btn-primary">{{ mood }}</button>
			</div>
		</div>
		<div v-if="isModalVisible" class="mood-modal">
			<div class="modal-overlay" @click="toggleModal"></div>
			<div class="modal-content">
				<span class="close" @click="toggleModal">&times;</span>
				<form @submit.prevent="submitForm">
					<p>You have selected: {{ mood }}</p>
					<div class="form-group">
						<label for="feedback">Your feedback:</label>
						<textarea id="feedback" class="form-control" v-model="feedback"></textarea>
					</div>
					<div class="form-group" v-if="isCauseInputVisible">
						<label for="cause">Select a cause:</label>
						<select id="cause" class="form-control" v-model="selectedCause">
							<option v-for="(choice, index) in causeChoices" :key="index" :value="choice[0]">
								{{ choice[1] }}
							</option>
						</select>
					</div>

					<button type="submit" class="btn btn-success">Submit</button>
				</form>
			</div>
		</div>
	</div>
</template>

