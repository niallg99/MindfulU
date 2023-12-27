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

<template>
  <div class="page-container">
    <navbar :is-logged-in="isLoggedIn" />
    <div class="container mt-4">
      <div class="card shadow padding-1">
        <div class="card-title">
          <h1 class="card-title">Support Resources</h1>
        </div>
        <div class="card-body">
          <p class="card-text">Find helpful resources and links to support your mental and emotional well-being.</p>
          <div class="accordion" id="supportAccordion">
            <div
              class="accordion-item"
              v-for="(section, index) in supportSections"
              :key="section.id"
            >
              <h2 class="accordion-header" :id="`heading${index}`">
                <button
                  class="accordion-button"
                  type="button"
                  :class="{ 'collapsed': collapsed !== index }"
                  @click="toggleCollapse(index)"
                >
                  {{ section.title }}
                </button>
              </h2>
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
      </div>
    </div>
    <custom-footer />
  </div>
</template>




<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.container {
  flex: 1;
  max-width: 90%;
  margin: auto;
}

.card {
  margin-top: 2rem;
}

.card-header {
  background-color: #f8f9fa;
}

.accordion-button {
  padding: 0.75rem 1.25rem;
}

@media (max-width: 768px) {
  .accordion-button {
    padding: 0.5rem 1rem;
  }
}

.custom-footer {
  margin-top: auto;
}
</style>



