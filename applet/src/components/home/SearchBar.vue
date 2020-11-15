<template>
  <div class="search-bar">
    <div class="search-bar-wrapper">
      <van-icon
        class="search"
        name="search"
        size="16px"
        color="#858c96"
      />
      <input
        class="search-bar-input"
        :focus="focus"
        :disabled="disabled"
        :maxlength="limit"
        :placeholder="hotSearch"
        v-model="searchWord"
        @input="onChange"
        confirm-type="search"
        @confirm="onConfirm"
      />
      <van-icon
        class="clear"
        name="clear"
        size="16px"
        color="#858c96"
        @click="onClearClick"
      />
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      focus: {
        type: Boolean,
        default: false
      },
      disabled: {
        type: Boolean,
        default: false
      },
      limit: {
        type: Number,
        default: 50
      },
      hotSearch: {
        type: String,
        default: '搜索'
      }
    },
    data () {
      return {
        searchWord: ''
      }
    },
    methods: {
      onSearchBarClick () {
        this.$emit('onClick')
      },
      onClearClick () {
        this.searchWord = ''
        this.$emit('onClear')
      },
      onChange (e) {
        const { value } = e.mp.detail
        this.$emit('onChange', value)
      },
      onConfirm (e) {
        const { value } = e.mp.detail
        this.$emit('onConfirm', value)
      },
      setValue (v) {
        this.searchWord = v
      },
      getValue () {
        return this.searchWord
      }
    }
  }
</script>

<style lang="scss" scoped>
.search-bar {
  padding: 0 15.5px;
  .search-bar-wrapper {
    display: flex;
    align-items: center;
    height: 40px;
    box-sizing: border-box;
    background: #F5F7F9;
    border-radius: 20px;
    padding: 12px 17px;
    .search-bar-input {
      flex: 1;
      margin: 0 12px;
    }
    .search, .clear {
      display: flex;
      align-items: center;
      height: 100%;
    }
  }
}
</style>
