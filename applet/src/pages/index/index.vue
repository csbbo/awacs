<template>
  <div class="home">
    <SearchBar />
  </div>
</template>

<script>
  import SearchBar from '../../components/home/SearchBar'
  const fly = require('flyio/dist/npm/wx')
  export default {
    components: {
      SearchBar
    },
    methods: {
      jump () {
        fly().get('https://www.baidu.com').then(response => {
          console.log('handleResponse...' + response)
        })
      }
    }
  }
</script>

<style lang="scss" scoped>
</style>
