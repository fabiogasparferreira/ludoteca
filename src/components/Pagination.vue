<template>

  <!-- Pagination -->
  <b-row v-show="totalCount > perPage" no-gutters>

    <!-- Pagination (prev) -->
    <ul class="col list-pagination-prev pagination pagination-tabs justify-content-start">
      <li class="page-item">
        <a class="page-link" href="#">
          <i class="fe fe-arrow-left mr-1"></i> Previous
        </a>
      </li>
    </ul>

    <!-- Pagination -->
    <ul class="col list-pagination pagination pagination-tabs justify-content-center">
      <li v-for="(page, index) in pages" v-bind:key="index"
          v-bind:class="{ active: currentPage === page }">
        <b-link v-if="Number.isInteger(page)" class="page" @click="setPage(page)">{{ page }}</b-link>
        <span v-else class="page">{{ page }}</span>
      </li>
    </ul>

    <!-- Pagination (next) -->
    <ul class="col list-pagination-next pagination pagination-tabs justify-content-end">
      <li class="page-item">
        <a class="page-link" href="#">
          Next <i class="fe fe-arrow-right ml-1"></i>
        </a>
      </li>
    </ul>
  </b-row>

</template>

<script>
export default {
  name: "Pagination",
  props: {
    value: {
      type: Number,
      required: true
    },
    totalCount: {
      type: Number,
      required: true
    },
    perPage: {
      type: Number,
      default: 50
    }
  },
  data() {
    return {
      pages: [],
    }
  },
  computed: {
    currentPage: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    }
  },
  beforeUpdate() {
    this.updatePages()
  },
  methods: {
    updatePages() {
      this.pages = []

      let current = this.currentPage,
          last = Math.ceil(this.totalCount / this.perPage),
          delta = 2,
          left = current - delta,
          right = current + delta + 1,
          range = [],
          l;

      for (let i = 1; i <= last; i++) {
        if (i === 1 || i === last || i >= left && i < right) {
          range.push(i);
        }
      }

      for (let i of range) {
        if (l) {
          if (i - l === 2) {
            this.pages.push(l + 1);
          } else if (i - l !== 1) {
            this.pages.push('...');
          }
        }
        this.pages.push(i);
        l = i;
      }
    },
    setPage(number) {
      this.currentPage = number
    }
  }
}
</script>
