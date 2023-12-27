<script>
export default {
  name: 'Spinner'
};
</script>

<template>
  <div class="spinner"></div>
</template>

<style scoped>
.spinner {
  border: 5px solid #f3f3f3; /* Light grey border */
  border-top: 5px solid #3498db; /* Blue border */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
