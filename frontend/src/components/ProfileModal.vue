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
            <img :src="profilePicture" @error="imageLoadError" class="rounded-circle" alt="Profile Picture" style="width: 100px; height: 100px;">
          </div>
          <div class="mb-3">
            <label for="profilePicture" class="form-label">Update Profile Picture</label>
            <input type="file" class="form-control" id="profilePicture" accept=".png, .jpeg, .jpg" @change="handleFileUpload">
          </div>
          <div class="mb-3 d-flex align-items-center">
            <label for="showMood" class="form-label me-2">Show most recent mood to friends</label>
            <div class="form-check form-switch mb-0">
              <input class="form-check-input" type="checkbox" id="showMood" v-model="localShowMood">
              <label class="form-check-label" for="showMood"></label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="updateProfile">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { updateProfile, saveShowMoodPreference } from '@/api/profile.js';

export default {
  name: 'ProfileModal',
  props: {
    userProfilePicture: {
      type: String,
      default: ''
    },
    showMood: {
      type: Boolean,
      default: true
    },
  },
   data() {
    return {
      selectedFile: null,
      localShowMood: this.showMood,
      localUserProfilePicture: this.userProfilePicture || '/src/images/person.svg',
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
        this.selectedFile = file;
      } else {
        alert("Please select a .png or .jpeg file.");
        event.target.value = "";
      }
    },
    async updateProfile() {
      try {
        let formData = new FormData();
        if (this.selectedFile) {
          formData.append('file', this.selectedFile);
        }
        const response = await updateProfile(formData);
        if (response.newProfilePictureUrl) {
          this.localUserProfilePicture = response.newProfilePictureUrl;
          this.$emit('profile-updated', response.newProfilePictureUrl);
        }
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
    async updateShowMoodPreference() {
      try {
        await saveShowMoodPreference(this.localShowMood);
        localStorage.setItem('showMood', this.localShowMood);
        this.$emit('showMood-updated', this.localShowMood);
      } catch (error) {
        console.error('Error saving showMood preference:', error);
      }
    },
       show() {
      if (this.modalInstance) {
        this.modalInstance.show();
      }
    },
    hide() {
      if (this.modalInstance) {
        this.modalInstance.hide();
      }
    },
      imageLoadError(event) {
    event.target.src = '/src/images/person.svg';
  },
  },
  watch: {
    userProfilePicture(newVal) {
      this.localUserProfilePicture = newVal || '/src/images/person.svg';
    },
    localShowMood(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.updateShowMoodPreference();
      }
    },
    showMood(newVal) {
      this.localShowMood = newVal;
    }
  },
  mounted() {
    this.$nextTick(() => {
      const modalElement = this.$el;
      if (modalElement) {
        this.modalInstance = new bootstrap.Modal(modalElement, {
          keyboard: false
        });
      }
    });
  },
  computed: {
    profilePicture() {
      return this.localUserProfilePicture ? this.localUserProfilePicture : '/src/images/person.svg';
    }
},



};
</script>
