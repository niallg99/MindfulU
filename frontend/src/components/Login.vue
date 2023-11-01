<template>
  <div class="p-4 m-0 border-0 bd-example m-0 border-0">
    <h2>Login</h2>
    <form @submit.prevent="login" class="row g-3">
      <div class="col-12">
        <label for="login_username" class="form-label">Username</label>
        <input v-model="login_username" type="text" class="form-control" id="login_username" required />
      </div>
      <div class="col-12">
        <label for="login_password" class="form-label">Password</label>
        <input v-model="login_password" type="password" class="form-control" id="login_password" placeholder="*******" required />
      </div>
      <div class="col-12">
        <button type="submit" class="btn btn-primary">Login</button>
      </div>
    </form>
    <div class="mt-3">
      Not a member yet? <router-link to="/register">Register here</router-link>
    </div>
    <div v-if="errorMessage" class="mt-2 text-danger">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { loginUser } from '@/api/login';

export default {
  data() {
    return {
      login_username: '',
      login_password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const userData = {
          username: this.login_username,
          password: this.login_password
        };
        const response = await loginUser(userData);
        if (response.message) {
          // Handle successful login, maybe redirect to a dashboard or show a success message
          this.$router.push('/dashboard'); // Example redirection to a dashboard
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    }
  }
}
</script>

<style>
/* If there are any specific styles for the login form, add them here. */
</style>
