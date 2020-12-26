import Vue from 'vue'
import App from '@/App.vue'

// -----------------------------------------------------------
// Vuex
// -----------------------------------------------------------

import store from '@/store'


// -----------------------------------------------------------
// Vue-router
// -----------------------------------------------------------

import router from '@/router'


// -----------------------------------------------------------
// Vue toastification
// -----------------------------------------------------------

import Toast, {POSITION} from "vue-toastification";
import "vue-toastification/dist/index.css";

Vue.use(Toast, {
    position: POSITION.TOP_CENTER,
    transition: "Vue-Toastification__fade",
    maxToasts: 10,
    newestOnTop: true,
    hideProgressBar: false,
    icon: true,
    closeButton: "button",
});


// -----------------------------------------------------------
// Vue Bootstrap
// -----------------------------------------------------------

import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)


// -----------------------------------------------------------
// Vue Select
// -----------------------------------------------------------

import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';

Vue.component('v-select', vSelect)


// -----------------------------------------------------------
// Theme and custom styles
// -----------------------------------------------------------
import "../public/theme/css/theme.min.css"
import '../public/static/main.scss'


// -----------------------------------------------------------
// Vuelidate
// -----------------------------------------------------------

import { Vuelidate } from 'vuelidate'
Vue.use(Vuelidate)


// -----------------------------------------------------------
// Other configurations
// -----------------------------------------------------------


Vue.config.productionTip = false

const vue = new Vue({
    router,
    store,
    render: h => h(App)
})

vue.$mount('#app')
