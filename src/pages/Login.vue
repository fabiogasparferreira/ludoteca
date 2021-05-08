<template>
  <!-- CONTENT
  ================================================== -->

  <div class="min-vh-100 d-flex">
    <div class="container align-self-center">
      <div class="row justify-content-center">
        <div class="col-12 col-md-5 col-xl-4 my-5">
          <!-- Heading -->
          <h1 class="display-4 text-center mb-3">
            Sign in
          </h1>

          <!-- Subheading -->
          <p class="text-muted text-center mb-5">
            Free access to leiriacon platform
          </p>

          <!-- Form -->
          <form @submit.prevent="doLogin">
            <b-form-group label="E-mail">
              <!-- Input -->
              <b-form-input
                v-model="email"
                placeholder="Enter your e-mail"
                tabindex="1"
                type="text"
              />
            </b-form-group>

            <!-- Password -->
            <b-form-group>
              <div class="row">
                <div class="col">
                  <!-- Label -->
                  <label>Password</label>
                </div>
                <div class="col-auto">
                  <!-- Help text -->
                  <a
                    class="form-text small text-muted"
                    href="password-reset.html"
                  >
                    Forgot password?
                  </a>
                </div>
              </div>
              <!-- / .row -->

              <!-- Input group -->
              <b-input-group class="input-group-merge">
                <!-- Input -->
                <b-form-input
                  v-model="password"
                  placeholder="Enter your password"
                  tabindex="2"
                  type="password"
                />
              </b-input-group>
            </b-form-group>

            <!-- Submit -->
            <button class="btn btn-lg btn-block btn-primary mb-3">
              Sign in
            </button>

            <!-- Link -->
            <div class="text-center">
              <small class="text-muted text-center">
                Don't have an account yet? <a href="sign-up.html">Sign up</a>.
              </small>
            </div>
          </form>
        </div>
      </div>
      <!-- / .row -->
    </div>
    <!-- / .container -->
  </div>
</template>

<script>
import axiosUtils from '@/mixins/axios.utils'
import authorizationService from '@/services/authorization.service'
import router from '@/router'

export default {
  name: 'Login',
  data: function() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    doLogin() {
      this.loading = true

      return authorizationService
        .doLogin(this.email, this.password)
        .then(response => {
          this.$store.commit('AUTH_SUCCESS', response.data)
          this.$store.dispatch("init")
          router.push({ name: 'LibraryHome' })
        })
        .catch(response => {
          this.$toast.error(axiosUtils.getErrorDescription(response))
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>

<style scoped></style>
