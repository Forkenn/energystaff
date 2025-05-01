<script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    total: Number,
    perPage: {
			type: Number,
			default: 6
		},
    page: {
			type: Number,
			default: 1
		},
  })

  const emit = defineEmits(['update:page'])
  
  const currentPage = computed(() => props.page)
  const totalPages = computed(() => Math.ceil(props.total / props.perPage))
  
  const changePage = (page) => {
    if (page === '...' || page === currentPage.value) return
    emit('update:page', page)
  }
  
  const visiblePages = computed(() => {
    const pages = []
    const total = totalPages.value
    const current = currentPage.value
  
    if (total <= 9) {
      for (let i = 1; i <= total; i++) pages.push(i)
    } else {
      pages.push(1)
      if (current > 4) pages.push('...')
      for (
        let i = Math.max(2, current - 2);
        i <= Math.min(total - 1, current + 2);
        i++
      ) {
        pages.push(i)
      }
      if (current < total - 3) pages.push('...')
      pages.push(total)
    }
  
    return pages
  })
</script>

<template>
	<nav aria-label="Навигация" v-if="totalPages > 1">
		<ul class="pagination justify-content-center">
			<li class="page-item" :class="{ disabled: currentPage === 1 }">
				<a class="page-link" aria-label="Предыдущая" @click="changePage(currentPage - 1)">
					<span aria-hidden="true">&laquo;</span>
				</a>
			</li>
			<li
				v-for="page in visiblePages"
				:key="page"
				:class="['page-item', { active: page === currentPage, disabled: page === '...' }]"
			>
				<button class="page-link" @click="changePage(page)" :disabled="page === '...'">{{ page }}</button>
			</li>
			<li class="page-item" :class="{ disabled: currentPage === totalPages}">
				<a class="page-link" aria-label="Следующая" @click="changePage(currentPage + 1)">
					<span aria-hidden="true">&raquo;</span>
				</a>
			</li>
		</ul>
	</nav>
</template>
