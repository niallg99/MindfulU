<template>
  <div class="event-panel">
    <h2 class="event-panel-title">Upcoming Events</h2>
    <div v-if="events.length > 0">
      <ul class="event-list">
        <li class="event-snippet" v-for="(event, index) in snippetEvents" :key="event.id">
          <h3>{{ event.name }}</h3>
          <p><strong>Date:</strong> {{ event.date }}</p>
          <p><strong>Venue:</strong> {{ event.venue }}</p>
        </li>
      </ul>
    </div>
    <p v-else>No upcoming events.</p>
  </div>
</template>

<script>
export default {
  name: 'EventPanel',
  data() {
    return {
      // Local copy of events to show in the panel
      events: []
    };
  },
  computed: {
    snippetEvents() {
      // Return the first three events for the snippet
      return this.events.slice(0, 3);
    }
  },
  created() {
    this.fetchEventSnippet();
  },
  methods: {
    fetchEventSnippet() {
      // Placeholder for fetching events logic, should be replaced with actual API call
      this.events = this.$parent.events; // This will access the events from the parent component
    }
  }
};
</script>

<style scoped>
.event-panel {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
}

.event-panel-title {
  margin-bottom: 1rem;
}

.event-list {
  list-style: none;
  padding: 0;
}

.event-snippet {
  margin-bottom: 0.5rem;
  background: white;
  padding: 0.75rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.event-snippet h3 {
  margin-top: 0;
}
</style>
