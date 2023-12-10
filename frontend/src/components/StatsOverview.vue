<template>
  <div class="stats-overview mt-4">
    <div class="card">
      <div class="card-header">Overview</div>
      <div class="card-body">
        <p>Average Mood: {{ averageMood }}</p>
        <p>Active Users: {{ activeUsers }}</p>
        <p>Most Provided Mood Cause: {{ mostProvidedMoodCause }}</p>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    averageMood: {
      type: String,
      default: null
    },
    activeUsers: {
      type: Number,
      default: null
    },
    mostProvidedMoodCause: {
      type: String,
      default: null
    },
  },
};
</script>
<style scoped>
.stats-overview {
    display: flex;
	justify-content: center;
	margin: 0 auto;
	width: 80%;
}


.card-body {
  /* Your styles for body */
  padding: 15px;
}
</style>
