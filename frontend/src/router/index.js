import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {path: '/', component: () => import('../views/Home.vue')},
  {path: '/Login', component: () => import ('../views/Login.vue')},
  {path: '/register', component: () => import('../views/Register.vue')},

  //____admin routes____
  {path: '/admin', component: () => import('../views/AdminDashboard.vue')},
  {path: '/admin/manage_treks', component: () => import('../views/ManageTreks.vue')},
  {path: '/admin/manage_staff', component: () => import('../views/ManageStaff.vue')},
  {path: '/admin/manage_users', component: () => import('../views/ManageUser.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})  

export default router