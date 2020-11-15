<template>
  <div>
    <span class="msg">Hello Word</span>
    <van-button type="primary" @click="jump">按钮</van-button>
  </div>
</template>

<script>
  const fly = require('flyio/dist/npm/wx')
  export default {
    methods: {
      jump () {
        // this.$router.push('/pages/index/main')
        // this.$router.replace('/pages/index/main')
        fly().get('https://www.baidu.com').then(response => {
          console.log('handleResponse...')
        })
      }
    }
  }
</script>

<style lang="scss" scoped>
.msg {
  color: red;
  font-size: 20px;
}
</style>
