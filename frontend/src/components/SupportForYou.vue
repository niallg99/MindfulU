<template>
  <div>
    <h2>Support For You</h2>
    <div class="accordion" id="supportAccordion">
      <div
        class="accordion-item"
        v-for="section in supportSections"
        :key="section.id"
      >
        <h3 class="accordion-header" :id="`${section.id}-accordion-label`">
          <button
            class="accordion-button"
            type="button"
            data-bs-toggle="collapse"
            :data-bs-target="`#${section.id}-accordion-content`"
            aria-expanded="false"
          >
            {{ section.title }}
          </button>
        </h3>
        <div
          :id="`${section.id}-accordion-content`"
          class="accordion-collapse collapse"
          :aria-labelledby="`${section.id}-accordion-label`"
        >
          <div class="accordion-body">
            <ul class="list-unstyled"> <!-- Use Bootstrap's list-unstyled class to remove bullet points -->
              <li v-for="link in section.links" :key="link.url">
                <a :href="link.link_url" target="_blank">{{ link.link_text }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Import the fetchSupport function from your API
import { fetchSupport } from '@/api/supportforyou.js';

export default {
  data() {
    return {
      supportSections: [],
    };
  },
  methods: {
    async loadSupportData() {
      try {
        // Fetch data from the API
        const response = await fetchSupport();
        this.supportSections = response;
      } catch (error) {
        console.error('Error fetching support data:', error);
      }
    },
  },
  mounted() {
    this.loadSupportData();
  },
};
</script>

<style scoped>
/* Add scoped styles for the component */
.accordion-item {
  max-width: 800px; /* Adjust the max-width to your preferred width */
  margin-bottom: 10px; /* Add margin to separate items */
}
</style>
