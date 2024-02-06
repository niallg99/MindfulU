<script>
import { updateMood, deleteMood } from '@/api/moods';

export default {
    props: {
      mood: Object,
      showModal: Boolean,
      moodChoices: Array,
      moodCauses: Array,
    },
    data() {
        return {
            editedMood: {},
            saveError: '',
        };
    },
    watch: {
      mood(newVal) {
        this.editedMood = { ...newVal, mood_cause: newVal.mood_cause};
      },
    },
  methods: {
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
        this.$emit('close-modal');
    },
    async saveChanges() {
      try {
        const updatedMood = await updateMood(this.editedMood.id, this.editedMood);
        this.$emit('update-mood', updatedMood); 
        this.hide();
      } catch (error) {
            console.error('Error updating mood:', error);
            this.saveError = 'Failed to update mood. Please try again.';
        }
    },
    async deleteMood() {
        try {
            await deleteMood(this.editedMood.id);
            this.$emit('delete', this.editedMood.id);
            this.hide();
        } catch (error) {
            console.error('Error deleting mood:', error);
            this.saveError = 'Failed to delete mood. Please try again.';
        }
    }
  },
  computed: {
    shouldShowMoodCauses() {
      return this.editedMood.mood_type !== 'Happy';
    },
  },
};
</script>
<template>
  <div class="modal fade" id="moodModal" tabindex="-1" aria-labelledby="moodModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="moodModalLabel">Edit Mood</h5>
          <button type="button" class="btn-close" @click="hide" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveChanges">
            <div class="form-group mb-3">
              <label for="moodType">Mood Type:</label>
              <select id="moodType" class="form-control" v-model="editedMood.mood_type">
                <option v-for="mood in moodChoices" :key="mood" :value="mood">{{ mood }}</option>
              </select>
            </div>
            <div class="form-group mb-3" v-if="shouldShowMoodCauses">
              <label for="moodCause">Mood Cause:</label>
              <select id="moodCause" class="form-control" v-model="editedMood.mood_cause">
                <option v-for="cause in moodCauses" :key="cause" :value="cause">{{ cause }}</option>
              </select>
            </div>
            <div class="form-group mb-3">
              <label for="description">Description:</label>
              <textarea id="description" class="form-control" v-model="editedMood.description"></textarea>
            </div>
            <div v-if="saveError" class="alert alert-danger">{{ saveError }}</div>
            <div class="modal-footer">
              <button type="button" class="btn btn-danger" @click="deleteMood">Delete</button>
              <button type="button" class="btn btn-secondary" @click="hide">Close</button>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

