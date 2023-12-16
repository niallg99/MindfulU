<template>
	<div class="container mt-4">
		<div class="row justify-content-center">
			<div class="col-lg-12">
				<div class="card panel-card">
					<div class="card-header">
						Support For You
					</div>
					<div class="card-body">
						<div v-if="isLoading">
							<spinner />
						</div>
						<div v-else>
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
						</div>
					</div>
					<div class="card-footer text-center">
						<button class="btn btn-primary" @click="navigateToSupportForYou">See More Support Options</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { useRouter } from 'vue-router';
import Spinner from './Spinner.vue';

export default {
	name: 'SupportPanel',
	components: {
		Spinner,
	},
	props: {
		supportSections: Array,
		isLoading: Boolean,
	},
	data() {
		return {
			collapsed: null,
		};
	},
	computed: {
		limitedSupportSections() {
			return this.supportSections.slice(0, 5);
		},
	},
	methods: {
		toggleCollapse(index) {
			this.collapsed = this.collapsed === index ? null : index;
		},
	},
	setup() {
		const router = useRouter();
		const navigateToSupportForYou = () => {
			router.push('/support');
		};
		return { navigateToSupportForYou };
	},
};
</script>
