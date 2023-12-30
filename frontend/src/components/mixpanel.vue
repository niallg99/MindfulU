<template>
  <div>
    <canvas id="myChart" width="400" height="400"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'AnalyticsChart',
  data() {
    return {
      chart: null,
    };
  },
  methods: {
    async fetchData() {
      // Fetch data from your backend or Mixpanel
      // For example, this could be an array of objects: [{component: 'ComponentName', count: 10}, ...]
      const dataFromBackend = await this.getEventData();

      this.renderChart(dataFromBackend);
    },
    renderChart(data) {
      const ctx = document.getElementById('myChart').getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.component),
          datasets: [{
            label: 'Number of Mounts',
            data: data.map(item => item.count),
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },
    async getEventData() {
      // Placeholder: Replace with actual call to your backend or Mixpanel
      return [
        { component: 'Profile', count: 5 },
        { component: 'Dashboard', count: 8 },
        { component: 'Settings', count: 3 }
      ];
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>
