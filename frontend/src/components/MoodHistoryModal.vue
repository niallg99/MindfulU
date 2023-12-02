<template>
  <div class="modal fade" id="moodModal" tabindex="-1" aria-labelledby="moodModalLabel" aria-hidden="true" v-show="showModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="moodModalLabel">Edit Mood</h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveChanges">
            <div class="form-group mb-3">
              <label for="moodType">Mood Type:</label>
              <select id="moodType" class="form-control" v-model="editedMood.mood_type">
								<option v-for="mood in moodChoices" :key="mood" :value="mood">{{ mood }}</option>
							</select>
            </div>
            <div class="form-group mb-3">
              <label for="description">Description:</label>
              <textarea id="description" class="form-control" v-model="editedMood.description"></textarea>
            </div>
            <div v-if="saveError" class="alert alert-danger">{{ saveError }}</div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="deleteMood">Delete</button>
          <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { updateMood, deleteMood } from '@/api/moods';

export default {
  props: {
    mood: Object,
    showModal: Boolean,
    moodChoices: Array
  },
  data() {
    return {
      editedMood: {},
      saveError: '',
    };
  },
  watch: {
    mood(newVal) {
      this.editedMood = { ...newVal };
    }
  },
  methods: {
    initializeModal() {
      const modalElement = document.getElementById('moodModal');
      this.modalInstance = new bootstrap.Modal(modalElement, {
        backdrop: 'static',
        keyboard: false
      });
      if (this.showModal) {
        this.modalInstance.show();
      }
    },
    closeModal() {
      if (this.modalInstance) {
        this.modalInstance.hide();
      }
      this.$emit('close');
    },
    async saveChanges() {
      try {
        const updatedMood = await updateMood(this.editedMood.id, this.editedMood);
        this.$emit('save', updatedMood);
        this.closeModal();
      } catch (error) {
        console.error('Error updating mood:', error);
        this.saveError = 'Failed to update mood. Please try again.';
      }
    },
    async deleteMood() {
      try {
        await deleteMood(this.editedMood.id);
        this.$emit('delete', this.editedMood.id);
        this.closeModal();
      } catch (error) {
        console.error('Error deleting mood:', error);
        this.saveError = 'Failed to delete mood. Please try again.';
      }
    }
  },
  mounted() {
    this.initializeModal();
  }
};
</script>