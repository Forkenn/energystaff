<script setup>
import { ref, watch, defineEmits, defineAsyncComponent } from 'vue';

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  modelValue: {
    type: Array,
    default: () => [],
  },
});

const DownloadIcon = defineAsyncComponent(() => import('../icons/DownloadIcon.vue'))

const emit = defineEmits(['update:modelValue']);
const accept = '.doc,.docx,.pdf,.jpg';
const maxSize = 10 * 1024 * 1024; // 10 MB
const fileInput = ref(null);
const files = ref([]);

watch(
  () => props.isLoading,
  () => {
    let locFiles = props.modelValue;
    for (const file of locFiles) {
      file.progress = 100;
      file.status = 'done'
    }
    files.value = locFiles;
    emit('update:modelValue', files.value);
  }
);

function triggerFileInput() {
  fileInput.value.click();
}

function handleDrop(e) {
  const droppedFiles = Array.from(e.dataTransfer.files);
  processFiles(droppedFiles);
}

function handleFileInput(e) {
  const inputFiles = Array.from(e.target.files);
  processFiles(inputFiles);
}

function processFiles(fileList) {
  for (const file of fileList) {
    if (file.size > maxSize || !accept.includes(file.name.split('.').pop().toLowerCase())) {
      files.value.push({ download_name: file.name, progress: 100, status: 'error' });
      emit('update:modelValue', files.value);
    } else {
      const fileObj = { data: file, download_name: file.name, progress: 0, status: 'uploading' };
      files.value.push(fileObj);
      emit('update:modelValue', files.value);
      const index = files.value.indexOf(fileObj);
      simulateUpload(index);
    }
  }
}

function simulateUpload(fileIndex) {
  const interval = setInterval(() => {
    const file = files.value[fileIndex];
    if (fileIndex === -1) {
      clearInterval(interval);
      return;
    }

    if (file.size > maxSize || !accept.includes(file.download_name.split('.').pop().toLowerCase())) {
      files.value[fileIndex] = { ...file, status: 'error', progress: 100 };
      clearInterval(interval);
      return;
    }

    if (file.progress >= 100) {
      clearInterval(interval);
      files.value[fileIndex] = { ...file, status: 'done' };
    } else {
      files.value[fileIndex] = { ...file, progress: file.progress + 10 };
    }
  }, 200);
}

function retryUpload(file) {
  file.progress = 0;
  file.status = 'uploading';
  const index = files.value.indexOf(file);
  simulateUpload(index);
}

function removeFile(index) {
  files.value.splice(index, 1);
}

const downloadFile = (realName, downloadName) => {
  const fileUrl = `${import.meta.env.BASE_URL}src/assets/storage/proof_documents/${realName}`

  const link = document.createElement('a');
  link.href = fileUrl;
  link.download = downloadName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

</script>

<template>
  <div class="upload-container">
    <div class="upload-dropzone" @dragover.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
      <input
        ref="fileInput"
        type="file"
        class="file-input"
        multiple
        :accept="accept"
        @change="handleFileInput"
      />
      <p>
        Нажмите или перетащите файлы в эту область.<br />
        <span class="hint">
          .doc .docx .pdf .jpg не более 10 мб
        </span>
      </p>
    </div>

    <div class="file-list">
      <div
        v-for="(file, index) in files"
        :key="file.download_name + index"
        class="file-item"
      >
        <div class="file-info">
          <p
            v-if="file.real_name"
            class="file-name downloadble"
            @click="downloadFile(file.real_name, file.download_name)"
          >
            {{ file.download_name }}
            <DownloadIcon style="width: 16px; height: 16px; fill: #7e7e7e;" />
          </p>
          <p v-else class="file-name">
            {{ file.download_name }}
          </p>
          <div class="progress-bar">
            <div
              class="progress"
              :class="file.status"
              :style="{ width: file.progress + '%' }"
            ></div>
          </div>
        </div>
        <div class="file-actions">
          <button v-if="file.status === 'error'" @click="retryUpload(file)" title="Повторить">
            ⟳
          </button>
          <button @click="removeFile(index)" title="Удалить">
            ✖
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-container {
  max-width: 900px;
  margin-bottom: 24px;
  font-family: "Montserrat";
}

.upload-dropzone {
  border: 2px dashed #ccc;
  background-color: #f5f5f5;
  padding: 2.5rem 1rem;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.upload-dropzone:hover {
  background-color: #e9e9e9;
}

.file-input {
  display: none;
}

.hint {
  font-size: 0.85rem;
  color: #888;
}

.file-list {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.downloadble {
  cursor: pointer;
  color: gray;
}

.downloadble:hover {
  color: black;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.progress {
  height: 100%;
  transition: width 0.3s ease;
}

.progress.uploading {
  background-color: #3490dc;
}

.progress.done {
  background-color: #38c172;
}

.progress.error {
  background-color: #e3342f;
}

.file-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 1rem;
}

.file-actions button {
  border: none;
  background: transparent;
  font-size: 1.1rem;
  cursor: pointer;
  color: #666;
  transition: color 0.2s ease;
}

.file-actions button:hover {
  color: #000;
}
</style>
