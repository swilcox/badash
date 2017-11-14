<template>
  <div class="header">
    <div class="home-menu pure-menu pure-menu-horizontal pure-menu-fixed">
      <img class="header-logo" src="../assets/badash-logo.png">
      <ul class="pure-menu-list">
        <li class="pure-menu-item"><router-link :to="{ name: 'home'}" class="pure-menu-link">Home</router-link></li>
        <li class="pure-menu-item"><router-link :to="{ name: 'about'}" class="pure-menu-link">About</router-link></li>
      </ul>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'app-header',
    data () {
      return {
        title: 'BaDash'
      }
    }
  }
</script>

<style>
  /*
  * -- MENU STYLES --
  * I want to customize how my .pure-menu looks at the top of the page
  */
  .header-logo {
      height: 2em;
      margin: 5px 0px -5px 5px;
      padding: 0px 0px -5px 0px;
  }

  .home-menu {
    padding: 0;
    text-align: center;
    box-shadow: 0 1px 1px rgba(0,0,0, 0.30);
    background: #2d3e50;
  }
  .pure-menu.pure-menu-fixed {
    /* Fixed menus normally have a border at the bottom. */
    border-bottom: none;
    /* I need a higher z-index here because of the scroll-over effect. */
    z-index: 4;
  }
  .home-menu .pure-menu-heading {
    color: white;
    font-weight: 400;
    font-size: 120%;
  }
  .home-menu a.router-link-exact-active {
    color: white;
  }
  .home-menu a {
    color: #6FBEF3;
  }
  .home-menu li a:hover,
  .home-menu li a:focus {
    background: none;
    border: none;
    color: #AECFE5;
  }
  /*
  * -- TABLET (AND UP) MEDIA QUERIES --
  * On tablets and other medium-sized devices, we want to customize some
  * of the mobile styles.
  */
  @media (min-width: 48em) {
    /* We can align the menu header to the left, but float the
    menu items to the right. */
    .home-menu {
        text-align: left;
    }
    .home-menu ul {
        float: right;
    }
  }
</style>