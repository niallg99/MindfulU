<template>
	<div v-if="show" ref="userModal" class="modal fade" tabindex="-1" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">User Details</h5>
					<button type="button" class="btn-close" @click="hide"></button>
				</div>
				<div class="modal-body">
          <p v-if="userDetails">Email: {{ userDetails.email }}</p>
          <p v-if="userDetails">Phone: {{ phone }}</p>
          <p v-else>Loading user details...</p>
        </div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" @click="hide">Close</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
  props: {
    userDetails: {
      type: Object,
      default: () => {}
    },
    phone: {
      type: String,
      default: ''
    },
  },
  mounted() {
    this.modalInstance = new bootstrap.Modal(this.$refs.userModal, {
      keyboard: false
    });
  },
  methods: {
    show() {
      this.modalInstance.show();
    },
    hide() {
      this.modalInstance.hide();
    }
  },
  watch: {
    userDetails(newVal) {
      if (newVal) {
        this.show();
      } else {
        this.hide();
      }
    }
  },
};
</script>
