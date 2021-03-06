<template>
  <WizardScreen :title="title" :back-to="{ name: 'LibraryHome' }" @submit="doWithdraw">
    <template #content>
      <b-form>
        <b-form-group :state="validateState('requisitor')"
            label="Requisitor" invalid-feedback="You need to select a player first">
          <b-row>
            <b-col class="d-flex align-items-center">
              <span v-if="!form.requisitor" class="text-muted"
                >No player selected</span
              >
              <b-form-input
                v-if="!!form.requisitor"
                readonly

                :value="form.requisitor.name"
              />
            </b-col>
            <b-col cols="auto">
              <b-button variant="white" v-b-modal.player-select>
                <span v-if="!!form.requisitor">Change</span
                ><span v-if="!form.requisitor">Select</span>
              </b-button>
            </b-col>
          </b-row>
        </b-form-group>

        <ModalPlayerSelect
          id="player-select"
          title="Players"
          v-on:player-selected="setRequisitor"
        >
        </ModalPlayerSelect>

        <b-form-group class="mt-5" :label="game.game.name">
          <LocationShelves :location="game.location.name" />
        </b-form-group>

      </b-form>
    </template>
  </WizardScreen>
</template>

<script>
import usersMixin from '@/mixins/users.mixin'
import gamesMixin from '@/mixins/games.mixin'
import axiosMixin from '@/mixins/axios.mixin'
import withdrawService from '@/services/withdraw.service'
import libraryService from '@/services/library.service'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import WizardScreen from '@/components/templates/WizardScreen'
import LocationShelves from '@/components/location/LocationShelves'

import formMixin from '@/mixins/form.mixins'

import { required } from 'vuelidate/lib/validators'

export default {
  name: 'WithdrawGame',
  components: {
    LocationShelves,
    ModalPlayerSelect,
    WizardScreen,
  },
  mixins: [usersMixin, axiosMixin, gamesMixin, formMixin],
  props: ['title', 'pretitle'],
  data() {
    return {
      game: {
        game: {
          name: '',
        },
        location: '',
      },
      form: {
        requisitor: undefined,
      },
    }
  },
  methods: {
    doWithdraw(e) {
      e.preventDefault()

      this.$v.form.$touch()
      if (this.$v.form.$anyError) {
        return
      }

      let data = {
        requisitor_id: this.form.requisitor.id,
        game_id: this.game.id,
      }

      withdrawService
        .withdrawGame(data)
        .then(() => {
          this.$toast.success(
            'Success! Don\'t forget to give the game to '+ this.form.requisitor.name,
          )
          this.$router.push({ name: 'Home' })
        })
        .catch((response) => this.$toast(this.getErrorDescription(response)))
    },
    setRequisitor(player) {
      this.form.requisitor = player
      this.$bvModal.hide('player-select')
    },
  },
  mounted() {
    libraryService
      .fetchGame(this.$route.params.id)
      .then((response) => (this.game = response))
  },
  validations: {
    form: {
      requisitor: {
          required,
      },
    },
  },
}
</script>

<style scoped></style>
