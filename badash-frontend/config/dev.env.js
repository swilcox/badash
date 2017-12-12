'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')
const baseURL = process.env.API_BASE_URL || 'http://localhost:8000'

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_BASE_URL: `"` + baseURL + `"`
})
