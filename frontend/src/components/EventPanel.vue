<script>
import { fetchEvents } from '@/api/events';
import { useRouter } from 'vue-router'; // Import useRouter from vue-router

export default {
  name: 'EventPanel',
  setup() {
    const router = useRouter(); // Initialize router
    const navigateToEvents = () => {
      router.push('/events'); // Navigate to '/events' when button is clicked
    };

    return { navigateToEvents };
  },
  data() {
    return {
      events: [],
      isLoading: true,
      isError: false,
      errorMessage: '',
    };
  },
  computed: {
    upcomingEvents() {
      return this.events.slice(1, 4); //Skip first element as it is the header
    },
  },
  created() {
    fetchEvents()
      .then(data => {
        this.events = data.sort((a, b) => new Date(a.date) - new Date(b.date)); // Sort events by date
        this.isLoading = false;
      })
      .catch(error => {
        console.error('There was a problem fetching the events:', error);
        this.isError = true;
        this.errorMessage = 'Failed to load events.';
      });
  }
}
</script>

<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-header">
            Upcoming Events
          </div>
          <div class="card-body">
            <div v-if="isLoading">
              Loading events...
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
              <button class="btn btn-primary mt-3" @click="navigateToEvents">See More Events</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
