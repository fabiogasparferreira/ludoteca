<template>
  <WizardScreen :title="title" :back-to="{name: 'LibraryHome'}">
    <template #content>
      <b-form>
        <b-form-group label="Game">
          <GameCard :game="game.game">
            <template v-slot:right>
              <h1 class="mb-0 text-muted">{{ game.location }}</h1>
            </template>
          </GameCard>
        </b-form-group>

        <b-form-group label="Player">

          <b-link v-b-modal.player-select>
            <div v-if="!requisitor.id"
                 class="d-flex col-12 card card-inactive "

                 role="button">

              <div class="card-body btn btn-link align-self-center">
                <span class="fe fe-plus-circle"></span>
                <span class="ml-2">Select a player</span>
              </div>
            </div>
          </b-link>
          <div v-if="!!requisitor.id" class="row">
            <div class="col">
              <PersonCard :person="requisitor"></PersonCard>
            </div>

            <div class="col-auto pb-4">
              <div class="btn btn-info d-flex align-items-center h-100 " data-target="#player-select-modal"
                   data-toggle="modal">
                <b-icon-pencil-fill></b-icon-pencil-fill>
              </div>
            </div>
          </div>
        </b-form-group>

        <div class="row mt-5">
          <div class="col">
          </div>
          <b-col cols="auto">
            <b-button variant="link" size="lg" class="text-muted" :to="{name: 'LibraryHome'}">Cancel</b-button>
          </b-col>
          <div class="col-auto">
            <button class="btn btn-lg btn-primary " v-on:click="doWithdraw">Finish</button>
          </div>
        </div>
        <ModalPlayerSelect id="player-select" title="Players" v-on:player-selected="setRequisitor">
        </ModalPlayerSelect>
      </b-form>
    </template>
  </WizardScreen>
</template>

<script>
import usersMixin from '@/mixins/users.mixin'
import gamesMixin from '@/mixins/games.mixin'
import axiosMixin from '@/mixins/axios.mixin'
import withdrawService from '@/services/withdraw.service'
import libraryService from "@/services/library.service";
import GameCard from "@/components/GameCard";
import ModalPlayerSelect from "@/components/ModalPlayerSelect";
import PersonCard from "@/components/PersonCard";
import WizardScreen from "@/components/templates/WizardScreen";

export default {
  name: "WithdrawGame",
  components: {ModalPlayerSelect, GameCard, PersonCard, WizardScreen},
  mixins: [usersMixin, axiosMixin, gamesMixin],
  props: ['title', 'pretitle'],
  data() {
    return {
      id: '',
      game: {
        game: {
          min_players: 0,
          max_players: 0
        },
        thumbnail: ''
      },
      requisitor: {
        id: '',
        name: '',
        email: ''
      },
    }
  },
  methods: {
    doWithdraw(e) {
      e.preventDefault();

      let data = {
        requisitor_id: this.requisitor.id,
        game_id: this.game.id
      };

      withdrawService.withdrawGame(data).then(() => {
        this.$toast.success('Successfully withdrawn. Game placed in ' + this.game.game.location)
        this.$router.push({name: 'Home'});
      }).catch(response => (
          this.$toast(this.getErrorDescription(response)))
      );
    },
    setRequisitor(player) {
      this.requisitor = player
      this.$bvModal.hide('player-select')
    }
  },
  mounted() {
    this.id = this.$route.params.id;
    libraryService.fetchGame(this.id)
        .then(response => (this.game = response));
  },
  validations: {}
}
</script>

<style scoped>

</style>
















