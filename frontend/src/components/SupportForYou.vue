<template>
  <div>
    <h2>Support For You</h2>
    <ul>
      <li v-for="section in supportSections" :key="section.id">
        <a
          v-if="section.link_url === ''"
          :href="section.url"
          target="_blank"
          class="accordion-title"
          aria-controls="i5wdcr-accordion"
          :id="`${section.id}-accordion-label`"
          aria-expanded="false"
        >
          {{ section.link_text }}
        </a>
        <div
          v-else
          class="accordion-content"
          :data-tab-content="section.id"
          role="region"
          :aria-labelledby="`${section.id}-accordion-label`"
          aria-hidden="true"
          :id="section.id"
        >
          <ul class="links-ul arrows-primary">
            <li v-for="link in section.links" :key="link.id">
              <a :href="link.link_url" target="_blank">{{ link.link_text }}</a>
            </li>
          </ul>
        </div>
      </li>
    </ul>
  </div>
</template>

<template>
  <div>
    <h2>Support For You</h2>
    <ul>
      <li v-for="section in supportSections" :key="section.id">
        <a
          v-if="!section.links.length"
          :href="section.url"
          target="_blank"
          class="accordion-title"
          aria-controls="i5wdcr-accordion"
          :id="`${section.id}-accordion-label`"
          aria-expanded="false"
        >
          {{ section.title }}
        </a>
        <div
          v-else
          class="accordion-content"
          :data-tab-content="section.id"
          role="region"
          :aria-labelledby="`${section.id}-accordion-label`"
          aria-hidden="true"
          :id="section.id"
        >
          <ul class="links-ul arrows-primary">
            <li v-for="link in section.links" :key="link.url">
              <a :href="link.url" target="_blank">{{ link.text }}</a>
            </li>
          </ul>
        </div>
      </li>
    </ul>
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
  mounted() {
    this.loadSupportData();
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
};
</script>

<style>
/* Add your component's styles here */
</style>
