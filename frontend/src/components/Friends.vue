<template>
  <navbar :is-logged-in="isLoggedIn" :is-staff-login="isStaffLogin" @update:isStaffLogin="handleStaffLoginToggle"/>
  <div class="container mt-4">
    <div class="row">
      <!-- Friend Cards -->
      <template v-if="friendsList.length">
        <div class="col-md-4" v-for="friend in paginatedFriendsList" :key="friend.id">
          <div class="card friend-card mb-3">
            <div class="row g-0">
              <div class="col-md-4">
                <img 
                  :src="friend.profilePicture || '/src/images/person.svg'" 
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
      </template>
      <!-- Add Friend Modal -->
      <div v-if="showAddFriendModal" class="modal fade show d-block" tabindex="-1" aria-hidden="true">
        <!-- Modal Content -->
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add a Friend</h5>
              <button type="button" class="btn-close" @click="modalToggle"></button>
            </div>
            <div class="modal-body">
              <input type="text" class="form-control" placeholder="Enter friend's username" v-model="friendUsername">
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="modalToggle">Close</button>
              <button type="button" class="btn btn-primary" @click="addFriend">Add Friend</button>
            </div>
          </div>
        </div>
      </div>
      <!-- Empty State Card -->
      <template v-else>
        <div class="col-12">
          <div class="card text-center">
            <div class="card-body">
              <p>No friends added yet. Start connecting!</p>
              <button class="btn btn-primary" @click="modalToggle">Add Friend</button>
            </div>
          </div>
        </div>
      </template>
    </div>
    <!-- Pagination -->
    <nav aria-label="Page navigation" v-if="totalPages > 1">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" aria-label="Previous" @click.prevent="changePage(currentPage - 1)">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" aria-label="Next" @click.prevent="changePage(currentPage + 1)">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
  <custom-footer />
</template>


<script>
import { fetchFriends, sendFriendRequest, acceptFriendRequest, rejectFriendRequest, fetchFriendRequests } from '@/api/friends';
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';

export default {
  name: 'Friends',
  components: {
    Navbar,
    CustomFooter,
  },
  data() {
    return {
      friendsList: [],
      isLoading: false,
      isError: false,
      errorMessage: '',
      currentPage: 1,
      pageSize: 25,
      showAddFriendModal: false,
      friendUsername: '',
      friendRequests: [],
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.friendsList.length / this.pageSize);
    },
    paginatedFriendsList() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.friendsList.slice(start, end);
    },
  },
  methods: {
    async loadFriendsData() {
      this.isLoading = true;
      try {
        const data = await fetchFriends();
        this.friendsList = data;
      } catch (error) {
        console.error('Error fetching friends data:', error);
        this.isError = true;
        this.errorMessage = 'Failed to load friends. Please try again later.';
      } finally {
        this.isLoading = false;
      }
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
      try {
        await acceptFriendRequest(requestId);
        // Refresh the list after accepting
        await this.fetchFriendRequests();
        await this.loadFriendsData();
      } catch (error) {
        console.error('Error accepting friend request:', error);
      }
    },
    async declineRequest(requestId) {
      try {
        await rejectFriendRequest(requestId);
        // Refresh the list after declining
        await this.fetchFriendRequests();
      } catch (error) {
        console.error('Error declining friend request:', error);
      }
    },
    async addFriend() {
      try {
        await sendFriendRequest(this.friendUsername);
        alert('Friend request sent successfully to ' + this.friendUsername);
        this.modalToggle(); // Close the modal after sending the request
        await this.loadFriendsData(); // Reload friend data
      } catch (error) {
        console.error('Error sending friend request:', error);
        alert('Failed to send friend request. Please try again.');
      }
    },
    modalToggle() {
      this.showAddFriendModal = !this.showAddFriendModal;
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) {
        return;
      }
      this.currentPage = page;
    },
  },
  mounted() {
    this.loadFriendsData();
    this.fetchFriendRequests();
  }
};
</script>




<style scoped>
.friend-card .card-body {
  padding: 1rem;
}

.friend-card img {
  width: 100%;
  object-fit: cover;
}

.friend-card .card-title {
  margin-bottom: 0.5rem;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 
}

</style>