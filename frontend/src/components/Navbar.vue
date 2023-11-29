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
          <li v-else class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="notificationsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <img src="/src/images/bell.svg" alt="Notifications" style="width: 20px; height: 20px;"> 
              <span v-if="friendRequests.length">({{ friendRequests.length }})</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationsDropdown">
              <li v-for="request in friendRequests" :key="request.id" class="dropdown-item d-flex justify-content-between">
                {{ request.sender }} wants to be friends.
                <span>
                  <button @click="acceptRequest(request.id)">✓</button>
                  <button @click="declineRequest(request.id)">✗</button>
                </span>
              </li>
              <li v-if="!friendRequests.length">
                <a class="dropdown-item" href="#">No new notifications</a>
              </li>
            </ul>
          </li>
          <li v-if="isLoggedIn" class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Profile
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="#" @click="openProfileModal">Profile</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><router-link class="dropdown-item" to="/logout">Logout</router-link></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <profile-modal ref="profileModalRef" />
</template>


<script>
import { fetchFriendRequests, acceptFriendRequest, rejectFriendRequest } from '@/api/friends';
import ProfileModal from './ProfileModal.vue';

export default {
  name: 'Navbar',
  components: {
    ProfileModal,
  },
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
    async fetchFriendRequests() {
      try {
        const requests = await fetchFriendRequests();
        this.friendRequests = requests;
      } catch (error) {
        console.error('Error fetching friend requests:', error);
      }
  },
    async acceptRequest(username) {
      try {
        const response = await acceptFriendRequest(username);
        console.log('Accept friend request response:', response);
        await this.fetchFriendRequests();
        await this.loadFriendsData();
      } catch (error) {
        console.error('Error accepting friend request:', error);
      }
    },
    async declineRequest(username) {
      try {
        await rejectFriendRequest(username);
        await this.fetchFriendRequests();
      } catch (error) {
        console.error('Error declining friend request:', error);
      }
    },
    openProfileModal() {
      this.$refs.profileModalRef.show();
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