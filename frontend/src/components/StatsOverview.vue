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

<template>
  <div class="stats-overview mt-4">
    <div class="card">
      <div class="card-header">Overview</div>
      <div class="card-body text-center">
        <div class="info-card ">
          <div class="info-card-header">Average Mood</div>
          <div class="info-card-content">{{ averageMood }}</div>
        </div>
        <div class="info-card">
          <div class="info-card-header">Active Users</div>
          <div class="info-card-content">{{ activeUsers }}</div>
        </div>
        <div class="info-card">
          <div class="info-card-header">Most Provided Mood Cause</div>
          <div class="info-card-content">{{ mostProvidedMoodCause }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-overview {
  display: flex;
  justify-content: center;
  margin: 0 auto;
  width: 80%;
}

.card-body {
  display: flex;
  justify-content: space-between;
  padding: 15px;
}

.info-card {
  background-color: #afcfd6;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  width: 30%;
}

.info-card-header {
  font-weight: bold;
}

.info-card-content {
  /* Your styles for content */
}
</style>
