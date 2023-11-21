<template>
  <div class="row">
    <div class="col-md-4" v-for="friend in friendsList" :key="friend.id">
      <div class="card friend-card mb-3">
        <div class="row g-0">
          <div class="col-md-4">
            <img 
              :src="friend.profilePicture || '/path/to/default-picture.png'" 
              class="img-fluid rounded-start" 
              :alt="friend.name"
            >
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <h5 class="card-title">{{ friend.name }}</h5>
              <p class="card-text"><small class="text-muted">@{{ friend.username }}</small></p>
              <p class="card-text">{{ friend.mostRecentMood }}</p>
              <p class="card-text" v-if="friend.mostRecentCause">Cause: {{ friend.mostRecentCause }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchFriends } from '@/api/friends';

export default {
  data() {
    return {
      friendsList: []
    };
  },
  async mounted() {
    try {
      // Assuming the userId is available, else you need to get it from auth state or local storage
      const userId = 'your-user-id'; // Replace with the actual user ID
      this.friendsList = await fetchFriends(userId);
    } catch (error) {
      console.error('Error fetching friends data:', error);
      // Handle error appropriately
    }
  }
};
</script>

<style scoped>
.friend-card .card-body {
  padding: 1rem;
}

.friend-card img {
  width: 100%;
  object-fit: cover; /* Ensures the image covers the area nicely */
}

.friend-card .card-title {
  margin-bottom: 0.5rem;
}
</style>
