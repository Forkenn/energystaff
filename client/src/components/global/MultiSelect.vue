<script setup>
import { ref, defineEmits, watch } from 'vue';

const props = defineProps({
  items: {
    type: Array,
    required: true,
    default: () => [],
  },
  placeholder: {
    type: String,
    default: 'Select items',
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  modelValue: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['update:modelValue']);
const selectedItems = ref([]);
const dataLoaded = ref(!props.isLoading);

watch(
  () => props.isLoading,
  () => {
    selectedItems.value = [...props.modelValue];
    dataLoaded.value = true;
  }
);

const isSelected = (item) => {
  return selectedItems.value.some(selected => selected.id === item.id);
};

const toggleCheck = (item) => {
  if (isSelected(item)) {
    selectedItems.value = selectedItems.value.filter(
      selected => selected.id !== item.id
    );
  } else {
    selectedItems.value = [...selectedItems.value, item];
  }
  emit('update:modelValue', selectedItems.value);
};

</script>

<template>
  <div class="multi-select position-relative">
    <div class="dropdown">
      <a class="btn btn-light btn-select dropdown-toggle sys-input-288" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
        {{ dataLoaded ? placeholder : 'Загрузка...' }}
      </a>
      <ul v-if="dataLoaded" class="dropdown-menu">
        <li v-for="item in items" :key="item.id" @click="toggleCheck(item)">
          <div class="dropdown-item">
            <div class="form-check">
              <input class="form-check-input sys-check-20" type="checkbox" value="" :id="'flexCheck-' + item.id" :checked="isSelected(item)">
              <label class="form-check-label" :for="'flexCheck-' + item.id">
                {{ item.name }}
              </label>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
  
<style scoped>
.btn-select {
  background-color: var(--bs-body-bg);
  border: var(--bs-border-width) solid var(--bs-border-color);
  transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
  align-content: center;
  text-align: left;
  --bs-form-select-bg-img: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/></svg>");;
  background-image: var(--bs-form-select-bg-img),var(--bs-form-select-bg-icon,none);
  background-repeat: no-repeat;
  background-position: right .75rem center;
  background-size: 16px 12px;
}

.btn-select:focus {
  border-color: #86b7fe;
  outline: 0;
  box-shadow: 0 0 0 .25rem rgba(13,110,253,.25);
}

.btn-select:hover {
  background-color: var(--bs-body-bg);
}

.dropdown-menu {
  width: 288px;
}

.dropdown-toggle::after {
  content: none;
}

.dropdown-item label {
  align-content: center;
  margin-bottom: 0;
}

</style>
