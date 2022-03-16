import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'

Vue.use(VueRouter)

const Home = () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
const NotFound = () => import(/* webpackChunkName: "notfound" */ '../views/NotFound.vue')
const ViewPlatform = () => import(/* webpackChunkName: "viewplatform" */ '../views/ViewPlatform.vue')
const Subscribe = () => import(/* webpackChunkName: "subscribe" */ '../views/Subscribe.vue')
const Settings = () => import(/* webpackChunkName: "settings" */ '../views/Settings.vue')

const routes: Array<RouteConfig> = [
  { path: '/', name: 'home', component: Home },
  { path: '*', name: 'notFound', component: NotFound },
  // TODO: Add pages here
  { path: '/platforms/:platform', name: 'viewPlatform', component: ViewPlatform },
  { path: '/subscribe', name: 'subscribe', component: Subscribe },
  { path: '/settings', name: 'settings', component: Settings }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
