<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>Project @Tim Lui (24-755-092)</v-app-bar-title>
    </v-app-bar>
    <v-main>
      <ConfigurationPanel />
    </v-main>
  </v-app>
</template>

<script>
import ConfigurationPanel from './components/ConfigurationPanel.vue';
export default {
  name: 'App',
  components: {
    ConfigurationPanel
  },
  data() {
    return {};
  }
}
</script>

<style>
/* disable scrolling */
html {
  scrollbar-width: none;
  /* For Firefox */
  -ms-overflow-style: none;
  /* For Internet Explorer and Edge */
}

html::-webkit-scrollbar {
  width: 0px;
  /* For Chrome, Safari, and Opera */
}
</style>