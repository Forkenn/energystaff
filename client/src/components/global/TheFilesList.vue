<script setup>
import { defineProps, defineAsyncComponent } from 'vue'

const PdfIcon = defineAsyncComponent(() => import('../icons/PdfIcon.vue'))
const DocIcon = defineAsyncComponent(() => import('../icons/DocIcon.vue'))
const ImageIcon = defineAsyncComponent(() => import('../icons/ImageIcon.vue'))
const DefaultIcon = defineAsyncComponent(() => import('../icons/FileIcon.vue'))
const DownloadIcon = defineAsyncComponent(() => import('../icons/DownloadIcon.vue'))

const props = defineProps({
	files: {
		type: Array,
		required: true,
	},
})

function getIconComponent(filename) {
	const ext = filename.split('.').pop().toLowerCase()
	switch (ext) {
		case 'pdf':
			return PdfIcon
		case 'doc':
		case 'docx':
			return DocIcon
		case 'jpg':
		case 'jpeg':
		case 'png':
			return ImageIcon
		default:
			return DefaultIcon
	}
}

function formatSize(bytes) {
	return `${(bytes / 1024 / 1024).toFixed(2)} MB`
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
	<div class="list-group">
		<div
			v-for="file in files"
			:key="file.id"
			class="list-group-item d-flex justify-content-between align-items-center"
		>
			<div class="d-flex align-items-center">
				<component
					:is="getIconComponent(file.download_name)"
					class="me-3"
					style="width: 32px; height: 32px; fill: #b5b5b5;"
				/>
				<div>
					<div class="fw-semibold">{{ file.download_name }}</div>
					<div class="text-muted small">{{ formatSize(file.size) }}</div>
				</div>
			</div>

			<a
				href="#"
				download
				class="text-decoration-none"
				title="Скачать"
				@click.prevent="downloadFile(file.real_name, file.download_name)"
			>
				<DownloadIcon style="width: 20px; height: 20px; fill: #7e7e7e;" />
			</a>
		</div>
	</div>
</template>

<style scoped>
.fw-semibold {
	font-family: "Montserrat" !important;
}
</style>