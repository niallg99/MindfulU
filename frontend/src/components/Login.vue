<script>
import loginApi from '@/api/login';
import { jwtDecode } from 'jwt-decode';


export default {
	name: 'Login',
	data() {
	return {
		login_username: '',
		login_password: '',
		email: '',
		newPassword: '',
		errorMessage: '',
		verifyStage: false,
	};
},
	computed: {
		isLoggedIn() {
			return !!localStorage.getItem('accessToken');
		}
	},
	methods: {
		async login() {
			try {
				const csrfToken = await loginApi.getCSRFToken();
				const userData = {
					username: this.login_username,
					password: this.login_password,
				};
				const response = await loginApi.loginUser(userData, csrfToken);
				if (response.access_token) {
					localStorage.setItem('accessToken', response.access_token);
					const userId = jwtDecode(response.access_token).user_id;
					localStorage.setItem('userId', userId);
					localStorage.setItem('username', userData.username);
					this.$router.push('/dashboard');
				}
			} catch (error) {
				this.errorMessage = error.message;
			}
		},
		async verifyDetails() {
			try {
				const response = await loginApi.verifyUserDetails({ email: this.email });
				if (response.verified) {
					this.verifyStage = true;
				} else {
					throw new Error('Verification failed: Incorrect details');
				}
			} catch (error) {
				this.errorMessage = error.message;
			}
		},
		async resetPassword() {
			try {
				await loginApi.resetUserPassword(this.email, this.newPassword);
				this.verifyStage = false;
				this.$emit('close-modal');
			} catch (error) {
				this.errorMessage = error.message;
			}
		},
		closeModal() {
			let modal = document.getElementById('resetPasswordModal');
			if (modal) {
				let bsModal = bootstrap.Modal.getInstance(modal);
				if (bsModal) {
					bsModal.hide();
				}
			}
		}
	},
};
</script>
<template>
	<div class="full-page d-flex justify-content-center align-items-center">
		<div class="card login-card shadow">
			<div class="card-header text-center bg-transparent">
				<img src="/src/images/mental.svg" alt="Logo" style="width: 200px; height: auto;">
			</div>
			<div class="card-body">
				<form @submit.prevent="login" class="row g-3">
					<div class="col-12">
							<label for="login_username" class="form-label">Username</label>
							<input v-model="login_username" type="text" class="form-control" id="login_username" required />
					</div>
					<div class="col-12">
							<label for="login_password" class="form-label">Password</label>
							<input v-model="login_password" type="password" class="form-control" id="login_password" placeholder="*******" required />
					</div>
					<div class="col-12 text-center">
							<button type="submit" class="btn btn-primary">Login</button>
					</div>
				</form>
			</div>
			<div class="card-footer text-center">
				<div class="grid">
					<div>New around here? <router-link to="/register">Sign up</router-link></div>
					<div class="row"><a href="#" @click="preventDefault" data-bs-toggle="modal" data-bs-target="#resetPasswordModal">Forgot your password?</a></div>
				</div>
			</div>
			<div v-if="errorMessage" class="alert alert-danger text-center">
					{{ errorMessage }}
			</div>
		</div>
	</div>
	<div class="modal fade" id="resetPasswordModal" tabindex="-1" aria-labelledby="resetPasswordModalLabel" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="resetPasswordModalLabel">Reset Password</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<form v-if="!verifyStage" @submit.prevent="verifyDetails">
						<div class="mb-3">
							<label for="reset_email" class="col-form-label">Email:</label>
							<input type="email" class="form-control" id="reset_email" v-model="email" required>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
							<button type="submit" class="btn btn-primary">Verify</button>
						</div>
					</form>
					<form v-else @submit.prevent="resetPassword">
						<div class="mb-3">
							<label for="newPassword" class="col-form-label">New Password:</label>
							<input type="password" class="form-control" id="newPassword" v-model="newPassword" required>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" @click="verifyStage = false">Back</button>
							<button type="submit" class="btn btn-primary">Reset Password</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>
</template>