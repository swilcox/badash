<template>
<div>
  <v-list-tile @click.stop="loginDialog=true">
    <v-list-tile-title><v-icon>account_box</v-icon> Login</v-list-tile-title>
  </v-list-tile>
  <v-dialog v-model="loginDialog" max-width="500px">
    <v-form v-model="valid" ref="form" @submit.stop.prevent="handleSubmit" lazy-validation>
    <v-card>
    <v-card-title>
      <span class="headline"><v-icon>account_box</v-icon> Login</span>
    </v-card-title>
    <v-card-text>
      <v-container grid-list-md>
      <v-layout wrap>
        <v-flex xs12>
        <v-text-field label="Email / Username" v-model="username" required></v-text-field>
        </v-flex>
        <v-flex xs12>
        <v-text-field label="Password" type="password" v-model="password" required></v-text-field>
        </v-flex>
      </v-layout>
      </v-container>
      <small>*indicates required field</small>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="gray darken-1" @click.native="loginDialog = false">Cancel</v-btn>
      <v-btn color="blue darken-1" type="submit">Login</v-btn>
    </v-card-actions>
    </v-card>
    </v-form>
  </v-dialog>
</div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      loginDialog: false,
      errorMessage: null,
      successMessage: null,
      disableAllInputs: false,
      protectedUI: false,
      username: '',
      password: '',
      valid: true
    }
  },
  methods: {
    handleSubmit () {
      this.successMessage = null
      this.errorMessage = null
      this.protectedUI = true
      console.log('made it here! to submit login')
      this.$store.dispatch('authenticateUser', {
        username: this.username,
        password: this.password
      }).then(() => {
        this.disableAllInputs = true
        this.password = ''
        this.errorMessage = null
        this.successMessage = 'Successfuly signed in'
        console.log(this.$store.state.cognito.user.username)
        this.$store.dispatch('getUserAttributes').then(() => {
          console.log(this.$store.state.cognito.user.attributes)
        })
      }).catch((err) => {
        this.errorMessage = err.message
        this.protectedUI = false
      })
    }
  }
}
</script>

<style>
</style>