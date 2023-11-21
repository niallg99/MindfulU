<template>
	<div class="container mt-4">
		<div class="row justify-content-center">
			<div class="col-lg-12">
				<div class="card">
					<div class="card-header">
						Support For You
					</div>
					<div class="card-body">
						<div class="accordion" id="supportAccordion">
							<div
								class="accordion-item"
								v-for="(section, index) in limitedSupportSections"
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
						<button class="btn btn-primary mt-3" @click="navigateToSupportForYou">See More Support Options</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { fetchSupport } from '@/api/supportforyou.js';
import { useRouter } from 'vue-router';

export default {
	name: 'SupportPanel',
	setup() {
		const router = useRouter();
		const navigateToSupportForYou = () => {
			router.push('/support');
		};
		return { navigateToSupportForYou };
	},
	data() {
		return {
			supportSections: [],
			collapsed: null,
		};
	},
	computed: {
		limitedSupportSections() {
			return this.supportSections.slice(0, 3);
		},
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
.support-panel .accordion-item {
	max-width: 800px;
	margin-bottom: 10px;
}
</style>
