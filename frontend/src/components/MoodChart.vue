<template>
  <div class="mood-chart-container">
    <div class="card">
      <h5 class="card-header">Mood Analytics</h5>
      <div class="card-body">
        <div class="chart-container">
          <canvas ref="barChartCanvas"></canvas>
        </div>
				<!-- <canvas ref="donutChartCanvas"></canvas> Donut chart canvas -->
      </div>
    </div>
  </div>
</template>



<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
	props: {
		 moodData: {
    type: Array,
    required: true,
    default: () => []
  },
  moodCauseData: {
    type: Array,
    required: true,
    default: () => []
  }
	},
	data() {
		return {
			chartInstance: null,
			donutChartInstance: null,
		};
	},
	 mounted() {
    this.$nextTick(() => {
      if (this.$refs.barChartCanvas) {
        this.createBarChart();
      }
      if (this.$refs.donutChartCanvas) {
        this.createDonutChart();
      }
    });
  },
	methods: {
		createBarChart() {
			if (this.chartInstance) {
				this.chartInstance.destroy();
			}
		const ctx = this.$refs.barChartCanvas.getContext('2d');
		this.chartInstance = new Chart(ctx, {
				type: 'bar',
				data: {
						labels: this.moodData.map(data => data.mood_type),
						datasets: [{
						label: 'Moods',
						data: this.moodData.map(data => data.count),
						backgroundColor: [
								'rgba(255, 99, 132, 0.2)',
								'rgba(54, 162, 235, 0.2)',
								'rgba(255, 206, 86, 0.2)',
								'rgba(75, 192, 192, 0.2)',
						],
						borderColor: [
								'rgba(255, 99, 132, 1)',
								'rgba(54, 162, 235, 1)',
								'rgba(255, 206, 86, 1)',
								'rgba(75, 192, 192, 1)',
						],
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
	 createDonutChart() {
      if (this.donutChartInstance) {
        this.donutChartInstance.destroy();
      }
      const ctx = this.$refs.donutChartCanvas.getContext('2d');
      this.donutChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: this.moodCauseData.map(data => data.cause),
          datasets: [{
            label: 'Mood Causes',
            data: this.moodCauseData.map(data => data.count),
            backgroundColor: [
              // Add more colors for different mood causes
              'rgba(255, 99, 132, 0.5)',
              'rgba(54, 162, 235, 0.5)',
              'rgba(255, 206, 86, 0.5)',
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        }
      });
    }
  },
  watch: {
		moodData(newData) {
			if (newData) {
				this.createBarChart();
			}
		},
    moodCauseData(newData) {
      if (newData) {
        this.createDonutChart();
      }
    }
  }
};
</script>

<style scoped>
.mood-chart-container {
  display: flex;
  justify-content: center;
  margin: 0 auto;
  width: 80%;
}

.chart-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
</style>

