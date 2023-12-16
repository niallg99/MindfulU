<template>
		<div class="container mt-4">
				<div class="row justify-content-center">
						<div class="col-lg-12">
								<div class="card panel-card">
										<div class="card-header">
												Upcoming Events
										</div>
										<div class="card-body">
												<div v-if="isLoading">
														<spinner />
												</div>
												<div v-else-if="isError">
														{{ errorMessage }}
												</div>
												<div v-else>
														<ul class="list-group list-group-flush">
																<li class="list-group-item" v-for="event in upcomingEvents" :key="event.id">
																		<strong>{{ event.name }}</strong><br>
																		Date: {{ event.date }}<br>
																		Venue: {{ event.venue }}
																</li>
														</ul>
												</div>
										</div>
										<div class="card-footer text-center">
												<button class="btn btn-primary" @click="navigateToEvents">See More Events</button>
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
	name: 'EventPanel',
		components: { Spinner },
    props: {
        events: Array,
        isLoading: Boolean,
        isError: Boolean,
        errorMessage: String,
    },
    setup() {
        const router = useRouter();
        const navigateToEvents = () => {
            router.push('/events');
        };
        return { navigateToEvents };
    },
    computed: {
        upcomingEvents() {
            return this.events.slice(0, 3);
        },
    },
    components: { Spinner }
};
</script>
