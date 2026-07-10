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

   //____staff routes____
  {path: '/staff', component: () => import('../views/StaffDashboard.vue')},
  {path: '/staff/manage_treks', component: () => import('../views/StaffManageTrek.vue')},

  //____user routes____
  {path: '/user', component: () => import('../views/UserDashboard.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})  

export default router