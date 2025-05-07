<script setup>
import { ref, defineEmits, watch } from 'vue';
import { debounce } from '@/composables/useDebounce';

const props = defineProps({
  callback: {
    type: Function,
    required: true,
    validator: (value) => typeof value === 'function',
  },
  modelValue: {
    type: Object,
    default: () => null,
  },
  placeholder: {
    type: String,
    default: () => 'Наименование ОУ',
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const searchQuery = ref('');
const objects = ref([]);
const isLoading = ref(false);

watch(
  () => props.isLoading,
  () => {
    if(props.modelValue)
      searchQuery.value = props.modelValue.name;
  }
);

const debouncedSearch = debounce(async () => {
  if (searchQuery.value.length > 2) {
    await fetchObjects();
  } else {
    objects.value = [];
  }
}, 300);

const onSearchInput = (event) => {
  searchQuery.value = event.target.value;
  debouncedSearch();
  const found = objects.value.find(inst => inst.name === searchQuery.value);
  emit('update:modelValue', found || null);
};

const fetchObjects = async () => {
  isLoading.value = true;
  try {
    const params = { q: searchQuery.value }
    const response = await props.callback(params)
    objects.value = response.data.items;
  } catch (err) {
    console.log(err)
    alert('Ошибка при загрузке учебных заведений');
    objects.value = [];
  } finally {
    isLoading.value = false;
  }
};

const selectObject = (item) => {
  emit('update:modelValue', item);
  searchQuery.value = item.name;
}

</script>

<template>
  <div class="dropdown">
    <input
      class="form-control form-text-field sys-input-288"
      type="text form-text-field"
      :placeholder="props.placeholder"
      :aria-label="props.placeholder"
      data-bs-toggle="dropdown"
      id="edu-institution-input"
      v-model="searchQuery"
      @input="onSearchInput"
      :title="searchQuery"
      :disabled="disabled"
    >
    <ul class="dropdown-menu">
      <li
        v-for="object in objects"
        :key="object.id"
      >
        <a
          class="dropdown-item text-truncate"
          :id="'dropdownItem-' + object.id"
          href="#"
          @click.prevent="selectObject(object)"
          :title="object.name"
        >
          {{ object.name }}
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.dropdown-menu {
  width: 288px;
  overflow-x: auto;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

.dropdown-menu::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.dropdown-menu::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.dropdown-menu::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.dropdown-menu::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.dropdown-toggle::after {
  content: none;
}

.dropdown-item label {
  align-content: center;
  margin-bottom: 0;
}
</style>