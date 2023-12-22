<template>
  <div class="page-container">
    <navbar :is-logged-in="isLoggedIn" />
    <div class="main-container-support">
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
    <custom-footer />
  </div>
</template>

<script>
import { fetchSupport } from '@/api/supportforyou.js';
import Navbar from './Navbar.vue';
import CustomFooter from './CustomFooter.vue';

export default {
  components: {
    Navbar,
    CustomFooter,
  },
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
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-container-support {
  justify-content: center;
  flex-grow: 1;
  padding: 20px;
}

.accordion {
  width: 100%;
  margin: 0 auto;
  margin-top: 15%;
}

@media (max-width: 768px) {
  .accordion-button {
    padding: 0.5rem 1rem;
  }

  .main-container {
    padding: 10px;
  }

  .accordion {
    width: 100%; /* Keep full width for smaller screens */
  }
}

.footer {
  width: 100%;
  margin-top: auto;
}
</style>

