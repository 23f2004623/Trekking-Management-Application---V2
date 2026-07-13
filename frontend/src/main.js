import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

window.apiFetch = async function(endpoint, options = {}) {
  let token = localStorage.getItem('token')

  let config = {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  }

  if (token) {
    config.headers['Authorization'] = 'Bearer ' + token
  }

  if (options.body) {
    config.body = JSON.stringify(options.body)
  }

  let response = await fetch(
    'http://127.0.0.1:5000' + endpoint,
    config
  )

  return response
}

const app = createApp(App)

app.use(router)

app.mount('#app')