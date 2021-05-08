<template>
  <InputScreenTemplate title="Add game" pre-title="Store" @submit="onSubmit" :back-to="{name: 'StoreHome'}">
    <form >
      <b-form-group class="max-width-3" invalid-feedback="No game selected" label="Game">
          <l-form-select
            v-model="game.name"
            :state="validateState('game_id')"
            @select="$bvModal.show('game-select-modal')"/>
      </b-form-group>
              <!-- modal -->
        <ModalGameSelect
            id="game-select-modal"
            @game-selected="assignGame"
        ></ModalGameSelect>

      <b-form-group invalid-feedback="No supplier selected" label="Supplier">
        <b-input-group>
          <b-form-input :state="validateState('supplier_id')" class="max-width-3" placeholder="Select an option" size="lg" readonly v-model="supplier.name"/>
          <b-input-group-append>
            <b-button v-b-modal:supplier-select-modal variant="outline-secondary"
            ><i class="fe fe-search mr-2"/>Search
            </b-button>
          </b-input-group-append>
        </b-input-group>
        <b-form-input
            v-model="form.supplier_id"
            :state="validateState('supplier_id')"
            hidden
        />
      </b-form-group>

      <ModalSupplierSelect
          id="supplier-select-modal"
          @selected="assignSupplier"/>

        <b-form-group class="max-width-2" invalid-feedback="Invalid amount" label="Selling price">
          <l-form-input-currency :state="validateState('selling_price')" v-model="form.selling_price"/>
        </b-form-group>

        <b-form-group class="max-width-2" label="Buying price" invalid-feedback="Invalid amount">
          <l-form-input-currency :state="validateState('buying_price')" v-model="form.buying_price"/>
        </b-form-group>

      <b-form-group label="Stock" class="max-width-2" invalid-feedback="Invalid number">
        <b-form-input number size="lg" placeholder="Insert a quantity" v-model="form.stock" :state="validateState('stock')" />
      </b-form-group>
    </form>
  </InputScreenTemplate>
</template>

<script>
import InputScreenTemplate from '@/components/templates/InputScreenTemplate'
import ModalGameSelect from '@/components/ModalGameSelect'
import ModalSupplierSelect from '@/components/ModalSupplierSelect'
import gamesMixin from '@/mixins/games.mixin'
import formMixin from '@/mixins/form.mixins'
import bggService from '@/services/bgg.service'
import {minValue, numeric, required} from 'vuelidate/lib/validators'
import LFormInputCurrency from '@/components/form/LFormInputCurrency'
import axiosMixin from '@/mixins/axios.mixin'
import storeService from '@/services/store.service'
import LFormSelect from "@/components/form/LFormSelect"

export default {
  name: 'NewGame',
  components: {LFormSelect, InputScreenTemplate, ModalGameSelect, ModalSupplierSelect, LFormInputCurrency},
  mixins: [gamesMixin, formMixin, axiosMixin],
  data() {
    return {
      currency_options:{
        currency: 'EUR',
        locale: 'pt-PT',
        precision: 2
      },
      game: {},
      supplier: {},
      form: {
        game_id: '',
        supplier_id: '',
        selling_price: null,
        buying_price: null,
        stock: ''
      },
    }
  },
  methods: {
    assignGame(game) {
      bggService.fetch(game.id).then((response) => {
        this.game = response
        this.form.game_id = parseInt(game.id)
        this.$bvModal.hide('game-select-modal')
      })
    },
    assignSupplier(supplier) {
      console.log('Selected: ' + supplier)
      this.supplier = supplier
      this.form.supplier_id = supplier.id
      this.$bvModal.hide('supplier-select-modal')
    },
    formatter(val){
      return this.$ci.parse(val, this.currency_options)
    },
    onSubmit() {
      this.$v.form.$touch()
      if (this.$v.form.$anyError) {
        return
      }

      storeService.createGame(this.form).then(() => {
        this.$toast.success('Saved')
        this.$router.push({ name: 'StoreHome' })
      }).catch((response) => this.$toast.error(this.getErrorDescription(response)))
    }
  },
  validations: {
    form: {
      game_id: {
        required,
      },
      supplier_id: {
        required,
      },
      buying_price: {
        required,
      },
      selling_price: {
        required,
      },
      stock: {
        required,
        numeric,
        minValue: minValue(0)
      },
    },
  },
}
</script>

<style scoped></style>
