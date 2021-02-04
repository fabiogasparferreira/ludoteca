<template>
  <!-- Modal -->
  <div>
    <b-modal
      :id="id"
      :hide-footer="hideFooter"
      :title="title"
      body-class="p-0"
      class=""
      scrollable
    >
      <template v-slot:modal-header>
        <slot name="header">
          <div class="input-group input-group-merge">
            <b-form-input
              v-model="search"
              class="form-control form-control-prepended search"
              debounce="300"
              flush
              placeholder="Search"
              type="search"
            />
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
              <b-list-group flush>
                <b-list-group-item
                  v-for="(item, index) in items"
                  v-bind:key="index"
                  button
                  class="px-4"
                  data-dismiss="modal"
                  @click="$emit('selected', item)"
                >
                  {{ item[itemTitle] }}
                  <span v-if="item[itemMetadata]" class="text-gray-600"
                    >({{ item[itemMetadata] }})</span
                  >
                </b-list-group-item>
                <b-list-group-item
                  v-show="items.length === 0"
                  class="px-4 text-muted"
                  >No results to show
                </b-list-group-item>
              </b-list-group>
            </b-skeleton-wrapper>
          </slot>
        </div>
      </template>
      <template #modal-footer>
        <slot name="footer"></slot>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'ModalSelect',
  props: {
    id: String,
    title: String,
    hideFooter: {
      type: Boolean,
      default: false,
    },
    items: {
      type: Array,
    },
    itemTitle: {
      default: 'name',
    },
    itemMetadata: {},
  },
  data: function() {
    return {
      loading: false,
      search: '',
    }
  },
  watch: {
    search: function(val) {
      this.$emit('search', val)
    },
  },
}
</script>
