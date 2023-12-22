<script>
import { postMood, fetchMoodCauses, fetchMoodChoices } from '@/api/moods';

export default {
	name: 'Mood',
	props: {
		mood: {
			type: String,
			required: true
		},
		userId: {
			type: [String, Number],
			required: true
		},
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
	},
	shouldShowCauseInput() {
		return !['Happy'].includes(this.mood);
	},
},
	methods: {
		toggleModal() {
			this.isModalVisible = !this.isModalVisible;
		},
		async submitForm() {
      try {
        const moodData = {
          mood_type: this.mood,
          description: this.feedback,
          mood_cause: this.selectedCause,
          user: this.userId,
        };
        await postMood(moodData);
        this.resetForm();
        this.isModalVisible = false;
      } catch (error) {
        console.error('Error posting mood:', error);
      }
    },
	resetForm() {
		this.selectedCause = '';
		this.feedback = '';
		},
	},
	async mounted() {
		try {
			this.moods = await fetchMoodChoices();
			this.causeChoices = await fetchMoodCauses();
		} catch (error) {
			console.error('Error fetching mood causes:', error);
		}
	}
};
</script>
<template>
	<div class="card mood-card">
		<div class="card-body p-0" :style="backgroundStyle">
			<div class="mood-overlay" @click="toggleModal">
				<button class="btn mood-btn-primary btn-primary">{{ mood }}</button>
			</div>
		</div>
		<div v-if="isModalVisible" class="mood-modal">
			<div class="modal-overlay" @click="toggleModal"></div>
				<div class="modal-content">
					<span class="close" @click="toggleModal">&times;</span>
					<form @submit.prevent="submitForm">
						<p>You have selected: {{ mood }}</p>
						<div class="form-group" v-if="shouldShowCauseInput">
							<label for="cause">Select a cause:</label>
							<select id="cause" class="form-control" v-model="selectedCause">
								<option v-for="cause in causeChoices" :key="cause" :value="cause">
									{{ cause }}
								</option>
							</select>
					</div>
					<div class="form-group padding-top-1">
						<label for="feedback">Your feedback:</label>
						<textarea id="feedback" class="form-control" v-model="feedback"></textarea>
					</div>
					<div class="padding-top-1">
						<button type="submit" class="btn btn-success">Submit</button>
					</div>
				</form>
  		</div>
		</div>
	</div>
</template>

