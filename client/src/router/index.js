import { watch } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignInView from '@/views/SignInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import AccountView from '@/views/AccountView.vue'
import NegotiationsView from '@/views/NegotiationsView.vue'
import ResumeEditorView from '@/views/ResumeEditorView.vue'
import ResumeView from '@/views/ResumeView.vue'
import CompanyEditorView from '@/views/CompanyEditorView.vue'
import CompanyView from '@/views/CompanyView.vue'
import VacancyEditorView from '@/views/VacancyEditorView.vue'
import VacancyView from '@/views/VacancyView.vue'
import VerificationView from '@/views/VerificationView.vue'
import RecommendationEditorView from '@/views/RecommendationEditorView.vue'
import AdminView from '@/views/AdminView.vue'

import { useUserStore } from '@/stores/user';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      meta: { requiresAuth: true },
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login_page',
      meta: {
        requiresAuth: false,
        authRedirect: true
       },
      component: SignInView,
    },
    {
      path: '/registration',
      name: 'registration_page',
      meta: {
        requiresAuth: false,
        authRedirect: true
      },
      component: SignUpView,
    },
    {
      path: '/account',
      name: 'account_page',
      meta: { requiresAuth: true },
      component: AccountView,
    },
    {
      path: '/negotiations',
      name: 'negotiations_page',
      meta: { requiresAuth: true },
      component: NegotiationsView,
    },
    {
      path: '/resume',
      name: 'resume_page',
      meta: { requiresAuth: true },
      component: ResumeView,
    },
    {
      path: '/resume/editor',
      name: 'resume_editor',
      meta: { requiresAuth: true },
      component: ResumeEditorView,
    },
    {
      path: '/company/:id',
      name: 'company_page',
      meta: { requiresAuth: true },
      component: CompanyView,
    },
    {
      path: '/company/editor',
      name: 'company_editor',
      meta: { requiresAuth: true },
      component: CompanyEditorView,
    },
    {
      path: '/vacancy/:id',
      name: 'vacancy_page',
      meta: { requiresAuth: true },
      component: VacancyView,
    },
    {
      path: '/vacancy/editor',
      name: 'vacancy_editor',
      meta: { requiresAuth: true },
      component: VacancyEditorView,
    },
    {
      path: '/edu/verification',
      name: 'edu_verification',
      meta: { requiresAuth: true },
      component: VerificationView,
    },
    {
      path: '/edu/recommendation/editor',
      name: 'edu_recommendation_editor',
      meta: { requiresAuth: true },
      component: RecommendationEditorView,
    },
    {
      path: '/control',
      name: 'control_page',
      meta: { requiresAuth: true },
      component: AdminView,
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  await userStore.getUser();

  if (userStore.isLoading) {
    const unwatch = watch(
      () => userStore.isLoading,
      (val) => {
        if (!val) {
          unwatch();
        }
      }
    )
  }

  if (to.meta.requiresAuth && !userStore.user.status.loggedIn) {
    next({ name: 'login_page' });
    return;
  }

  if (to.meta.authRedirect && userStore.user.status.loggedIn) {
    next({ name: 'home' });
    return;
  }

  next();
})

export default router
