<template>
  <div>
    <h1>Events</h1>
    <table>
      <thead>
        <tr>
          <th>Event/Programme</th>
          <th>Date</th>
          <th>Venue</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="event in filteredEvents" :key="event.id">
          <td>{{ event.name }}</td>
          <td>{{ event.date }}</td>
          <td>{{ event.venue }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="filteredEvents.length === 0">No events found.</p>
  </div>
</template>

<script>
import { fetchEvents } from '@/api/events';

export default {
  data() {
    return {
      events: []
    }
  },
  computed: {
    filteredEvents() {
      // Slice the first entry (header) from the events data
      return this.events.slice(1);
    }
  },
  created() {
    fetchEvents()
      .then(data => {
        this.events = data;
      })
      .catch(error => {
        console.error('There was a problem fetching the events:', error);
      });
  }
}
</script>
