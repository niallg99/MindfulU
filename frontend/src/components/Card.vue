<template>
  <div class="card h-100">
    <div class="card-header">
      {{ header }}
    </div>
    <div class="card-body">
      {{ body }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    header: String,
    body: String
  },
};
</script>
