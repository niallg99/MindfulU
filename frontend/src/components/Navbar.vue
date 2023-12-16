<template>
  <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-fluid">
      <template v-if="isLoggedIn">
        <router-link to="/dashboard" class="navbar-brand">MindfulU</router-link>
      </template>
      <template v-else>
        <a class="navbar-brand" href="#">MindfulU</a>
      </template>
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
           <li class="nav-item" v-if="isLoggedIn">
            <a class="nav-link" href="#" @click="openProfileModal">Profile</a>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link to="/events" class="nav-link">Events</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link to="/support" class="nav-link">Support</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link to="/friends" class="nav-link">Friends</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link to="/mood-history" class="nav-link">Mood History</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link to="/login" class="nav-link">Logout</router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="pagesDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Pages
            </a>
            <ul class="dropdown-menu" aria-labelledby="pagesDropdown">
              <li v-for="route in router.getRoutes()" :key="route.path">
                <router-link :to="route.path" class="dropdown-item">{{ route.name }}</router-link>
              </li>
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
import router from '../router';

export default {
  name: 'Navbar',
  components: {
    ProfileModal,
  },
  data() {
    return {
      notifications: [],
      friendRequests: [],
      router: router,
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
    logout() {
    localStorage.removeItem('accessToken');
    this.$router.push('/login');
    },
  toggleNavbar() {
    const navbarCollapse = this.$refs.navbarCollapse;
    navbarCollapse.classList.toggle('show');
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