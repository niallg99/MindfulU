<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-12">
        <div class="card">
          <div class="card-header">
            Friends
          </div>
          <div class="card-body">
            <div v-if="showAddFriendModal" class="modal fade show d-block" id="addFriendModal" tabindex="-1" aria-labelledby="addFriendModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="addFriendModalLabel">Add a Friend</h5>
                    <button type="button" class="btn-close" @click="closeAddFriendModal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    <input type="text" class="form-control" placeholder="Enter friend's username" v-model="friendUsername">
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="closeAddFriendModal">Close</button>
                    <button type="button" class="btn btn-primary" @click="addFriend">Add Friend</button>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-backdrop fade show" v-if="showAddFriendModal"></div>
            <div v-if="isLoading">
              <spinner />
            </div>
            <div v-else-if="isError">
              {{ errorMessage }}
            </div>
            <div v-else-if="friendsList?.length === 0">
              <div class="no-friends">
                <p>No friends yet. Start adding friends now!</p>
              </div>
            </div>
            <div v-else>
              <div class="row">
                <div class="col-md-4" v-for="friend in limitedFriendsList" :key="friend.id">
                  <div class="card friend-card mb-3">
                    <div class="row g-0">
                      <div class="col-md-4">
                        <img :src="friend.profilePicture || '/path/to/default-picture.png'" class="img-fluid rounded-start" :alt="friend.name">
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
              <button class="btn btn-primary mt-3" @click="navigateToAllFriends">See All Friends</button>
            </div>
						<button class="btn btn-primary float-right" @click="openAddFriendModal">Add Friends</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchFriends, sendFriendRequest } from '@/api/friends';
import { useRouter } from 'vue-router'; 

export default {
	name: 'FriendsPanel',
		setup() {
			const router = useRouter();
			return {
				navigateToAllFriends() {
					router.push('/friends');
				},
			};
	},
  data() {
    return {
      friendsList: [],
      isLoading: true,
      isError: false,
      errorMessage: '',
      showAddFriendModal: false,
      friendUsername: '',
    };
  },
  computed: {
    limitedFriendsList() {
      return this.friendsList ? this.friendsList.slice(0, 3) : [];
    },
  },
  methods: {
    async loadFriendsData() {
      try {
        this.userId = localStorage.getItem('userId');
        if (!this.userId) {
          throw new Error("User ID is undefined");
        }
        this.friendsList = await fetchFriends(this.userId);
        this.isLoading = false;
      } catch (error) {
        console.error('Error fetching friends data:', error);
        this.isError = true;
        this.errorMessage = 'Failed to load friends.';
        this.friendsList = [];
      }
    },
    openAddFriendModal() {
      this.showAddFriendModal = true;
    },
    closeAddFriendModal() {
      this.showAddFriendModal = false;
      this.friendUsername = '';
    },
    async addFriend() {
      try {
        await sendFriendRequest(this.friendUsername);
        alert('Friend request sent successfully to ' + this.friendUsername);
        this.closeAddFriendModal();

        await this.loadFriendsData();
      } catch (error) {
        console.error('Error sending friend request:', error);
        alert('Failed to send friend request. Please try again.');
      }
    },
  },
  mounted() {
    this.loadFriendsData();
  }
};
</script>
