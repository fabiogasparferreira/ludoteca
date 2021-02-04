<template>
  <div>
    <div class="dropdown">
      <b-form-input
        v-if="Object.keys(selectedItem).length === 0"
        ref="dropdowninput"
        v-model.trim="inputValue"
        class="dropdown-input custom-select"
        type="text"
        placeholder="Type to search"
      />
      <!--        <div v-else @click="resetSelection" class="form-control">-->
      <div v-else @click="resetSelection" class="form-control custom-select">
        <img :src="selectedItem.game.thumbnail" class="dropdown-item-flag" />
        {{ selectedItem.game.name }}
      </div>
      <div v-show="inputValue && apiLoaded" class="dropdown-list">
        <!--            <b-form-input type="search"></b-form-input>-->
        <b-dropdown-item
          @click="selectItem(item)"
          v-show="itemVisible(item)"
          v-for="item in itemList"
          :key="item.id"
        >
          <b-avatar rounded :src="item.game.thumbnail" size="1.5em"></b-avatar>
          <img class="dropdown-item-flag" />
          {{ item.game.name }}
        </b-dropdown-item>
      </div>
    </div>
    <b-dropdown
      boundary="window"
      text="Select stuff"
      class=""
      style="max-height: 200px; overflow-x: hidden;"
    >
      <b-dropdown-form>
        <b-form-input type="search" size="sm"></b-form-input>
      </b-dropdown-form>
      <b-dropdown-item></b-dropdown-item>

      <b-dropdown-item
        @click="selectItem(item)"
        v-show="itemVisible(item)"
        v-for="item in itemList"
        :key="item.id"
      >
        <b-avatar rounded :src="item.game.thumbnail" size="1.5em"></b-avatar>
        <img class="dropdown-item-flag" />
        {{ item.game.name }}
      </b-dropdown-item>
    </b-dropdown>
    <b-form-input list="my-list-id"></b-form-input>

    <datalist id="my-list-id">
      <option v-for="(item, index) in itemList" v-bind:key="index">{{
        item.game.name
      }}</option>
    </datalist>
  </div>
</template>

<script>
import libraryService from '@/services/library.service'

export default {
  data() {
    return {
      selectedItem: {},
      inputValue: '',
      itemList: [],
      apiLoaded: false,
      apiUrl: 'https://restcountries.eu/rest/v2/all?fields=name;flag',
    }
  },
  props: {
    options: {
      type: Array,
      required: true,
    },
  },
  mounted() {
    this.getList()
  },
  methods: {
    resetSelection() {
      this.selectedItem = {}
      this.$nextTick(() => this.$refs.dropdowninput.focus())
      this.$emit('on-item-reset')
    },
    selectItem(theItem) {
      this.selectedItem = theItem
      this.inputValue = ''
      this.$emit('on-item-selected', theItem)
    },
    itemVisible(item) {
      let currentName = item.game.name.toLowerCase()
      let currentInput = this.inputValue.toLowerCase()
      return currentName.includes(currentInput)
    },
    getList() {
      libraryService.fetchGames().then(response => {
        this.itemList = response.results
        this.apiLoaded = true
      })
    },
  },
}
</script>

<style>
.dropdown {
  position: relative;
  width: 100%;
  margin: 0 auto;
}

.dropdown-input::placeholder {
  opacity: 0.7;
}

.dropdown-selected {
  font-weight: bold;
  cursor: pointer;
}

.dropdown-list {
  position: absolute;
  width: 100%;
  max-height: 500px;
  margin-top: 4px;
  overflow-y: auto;
  background: #ffffff;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.dropdown-item {
  display: flex;
  width: 100%;
  padding: 11px 16px;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #edf2f7;
}

.dropdown-item-flag {
  max-width: 24px;
  max-height: 18px;
  margin: auto 12px auto 0px;
}
</style>
