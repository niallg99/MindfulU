<script>
export default {
	name: 'Navbar',
	props: {
		isLoggedIn: {
			type: Boolean,
			default: false
		},
		isStaffLogin: {
			type: Boolean,
			default: false
		}
	},
	methods: {
		toggleLogin() {
		this.$emit('update:isStaffLogin', !this.isStaffLogin);
		}
  }
}
</script>
<template>
  <nav :class="['navbar', { 'navbar-staff-login': isStaffLogin }]" 
  	class="navbar navbar-expand-lg navbar-custom">
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
			<li class="nav-item">
				<router-link class="nav-link" to="/">Login</router-link>
			</li>
			<li class="nav-item">
				<button type="button" class="nav-link btn btn-link" @click="toggleLogin">{{ isStaffLogin ? 'User Login' : 'Staff Login' }}</button>
			</li>
			<li v-if="isLoggedIn"
				class="nav-item dropdown">
				<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
					Profile
				</a>
				<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
					<li><router-link class="dropdown-item" to="/action">Action</router-link></li>
					<li><router-link class="dropdown-item" to="/another-action">Another action</router-link></li>
					<li><hr class="dropdown-divider"></li>
					<li><router-link class="dropdown-item" to="/something-else-here">Logout</router-link></li>
				</ul>
		  </li>
		</ul>
	  </div>
	</div>
  </nav>
</template>

