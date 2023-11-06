<template>
  <div class="card mood-card">
    <div class="card-body p-0" :style="backgroundStyle">
      <div class="mood-overlay" @click="toggleModal">
        <button class="btn btn-primary">{{ mood }}</button>
      </div>
    </div>
    <div v-if="isModalVisible" class="mood-modal">
      <div class="modal-overlay" @click="toggleModal"></div>
      <div class="modal-content">
        <span class="close" @click="toggleModal">&times;</span>
        <form @submit.prevent="submitForm">
          <p>You have selected: {{ mood }}</p>
          <div class="form-group">
            <label for="feedback">Your feedback:</label>
            <textarea id="feedback" class="form-control"></textarea>
          </div>
          <button type="submit" class="btn btn-success">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Mood',
  props: {
    mood: {
      type: String,
      required: true
    },
    selectionCount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      isModalVisible: false,
    };
  },
  computed: {
    backgroundStyle() {
      // Use the static path to your Django static files
      const imageUrl = `/src/images/${this.mood.toLowerCase()}.png`;
      return {
        backgroundImage: `url(${imageUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      };
    }
  },
  methods: {
    toggleModal() {
      this.isModalVisible = !this.isModalVisible;
    },
    submitForm() {
      // Handle the form submission
      console.log("Form submitted!");
    }
  }
};
</script>

<style scoped lang="scss">
  @import "/src/scss/components/mood.scss";
</style>
