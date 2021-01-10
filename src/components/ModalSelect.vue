<template>
  <!-- Modal -->
  <div>
    <b-modal :id="id"
             :hide-footer="hideFooter"
             :title="title"
             body-class="p-0"
             class=""
             scrollable>
      <template v-slot:modal-header>
        <slot name="header">
          <div class="input-group input-group-merge">
            <b-form-input v-model="search"
                          class="form-control form-control-prepended search"
                          debounce="300"
                          flush
                          placeholder="Search"
                          type="search"/>
            <div class="input-group-prepend">
              <div class="input-group-text">
                <b-icon-search font-scale="0.8"></b-icon-search>
              </div>
            </div>
          </div>
        </slot>
      </template>
      <template v-slot:default>
        <div style="max-height: 400px">
          <slot name="content">

            <b-skeleton-wrapper :loading="loading">
              <template #loading>
                <b-skeleton width="2rem"></b-skeleton>
              </template>
              <b-list-group  flush>
                <b-list-group-item v-for="(item, index) in items"
                                   v-bind:key="index"
                                   button
                                   class="px-4 border-0 text-gray-700"
                                   :variant="selected.includes(item.id) ? 'primary' : ''"
                                   :class="{'bg-primary-soft text-gray-800': selected.includes(item.id)}"
                                   data-dismiss="modal"
                                   @click="select(item)">
                  <div class="d-flex flex-row align-items-center justify-content-between">
                      {{ item[itemTitle] }}
                    <b-icon-check-circle-fill class="text-primary" v-show="selected.includes(item.id)"/>
                  </div>
                </b-list-group-item>
                <b-list-group-item v-show="items.length === 0" class="px-4 text-muted">No results to show
                </b-list-group-item>
              </b-list-group>
            </b-skeleton-wrapper>

          </slot>
        </div>
      </template>
      <template v-if="!hideFooter || multiple" #modal-footer>
        <slot name="footer">
          <b-button variant="primary" @click="done">Done</b-button>
        </slot>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "ModalSelect",
  props: {
    id: String,
    title: String,
    value: {},
    hideFooter: {
      type: Boolean,
      default: false
    },
    items: {
      type: Array
    },
    itemTitle: {
      default: 'name'
    },
    itemMetadata: {},
    multiple: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      loading: false,
      search: '',
      selected: []
    }
  },
  watch: {
    search: function (val) {
      this.$emit('search', val)
    }
  },
  methods: {
    select(val) {
      if (this.multiple) {
        if (this.selected.includes(val.id)) {
          this.selected = this.selected.filter(item => item !== val.id)
        } else {
          this.selected.push(val.id)
        }
      } else {
        this.$emit('input', val)
      }
    },
    done(){
      this.$emit('input', this.selected)
    }
  }
}
</script>