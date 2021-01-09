<template>
  <!-- Modal -->

  <ModalSelect
      :id="id"
      :items="players"
      :title="title"
      item-metadata="email"
      item-title="name"
      @search="search"
      @selected="$emit('player-selected', $event)"
  >
    <template v-if="isNewPlayer" v-slot:header>
      <div class="d-flex flex-row align-items-center justify-content-between flex-fill">
        <div class="d-flex flex-fill mr-auto">
          <b-button v-show="isNewPlayer" size="sm" variant="info" @click="isNewPlayer=false">
            Search for players
          </b-button>
        </div>
        <div class="d-flex flex-fill justify-content-center">
          <h4 v-show="isNewPlayer" class="mb-0">Add player</h4>
        </div>
        <div class="d-flex flex-fill ml-auto"></div>
      </div>
    </template>

    <template v-if="isNewPlayer" #content>
      <div>

        <form>
          <div class="px-4 mt-4">
            <b-alert :show="emailAlreadyRegistered" variant="warning">E-mail already registered</b-alert>
            <b-form-group
                invalid-feedback="This field is required"
                label="Name">
              <b-form-input
                  v-model="form.name"
                  :state="validateState('name')"
                  placeholder="Name"
                  type="text"/>
            </b-form-group>
            <b-form-group invalid-feedback="Please insert a valid e-mail address" label="E-mail">
              <b-form-input
                  v-model="form.email"
                  :state="validateState('email')"
                  placeholder="eg. name@mail.com"
                  type="text"/>
            </b-form-group>

          </div>
        </form>
      </div>

    </template>
    <template #footer>
      <button v-if="!isNewPlayer" class="btn btn-info" type="button" @click="doNewPlayer">
        New player
      </button>
      <b-button
          v-if="isNewPlayer"
          variant="primary"
          @click="onSubmit">
        <span v-show="!loading">Add</span>
        <b-spinner v-show="loading" small/>
      </b-button>
    </template>
  </ModalSelect>

</template>

<script>
import usersMixin from '@/mixins/users.mixin'
import formMixin from '@/mixins/form.mixins'
import playerService from '@/services/player.service'
import ModalSelect from "@/components/ModalSelect";

import {email, required} from 'vuelidate/lib/validators'
import axiosUtils from "@/mixins/axios.utils";

export default {
  name: "ModalPlayerSelect",
  mixins: [usersMixin, formMixin],
  props: ['id', 'title'],
  components: {ModalSelect},
  data: function () {
    return {
      isNewPlayer: false,
      selectedPlayer: undefined,
      players: [],
      form: {
        name: '',
        email: ''
      },
      loading: false,
      emailAlreadyRegistered: false,
    }
  },
  methods: {
    doNewPlayer(e) {
      e.preventDefault();
      this.isNewPlayer = true;
    },
    search(val) {
      this.form.name = val
      playerService.searchPlayers(val).then(response => this.players = response)
    },
    onSubmit() {
      this.emailAlreadyRegistered = false
      this.$v.form.$touch();
      if (this.$v.form.$anyError) {
        return;
      } else {
        this.loading = true;

        let player = {
          email: this.form.email
        }

        // In case only one name is inserted
        if (this.form.name.indexOf(' ') < 0) {
          player['first_name'] = this.form.name

          // If more than one name was inserted
          // Break on first space, use first element as first name and all the others use as last name
        } else {
          player['first_name'] = this.form.name.substring(0, this.form.name.indexOf(' '))
          player['last_name'] = this.form.name.substring(this.form.name.indexOf(' ') + 1, this.form.name.length)
        }

        playerService
            .createPlayer(player)
            .then((response) => {
              this.$bvModal.hide(this.id)
              this.$emit('player-selected', response)
            })
            .catch(response => {
              if (response?.response?.data?.email) {
                this.emailAlreadyRegistered = true
              } else {
                this.$toast.error('Error adding player: ' + axiosUtils.getErrorDescription(response));
              }
            })
            .finally(() => this.loading = false)

      }
    }
  },
  validations: {
    form: {
      name: {
        required
      },
      email: {
        email, required
      }
    }
  }
}
</script>

<style scoped>

</style>
