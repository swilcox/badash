<template>
  <div class="about">
    <img class="logo" src="../assets/badash-logo.svg"/>
    <h1>BADash</h1>
    <h2>the Barely Adequate Dashboard</h2>
    <p></p>
  </div>
</template>


<script>
export default {
  name: 'Home',
  data () {
    return {
      msg: 'BaDash'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

  .about img.logo {
      height: 10em;
  }

</style>