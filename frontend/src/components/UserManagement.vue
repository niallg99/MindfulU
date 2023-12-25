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
			localUsers: [],
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
		this.localUsers = JSON.parse(JSON.stringify(this.users));
		this.processUsers();
		this.applySearchFilter();
	},
	methods: {
		processUsers() {
			this.localUsers = this.localUsers.map(user => {
				return {
					...user,
					averageMood: this.calculateMostSelectedMood(user.moods)
				};
			});
		},
		calculateMostSelectedMood(moods) {
			if (!moods || moods.length === 0) {
				return 'N/A';
			}
			const moodCount = moods.reduce((acc, mood) => {
				acc[mood.mood_type] = (acc[mood.mood_type] || 0) + 1;
				return acc;
			}, {});
			return Object.entries(moodCount).reduce((a, b) => a[1] > b[1] ? a : b)[0];
		},
		applySearchFilter() {
			this.filteredUsers = this.searchQuery ?
				this.localUsers.filter(user =>
					user.username.includes(this.searchQuery) ||
					user.first_name.includes(this.searchQuery) ||
					user.last_name.includes(this.searchQuery)
				) : this.localUsers;
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
		users(newValue) {
			this.localUsers = JSON.parse(JSON.stringify(newValue));
			this.processUsers();
			this.applySearchFilter();
		},
		searchQuery(newValue) {
			this.localSearchQuery = newValue;
		}
	}
};
</script>
<template>
	<div class="user-management padding-bottom-2">
		<div class="card mt-4">
			<h5 class="card-header">User Management</h5>
			<div class="card-body">
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
