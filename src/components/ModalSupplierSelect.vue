<template>
  <!-- Modal -->

  <ModalSelect
    :id="id"
    :items="suppliers"
    :title="title"
    item-metadata="email"
    item-title="name"
    @search="search"
    @selected="$emit('selected', $event)"
  >
    <template v-if="isNewSupplier" v-slot:header>
      <div
        class="d-flex flex-row align-items-center justify-content-between flex-fill"
      >
        <div class="d-flex flex-fill mr-auto">
          <b-button
            v-show="isNewSupplier"
            size="sm"
            variant="info"
            @click="isNewSupplier = false"
          >
            Search for suppliers
          </b-button>
        </div>
        <div class="d-flex flex-fill justify-content-center">
          <h4 v-show="isNewSupplier" class="mb-0">Add supplier</h4>
        </div>
        <div class="d-flex flex-fill ml-auto"></div>
      </div>
    </template>

    <template v-if="isNewSupplier" #content>
      <div>
        <form>
          <div class="px-4 mt-4">
            <b-form-group
              invalid-feedback="Required"
              label="Name"
            >
              <b-form-input
                v-model="form.name"
                :state="validateState('name')"
                placeholder="Name"
                type="text"
              />
            </b-form-group>
            <b-form-group
              invalid-feedback="Please insert a valid e-mail address"
              label="E-mail"
            >
              <b-form-input
                v-model="form.email"
                :state="validateState('email')"
                placeholder="eg. name@mail.com"
                type="email"
              />
            </b-form-group>
            <b-form-group
              invalid-feedback="Required"
              label="Phone"
            >
              <b-form-input
                v-model="form.phone"
                :state="validateState('phone')"
                placeholder="Phone"
                type="tel"
              />
            </b-form-group>
            <b-form-group
              invalid-feedback="Not valid"
              label="Website"
              description="Optional"
            >
              <b-form-input
                v-model="form.website"
                :state="validateState('website')"
                placeholder="https://suppliers.site"
                type="text56u"
              />
            </b-form-group>
          </div>
        </form>
      </div>
    </template>
    <template #footer>
      <button
        v-if="!isNewSupplier"
        class="btn btn-info"
        type="button"
        @click="enableSupplierForm"
      >
        Add
      </button>
      <b-button v-if="isNewSupplier" variant="primary" @click="onSubmit">
        <span v-show="!loading">Save</span>
        <b-spinner v-show="loading" small />
      </b-button>
    </template>
  </ModalSelect>
</template>

<script>
import usersMixin from '@/mixins/users.mixin'
import formMixin from '@/mixins/form.mixins'
import supplierService from '@/services/supplier.service'
import ModalSelect from '@/components/ModalSelect'

import { email, required, url } from 'vuelidate/lib/validators'
import axiosUtils from '@/mixins/axios.utils'

export default {
  name: 'ModalPlayerSelect',
  mixins: [usersMixin, formMixin],
  props: ['id', 'title'],
  components: { ModalSelect },
  data: function () {
    return {
      isNewSupplier: false,
      selectedSupplier: undefined,
      suppliers: this.$store.getters['store/suppliers'],
      form: {
        name: '',
        email: '',
        phone: '',
        website: ''
      },
      loading: false,
    }
  },
  methods: {
    enableSupplierForm(e) {
      e.preventDefault()
      this.isNewSupplier = true
    },
    search(val) {
      this.form.name = val
      supplierService.filter({'search': val})
        .then((response) => (this.suppliers = response))
    },
    onSubmit() {
      this.$v.form.$touch()
      if (this.$v.form.$anyError) {
        return
      }
      this.loading = true

      supplierService.create(this.form)
        .then((response) => {
          this.$bvModal.hide(this.id)
          this.$emit('selected', response)
        })
        .catch((response) => {
          this.$toast.error(
            'Error creating new supplier: ' +
              axiosUtils.getErrorDescription(response),
          )
        })
        .finally(() => (this.loading = false))

    },
  },
  mounted() {
    this.suppliers = this.$store.getters['store/suppliers']
  },
  validations: {
    form: {
      name: {
        required,
      },
      email: {
        email,
        required,
      },
      phone: {
        required
      },
      website: {
        url
      }
    },
  },
}
</script>

<style scoped></style>
