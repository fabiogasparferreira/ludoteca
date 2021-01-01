<template>
  <b-modal no-close-on-backdrop :id="id" :title="game.game.name">
    <template #default>
      <b-form>
        <b-form-group label="Shelf">
          <FormSelect
              v-model="selected"
              :options="$store.getters['library/locations']"
              option-text="name"
              option-value="id">
          </FormSelect>
        </b-form-group>
      </b-form>
    </template>

    <template #modal-footer>
      <b-button variant="secondary" @click="$bvModal.hide(id)">
        Cancel
      </b-button>
      <b-button variant="primary" @click="checkin">
        OK
      </b-button>
    </template>
  </b-modal>
</template>

<script>
import libraryService from "@/services/library.service";
import FormSelect from "@/components/FormSelect";

export default {
  name: "CheckinModal",
  components: {FormSelect},
  props: ['id', 'game', 'shelves'],
  data: function () {
    return {
      selected: ''
    }
  },
  methods: {
    checkin() {
      libraryService.updateGame(this.game.id, {
        location_id: this.selected,
        date_checkin: new Date()
      })
          .then((response) => {
            this.$toast.success('Success! Place the game on ' + response.location.name)
            this.$bvModal.hide(this.id)
            this.$emit('done')
          })
    }
  }
}
</script>

<style scoped>

</style>