<template>
  <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img src="/src/images/mental-health-during-covid-19.png" alt="MindfulU Logo" width="45" height="30">
        MindfulU
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li v-if="!isLoggedIn" class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item dropdown" v-if="isLoggedIn">
            <a class="nav-link dropdown-toggle" href="#" id="notificationsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Notifications <span v-if="friendRequests.length">({{ friendRequests.length }})</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationsDropdown">
              <li v-for="request in friendRequests" :key="request.id" class="dropdown-item d-flex justify-content-between">
                {{ request.sender }} wants to be friends.
                <span>
                  <button @click="acceptRequest(request.id)">✓</button>
                  <button @click="declineRequest(request.id)">✗</button>
                </span>
              </li>
              <li v-if="notifications.length === 0">
                <a class="dropdown-item" href="#">No new notifications</a>
              </li>
            </ul>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <a class="nav-link" href="#" id="loginPrompt">Need to log in</a>
          </li>
          <li class="nav-item dropdown" v-if="isLoggedIn">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Profile
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
              <li><router-link class="dropdown-item" to="/profile">Profile</router-link></li>
              <li><router-link class="dropdown-item" to="/settings">Settings</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><router-link class="dropdown-item" to="/logout">Logout</router-link></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { fetchFriendRequests } from '@/api/friends';

export default {
  name: 'Navbar',
  data() {
    return {
      notifications: [],
      friendRequests: [],
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('accessToken');
    },
  },
  methods: {
    toggleLogin() {
      this.$emit('update:isStaffLogin', !this.isStaffLogin);
    },
    async fetchFriendRequests() {
      try {
        const requests = await fetchFriendRequests();
        this.friendRequests = requests;
      } catch (error) {
        console.error('Error fetching friend requests:', error);
      }
  },
    async acceptRequest(requestId) {
      // Logic to accept friend request
    },
    async declineRequest(requestId) {
      // Logic to decline friend request
    },
  },
    mounted() {
    if (this.isLoggedIn) {
      this.fetchFriendRequests();
    }
    const dropdownElements = document.querySelectorAll('.dropdown-toggle');
    dropdownElements.forEach(dropdown => {
      new bootstrap.Dropdown(dropdown);
    });
  }
};
</script>
