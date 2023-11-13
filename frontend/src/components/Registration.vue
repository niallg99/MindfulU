<script>
import { registerUser } from '@/api/registration';
import { getAccessToken } from '@/api/auth';
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';

export default {
	name: 'Registration',
	components: {
	Navbar,
	CustomFooter,
},
	data() {
		return {
				username: "",
				email: "",
				password: "",
				first_name: "",
				last_name: "",
		};
	},
	methods: {
		register() {
			const userData = {
				username: this.username,
				email: this.email,
				password: this.password,
				first_name: this.first_name,
				last_name: this.last_name,
			};

			registerUser(userData)
				.then(result => {
					if (result.success) {
						this.$router.push("/login");
					} else {
						console.error("Error registering user:", result.error);
					}
				})
				.catch(error => {
					console.error("Error during registration:", error);
				});
		}
	},
};
</script>
<template>
	<Navbar />
	<div class="container content h-100">
		<div class="row justify-content-center align-items-center">
			<div class="col-md-8">
				<div class=" card registration-card">
					<div class="card-header text-center">
						<img src="/src/images/mental.svg" alt="Logo" class="mb-4" style="width: 200px; height: auto;">
					</div>
					<div class="card-body">
						<form @submit.prevent="register" class="row g-3">
							<div class="col-md-6">
								<label for="first_name" class="form-label">Forename</label>
								<input v-model="first_name" type="text" class="form-control" id="first_name" required />
							</div>
							<div class="col-md-6">
								<label for="last_name" class="form-label">Surname</label>
								<input v-model="last_name" type="text" class="form-control" id="last_name" required />
							</div>
							<div class="col-12">
								<label for="username" class="form-label">Username</label>
								<input v-model="username" type="text" class="form-control" id="username" required />
							</div>
							<div class="col-12">
								<label for="email" class="form-label">Email</label>
								<input v-model="email" type="email" class="form-control" id="email" placeholder="johndoe@gmail.com" required />
							</div>
							<div class="col-12">
								<label for="password" class="form-label">Password</label>
								<input v-model="password" type="password" class="form-control" id="password" placeholder="*******" required />
							</div>
							<div class="col-12">
								<button type="submit" class="btn btn-primary">Register</button>
								Already registered? <router-link to="/login">Login here</router-link>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>
	<custom-footer />
</template>


