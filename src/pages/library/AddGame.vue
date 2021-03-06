<template>
  <WizardScreen
    :back-to="{ name: 'Home' }"
    pre-title="library"
    title="New game"
    @submit="onSubmit"
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
          <b-card v-if="!!game.id" :game="game">
            <b-media>
              <template #aside>
                <b-avatar :src="game.thumbnail" rounded size="lg"/>
              </template>
              <div class="d-flex flex-column">
              <span>{{game.name}}</span>
                <metadata-item icon="calendar-fill" :text="game.year"/>
                </div>
            </b-media>
          </b-card>
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

                  <b-card v-if="!!player.id" >
            <b-media>
              <template #aside>
                <b-avatar variant="light" size="lg"/>
              </template>
              <div class="d-flex flex-column">
              <span>{{player.name}}</span>
                <metadata-item icon="envelope" :text="player.email"/>
                </div>
            </b-media>
          </b-card>
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
            v-model="form.location"
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
<!--          <b-button-->
<!--            size="lg"-->
<!--            variant="link"-->
<!--            class="mr-3 text-muted"-->
<!--            :to="{ name: 'LibraryHome' }"-->
<!--            >Cancel</b-button-->
<!--          >-->
<!--          <b-button size="lg" type="submit" variant="primary">Create</b-button>-->
        </div>
      </form>
    </template>
  </WizardScreen>
</template>

<script>
import ModalGameSelect from '@/components/ModalGameSelect'
import bggService from '@/services/bgg.service'
import libraryService from '@/services/library.service'
import gamesMixin from '@/mixins/games.mixin'
import formMixin from '@/mixins/form.mixins'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import WizardScreen from '@/components/templates/WizardScreen'
import FormSelect from '@/components/FormSelect'

import { required } from 'vuelidate/lib/validators'
import MetadataItem from "@/components/cards/MetadataItem"

export default {
  name: 'AddGame',
  components: {
    MetadataItem,
    WizardScreen,
    ModalPlayerSelect,
    ModalGameSelect,
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
        .then(() => {
          this.$toast.success('Saved')
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
