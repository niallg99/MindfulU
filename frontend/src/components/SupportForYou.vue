<template>
  <div>
    <h2>Support For You</h2>
    <div class="accordion" id="supportAccordion">
      <div
        class="accordion-item"
        v-for="(section, index) in supportSections"
        :key="section.id"
      >
        <h3 class="accordion-header" :id="`heading${index}`">
          <button
            class="accordion-button"
            type="button"
            :class="{ 'collapsed': collapsed !== index }"
            @click="toggleCollapse(index)"
          >
            {{ section.title }}
          </button>
        </h3>
        <div
          :id="`collapse${index}`"
          class="accordion-collapse collapse"
          :class="{ 'show': collapsed === index }"
          :aria-labelledby="`heading${index}`"
        >
          <div class="accordion-body">
            <ul class="list-unstyled">
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
import { fetchSupport } from '@/api/supportforyou.js';

export default {
  data() {
    return {
      supportSections: [],
      collapsed: null,
    };
  },
  methods: {
    async loadSupportData() {
      try {
        const response = await fetchSupport();
        this.supportSections = response;
      } catch (error) {
        console.error('Error fetching support data:', error);
      }
    },
    toggleCollapse(index) {
      this.collapsed = this.collapsed === index ? null : index;
    },
  },
  mounted() {
    this.loadSupportData();
  },
};
</script>

<style scoped>
.accordion-item {
  max-width: 800px;
  margin-bottom: 10px;
}
</style>