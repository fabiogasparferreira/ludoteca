<template>
  <WizardScreen
    :back-to="{ name: 'Home' }"
    pre-title="library"
    title="New game"
  >
    <template #content>
      <form novalidate @submit.stop.prevent="onSubmit">
        <!-- Game -->
        <b-form-group invalid-feedback="This field is required" label="Game">
          <div
            v-if="!game.id"
            class="d-flex flex-row align-items-center justify-content-between"
          >
            <span class="text-muted">No game selected</span>
            <b-button v-b-modal.game-select-modal variant="outline-secondary"
              >Search games</b-button
            >
          </div>
          <b-form-input
            v-model="form.game_id"
            :state="validateState('game_id')"
            hidden
          ></b-form-input>

          <!-- modal -->
          <ModalGameSelect
            id="game-select-modal"
            @game-selected="assignGame"
          ></ModalGameSelect>

          <!-- details -->
          <GameCard v-if="!!game.id" :game="game" />
        </b-form-group>

        <!-- Owner -->
        <b-form-group invalid-feedback="This field is required" label="Owner">
          <div
            v-if="!player.id"
            class="d-flex flex-row align-items-center justify-content-between"
          >
            <span class="text-muted">No player selected</span>
            <b-button v-b-modal.player-select-modal variant="outline-secondary"
              >Search players</b-button
            >
          </div>
          <b-form-input
            v-model="form.owner_id"
            :state="validateState('owner_id')"
            hidden
          ></b-form-input>

          <PersonCard v-if="!!player.id" :person="player" />

          <!-- Owner modal -->
          <ModalPlayerSelect
            id="player-select-modal"
            @player-selected="assignPlayer"
          ></ModalPlayerSelect>
        </b-form-group>

        <!-- Location -->
        <b-form-group
          invalid-feedback="This field is required"
          label="Location"
        >
          <b-form-input
            v-model="selected"
            :state="validateState('location')"
            hidden
          />
          <FormSelect
            v-model="form.location"
            :options="$store.getters['library/locations']"
            :state="validateState('location')"
            option-text="name"
            option-value="id"
          />
        </b-form-group>

        <!-- Notes -->
        <b-form-group description="Optional" label="Notes">
          <b-form-textarea
            v-model="form.notes"
            placeholder="Eg. expansion included, missing components"
          ></b-form-textarea>
        </b-form-group>

        <div class="d-flex flex-row justify-content-end mt-5">
          <b-button
            size="lg"
            variant="link"
            class="mr-3 text-muted"
            :to="{ name: 'LibraryHome' }"
            >Cancel</b-button
          >
          <b-button size="lg" type="submit" variant="primary">Create</b-button>
        </div>
      </form>
    </template>
  </WizardScreen>
</template>

<script>
import ModalGameSelect from '@/components/ModalGameSelect'
import bggService from '@/services/bgg.service'
import libraryService from '@/services/library.service'
import PersonCard from '@/components/PersonCard'
import gamesMixin from '@/mixins/games.mixin'
import formMixin from '@/mixins/form.mixins'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import GameCard from '@/components/cards/GameCard'
import WizardScreen from '@/components/templates/WizardScreen'
import FormSelect from '@/components/FormSelect'

import { required } from 'vuelidate/lib/validators'

export default {
  name: 'AddGame',
  components: {
    WizardScreen,
    ModalPlayerSelect,
    PersonCard,
    ModalGameSelect,
    GameCard,
    FormSelect,
  },
  mixins: [gamesMixin, formMixin],
  data() {
    return {
      game: this.initGame(),
      games: [],
      form: {
        location: '',
        owner_id: '',
        notes: '',
        game_id: '',
      },
      options: {
        isMultipleGamesActive: false,
        isKeepOwnerActive: false,
        isAddMoreGamesActive: false,
      },
      player: {},
    }
  },
  watch: {},
  methods: {
    initGame() {
      return {
        id: '',
        name: '',
        thumbnail: '',
      }
    },
    assignGame(game) {
      bggService.fetch(game.id).then(response => {
        this.game = response
        this.form.game_id = game.id
        this.$bvModal.hide('game-select-modal')
      })
    },
    assignPlayer(player) {
      this.player = player
      this.form.owner_id = player.id
      this.$bvModal.hide('player-select-modal')
    },
    onSubmit() {
      this.$v.form.$touch()
      if (this.$v.form.$anyError) {
        return
      }

      this.form.game_id = this.game.id
      this.form.owner_id = this.player.id

      libraryService
        .createGame(this.form)
        .then(response => {
          this.$toast.success('Success! Place the game on ' + response.location)
          this.$router.push({ name: 'Home' })
        })
        .catch(response => console.log(response))
    },
  },
  validations: {
    form: {
      game_id: {
        required,
      },
      owner_id: {
        required,
      },
      location: {
        required,
      },
    },
  },
}
</script>

<style scoped></style>
