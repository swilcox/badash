# badash-frontend

> Vue.js-based frontend for badash

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Additional Required Configuration

### Auth0

Add a new file `badash-frontend/config/auth0.js`.

Contents of the file:

```js
export default {
    clientId: '<client id from auth0>',
    domain: '<domain from auth0>',
    redirect: 'http://localhost:8080/callback',
    audience: '<audience value from auth0>'
}
```

To setup an account and configure the client (to get the required settings) visit: https://auth0.com

Before deploying to production, you'd need to change the `redirect` value in the file to your production callback URL.

### Google Maps API

Add a new file `badash-frontend/config/google.js`.

Contents of the file:

```js
export default {
    mapsApiKey: '<your-google-maps-api-key>',
}
```

### API URL

before running the `npm` commands for building or running the dev server, you need to set the URL for the badash-api server.

```
$ export API_BASE_URL=http://localhost:8000/
```

Modify the URL as needed. Obviously, changing this prior to deploying a generated site to production with the production API URL.

