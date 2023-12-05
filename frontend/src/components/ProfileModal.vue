<template>
	<div class="modal fade" id="profileModal" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="profileModalLabel">Profile</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<div class="text-center mb-3">
						<img :src="userProfilePicture || '/src/images/person.svg'" class="rounded-circle" alt="Profile Picture" style="width: 100px; height: 100px;">
					</div>
					<div class="mb-3">
						<label for="profilePicture" class="form-label">Update Profile Picture</label>
						<input type="file" class="form-control" id="profilePicture" @change="handleFileUpload">
					</div>
					<label for="profilePicture" class="form-label">Update Privacy Settings</label>
				<div class="form-check">
						<input 
							class="form-check-input" 
							type="checkbox" 
							id="showMood" 
							:checked="showMood" 
							@change="$emit('update:showMood', $event.target.checked)"
						>
						<label class="form-check-label" for="showMood">
							Show most recent mood to friends
						</label>
				</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
					<button type="button" class="btn btn-primary" @click="updateProfile">Save Changes</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'ProfileModal',
	props: {
		userProfilePicture: String,
		showMood: Boolean,
	},
	data() {
		return {
			selectedFile: null,
		};
	},
	methods: {
		handleFileUpload(event) {
			this.selectedFile = event.target.files[0];
		},
		async updateProfile() {
				const formData = new FormData();
				formData.append('profilePicture', this.selectedFile);
				formData.append('showMood', this.showMood);
				try {
						const response = await fetch('/api/user/profile', {
						method: 'POST',
						body: formData,
						});
						if (response.ok) {
							this.$emit('profile-updated');
						} else {
							const error = await response.json();
							throw new Error(error.message);
						}
				} catch (error) {
						console.error(error);
				}
		},
		show() {
			const modalElement = this.$el;
			this.modalInstance = new bootstrap.Modal(modalElement, {
				keyboard: false
			});
			this.modalInstance.show();
		},
		hide() {
			if (this.modalInstance) {
				this.modalInstance.hide();
			}
		},
	},
};
</script>

