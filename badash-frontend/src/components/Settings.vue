<template>
  <v-container grid-list-md text-xs-center>
  <v-layout row wrap>
    <v-flex xs12>
      <h1>Settings</h1>
      <h2>API Keys</h2>
      <v-data-table
        v-bind:headers="tableHeaders"
        v-bind:items="apiKeys"
        :total-items="totalKeys"
        hide-actions
        :loading="loading"
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <td class="text-xs-left">{{ props.item.user }}</td>
          <td class="text-xs-left">{{ props.item._id }}</td>
          <td class="text-xs-left">{{ props.item.api_key }}</td>
          <td class="text-xs-right"><v-btn @click="deleteApiKey(props.item._id)">Delete</v-btn></td>
        </template>
      </v-data-table>
      <v-btn v-on:click="newApiKey">Add New API Key</v-btn>
    </v-flex>
  </v-layout>
  </v-container>
</template>

<script>
import { getAccessToken } from '@/utils/auth'

export default {
  name: 'settings',
  data () {
    return {
      tableHeaders: [
        {
          text: 'User ID',
          align: 'left',
          value: 'user',
          sortable: false
        },
        {
          text: 'ID',
          align: 'left',
          value: '_id',
          sortable: false
        },
        {
          text: 'API Key',
          align: 'left',
          value: 'api_key',
          sortable: false
        },
        {
          text: '',
          align: 'right',
          sortable: false
        }
      ],
      apiKeys: [],
      totalKeys: 0,
      loading: true,
      pagination: {}
    }
  },
  methods: {
    getApiKeys () {
      this.loading = true
      const token = getAccessToken()
      console.log(token)
      this.$http.get(`api_keys`, {headers: {'Authorization': 'Bearer ' + token, 'Access-Control-Allow-Origin': '*'}}).then(response => {
        this.apiKeys = response.body
        this.totalKeys = this.apiKeys.length
      },
      response => {
        console.log('error getting')
        console.log(response.statusText)
      })
      this.loading = false
    },
    newApiKey: function (event) {
      this.createApiKey()
    },
    createApiKey () {
      const token = getAccessToken()
      this.$http.post(`api_keys`, null, {headers: {'Authorization': 'Bearer ' + token, 'Access-Control-Allow-Origin': '*'}}).then(response => {
        this.getApiKeys()
      },
      response => {
        console.log('error requesting new API Key')
        console.log(response.statusText)
      })
    },
    deleteApiKey (id) {
      const token = getAccessToken()
      this.$http.delete(`api_keys/${id}`, {headers: {'Authorization': 'Bearer ' + token, 'Access-Control-Allow-Origin': '*'}}).then(response => {
        this.getApiKeys()
      },
      response => {
        console.log('error deleting API Key')
        console.log(response.statusText)
      })
    }
  },
  mounted () {
    this.getApiKeys()
  }
}
</script>

<style>
</style>