import Vue from 'vue'
import App from '@/App.vue'


// Vuex
import store from '@/store'


// Vue-router
import router from '@/router'


// Vue toastification
import Toast, {POSITION} from 'vue-toastification'
import 'vue-toastification/dist/index.css'
// Vue Bootstrap
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// Theme and custom styles
import '../public/theme/scss/theme.scss'
import '../public/static/main.scss'
import '../public/theme/fonts/feather/feather.css'


// Vuelidate
import {Vuelidate} from 'vuelidate'

Vue.use(Toast, {
    position: POSITION.TOP_CENTER,
    transition: 'Vue-Toastification__fade',
    maxToasts: 10,
    newestOnTop: true,
    hideProgressBar: false,
    icon: true,
    closeButton: 'button',
})


Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)


Vue.use(Vuelidate)


import VueCurrencyInput from 'vue-currency-input'

const pluginOptions = {
  /* see config reference */
  globalOptions: {locale: 'pt-PT', precision: 2 }
}
Vue.use(VueCurrencyInput, pluginOptions)

// Other configurations
Vue.config.productionTip = false

const vue = new Vue({
    router,
    store,
    render: h => h(App),
})

vue.$mount('#app')
