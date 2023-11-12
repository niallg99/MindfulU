<script>
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';
import Mood from './Mood.vue';
import Card from './Card.vue';
import { fetchMoodChoices } from '../api/moods.js'; 
import SupportForYou from './SupportForYou.vue';

export default {
	name: 'Dashboard',
	components: {
		Navbar,
		Mood,
		Card,
		SupportForYou,
		CustomFooter,
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
<template>
	<navbar :isLoggedIn="true" :isStaff="isStaff" @update:isStaffLogin="isLoggedIn" />
	
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
				<card :header="header" :body="'This is the ' + header" />
			</div>
		</div>
		<div class="row">
			<div class="col-lg-6 col-md-6 col-sm-12 mb-4" v-for="(header, index) in cardHeaders.slice(2, 4)" :key="'bottom-row-' + index">
				<card :header="header" :body="'This is the ' + header" />
			</div>
		</div>
	</div>
	<div class="container-fluid">
		<div class="row justify-content-center">
			<div class="col-lg-6 col-md-8 col-sm-12 mb-4">
				<support-for-you />
			</div>
		</div>
	</div>
	<custom-footer />
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
