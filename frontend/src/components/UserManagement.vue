<template>
  <div class="user-management padding-bottom-2">
    <div class="card mt-4">
      <h5 class="card-header">User Management</h5>
      <div class="card-body">
        <!-- Input Group for Search -->
        <div class="input-group mb-3">
          <input type="text" 
                 class="form-control" 
                 :value="searchQuery" 
                 @input="$emit('update:searchQuery', $event.target.value)" 
                 placeholder="Search users by username, name, or surname">
          <div class="input-group-append">
            <button class="btn btn-primary" @click="applySearchFilter">Search</button>
          </div>
        </div>
        <div v-if="filteredUsers.length"
					class="table-responsive"
				>
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Username</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Last Mood Date</th>
                <th>Average Mood</th>
                <th>Risk Level</th>
              </tr>
            </thead>
            <tbody>
						<tr v-for="user in paginatedUsers" :key="user.id" @click="$emit('user-clicked', user)">
                <td>{{ user.username }}</td>
                <td>{{ user.first_name }}</td>
                <td>{{ user.last_name }}</td>
                <td>{{ user.lastMoodDate }}</td>
                <td>{{ user.averageMood }}</td>
                <td :class="riskLevelClass(user.riskLevel)">{{ user.riskLevel }}</td>
              </tr>
            </tbody>
          </table>
          <nav aria-label="User Pagination" v-if="totalPages > 1">
            <ul class="pagination">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="changePage(currentPage - 1)">&laquo; Previous</button>
              </li>
              <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                <button class="page-link" @click="changePage(page)">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="changePage(currentPage + 1)">Next &raquo;</button>
              </li>
            </ul>
          </nav>
        </div>
        <div v-else>
          <spinner />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Spinner from './Spinner.vue';

export default {
	components: {
		Spinner,
	},
  props: {
    users: {
      type: Array,
      default: () => []
    },
    searchQuery: String
  },
	data() {
		 return {
      filteredUsers: [],
      currentPage: 1,
      pageSize: 25,
      totalPages: 0,
			localSearchQuery: this.searchQuery,
			selectedUser: null,
      showUserModal: false
    };
	},
	computed: {
    paginatedUsers() {
      if (!Array.isArray(this.filteredUsers)) {
        return [];
      }
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredUsers.slice(start, end);
    }
  },
  mounted() {
    console.log('Received users:', this.users);
    this.applySearchFilter();
  },
	methods: {
		applySearchFilter() {
			this.filteredUsers = this.searchQuery ?
				this.users.filter(user =>
					user.username.includes(this.searchQuery) ||
					user.first_name.includes(this.searchQuery) ||
					user.last_name.includes(this.searchQuery)
				) : this.users;
			this.updatePagination();
		},
		changePage(page) {
			if (page < 1 || page > this.totalPages) {
				return;
			}
			this.currentPage = page;
		},
		updatePagination() {
			this.totalPages = Math.ceil(this.filteredUsers.length / this.pageSize);
		},
		riskLevelClass(riskLevel) {
			return {
				'high-risk': riskLevel === 'High',
				'medium-risk': riskLevel === 'Medium',
				'low-risk': riskLevel === 'Low',
			};
			},
			updateSearchQuery() {
			this.$emit('update:searchQuery', this.localSearchQuery);
		},
	},
	watch: {
		users: {
			immediate: true,
			handler(newValue) {
				this.filteredUsers = newValue || [];
				this.updatePagination();
			}
		},
		searchQuery(newValue) {
			this.localSearchQuery = newValue;
		}
	}
};
</script>

<style scoped>
.high-risk {
	background-color: #ffcccc; 
}
.medium-risk {
	background-color: #ffffcc; 
}
.low-risk {
	background-color: #ccffcc; 
}
.user-management {
	display: flex;
	justify-content: center;
	margin: 0 auto;
	width: 80%;
}

</style>
