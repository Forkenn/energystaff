import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignInView from '@/views/SignInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import AccountView from '@/views/AccountView.vue'
import NegotiationsView from '@/views/NegotiationsView.vue'
import ResumeEditorView from '@/views/ResumeEditorView.vue'
import CompanyEditorView from '@/views/CompanyEditorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login_page',
      component: SignInView,
    },
    {
      path: '/registration',
      name: 'registration_page',
      component: SignUpView,
    },
    {
      path: '/account',
      name: 'account_page',
      component: AccountView,
    },
    {
      path: '/negotiations',
      name: 'negotiations_page',
      component: NegotiationsView,
    },
    {
      path: '/resume/editor',
      name: 'resume_editor',
      component: ResumeEditorView,
    },
    {
      path: '/company/editor',
      name: 'company_editor',
      component: CompanyEditorView,
    },
  ],
})

export default router
