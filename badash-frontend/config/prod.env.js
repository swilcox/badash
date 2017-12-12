'use strict'
const baseURL = process.env.API_BASE_URL || 'http://localhost:8000'

module.exports = {
  NODE_ENV: '"production"',
  API_BASE_URL: `"` + baseURL + `"`
}
