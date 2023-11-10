<script>
import loginApi from '@/api/login';

export default {
  data() {
    return {
      login_username: '',
      login_password: '',
      reset_email: '',
      errorMessage: '',
      isStaffLogin: false,
      isLoggedIn: false
    };
  },
  methods: {
    handleStaffLoginToggle(newValue) {
      this.isStaffLogin = newValue;
    },
    async login() {
      try {
        const csrfToken = await loginApi.checkCSRFToken();
        const userData = {
          username: this.login_username,
          password: this.login_password
        };
        const response = await loginApi.loginUser(userData, csrfToken);
        if (response.message) {
          this.isLoggedIn = true;
          this.$emit('login-success', this.isLoggedIn);
          this.$router.push('/dashboard');
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async resetPassword() {
      if (!this.reset_email) {
        this.errorMessage = 'Please enter your email address.';
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.reset_email)) {
        this.errorMessage = 'Please enter a valid email address.';
        return;
      }

      try {
        this.errorMessage = '';
        const csrfToken = await loginApi.checkCSRFToken();
        const response = await loginApi.resetUserPassword(this.reset_email, csrfToken);
        console.log(response.message);
      } catch (error) {
        this.errorMessage = error.message || 'Failed to reset password.';
      }
    },
    preventDefault(event) {
      event.preventDefault();
    },
  }
}
</script>

<template>
  <Navbar :is-logged-in="isLoggedIn" :is-staff-login="isStaffLogin" @update:isStaffLogin="handleStaffLoginToggle"/>
  <div class="full-page d-flex justify-content-center align-items-center">
    <div class="card login-card shadow">
      <div v-if="isStaffLogin" class="card-header staff-header text-center text-white">
        Staff Login
      </div>
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
				New around here? <router-link to="/register">Sign up</router-link><br>
				<a href="#" @click="preventDefault" data-bs-toggle="modal" data-bs-target="#resetPasswordModal">Forgot your password?</a>
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
					<form @submit.prevent="resetPassword">
						<div class="mb-3">
							<label for="reset_email" class="col-form-label">Email:</label>
							<input type="email" class="form-control" id="reset_email" v-model="reset_email" required>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
							<button type="submit" class="btn btn-primary">Send Reset Link</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>
	<CustomFooter />
</template>