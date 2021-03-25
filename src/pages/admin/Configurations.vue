<template>
  <InputScreenTemplate
    @submit="$router.push({ name: 'Home' })"
    :back-to="{ name: 'Home' }"
    :title="title"
    :pre-title="pretitle"
  >
    <b-card no-body class="mt-5">
      <b-card-header>
        <b-input-group class="input-group-flush">
          <div class="input-group-prepend">
            <span class="input-group-text">
              <b-icon-search font-scale="0.8" />
            </span>
          </div>
          <b-form-input
            class="list-search"
            type="search"
            placeholder="Search"
          />
        </b-input-group>
      </b-card-header>
      <b-table
        hover
        :fields="['type', 'key', 'value', 'actions']"
        :items="$store.getters['configurations/all']"
      >
        <template #cell(actions)="data">
          <b-link
            v-b-modal.modal-edit
            @click="selectedConfig = { ...data.item }"
            ><b-icon-pencil-fill
          /></b-link>
          <b-link hidden class="ml-3" @click="deleteConfig(data.item.id)">
            <b-icon-trash-fill />
          </b-link>
        </template>
      </b-table>
    </b-card>
    <b-modal
      title="Edit configuration"
      id="modal-edit"
      @close="selectedConfig = {}"
      @cancel="selectedConfig = {}"
      @ok="updateConfig()"
    >
      <b-form>
        <b-form-group label="Value">
          <b-form-input v-model="selectedConfig['value']" />
        </b-form-group>
      </b-form>
    </b-modal>
  </InputScreenTemplate>
</template>

<script>
import InputScreenTemplate from '@/components/templates/InputScreenTemplate'
import configurationsService from '@/services/configurations.service'

export default {
  name: 'Configurations',
  data() {
    return {
      selectedConfig: {},
    }
  },
  components: {
    InputScreenTemplate,
  },
  methods: {
    updateConfig() {
      configurationsService
        .updateConfiguration(this.selectedConfig.id, {
          value: this.selectedConfig.value,
        })
        .then(() => {
          this.$store.dispatch('configurations/load')
          this.selectedConfig = {}
        })
    },
    deleteConfig(id) {
      configurationsService.deleteConfiguration(id).then(() => {
        this.$store.dispatch('configurations/load')
      })
    },
  },
  props: ['pretitle', 'title'],
}
</script>

<style scoped></style>
