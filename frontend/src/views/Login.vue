<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height: 90vh;">
    <div class="card shadow" style="max-width: 850px; width: 100%;">
      <div class="row g-0">

        <!-- left part -->
        <div class="col-md-5 text-white p-4" style="background-color: #1a1a2e;">
          <h3 class="mb-3">
            <i class="fa-solid fa-mountain-sun text-warning me-2"></i>
            Trek Journey
          </h3>

          <p class="text-white-50">
            Trekking Management Application for trek booking and management.
          </p>

          <h6 class="text-warning mt-4">Select Role</h6>

          <div
            class="role-box"
            :class="{ active: activeRole == 'admin' }"
            @click="selectRole('admin')"
          >
            <i class="fa-solid fa-user-shield me-2"></i>
            Admin
            <br>
            <small>Manage treks, users and staff</small>
          </div>

          <div
            class="role-box"
            :class="{ active: activeRole == 'staff' }"
            @click="selectRole('staff')"
          >
            <i class="fa-solid fa-person-hiking me-2"></i>
            Trekking Staff
            <br>
            <small>Manage assigned treks</small>
          </div>

          <div
            class="role-box"
            :class="{ active: activeRole == 'user' }"
            @click="selectRole('user')"
          >
            <i class="fa-solid fa-users me-2"></i>
            User
            <br>
            <small>Book and explore treks</small>
          </div>

          <p class="small text-white-50 mt-4">
            Selected role is only for login profile highlight.
          </p>
        </div>

        <!-- login form -->
        <div class="col-md-7 p-4 bg-white">
          <h2>Welcome Back</h2>
          <p class="text-muted">Login to continue your trekking journey.</p>

          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
            <button type="button" class="btn-close float-end" @click="errorMessage = ''"></button>
          </div>

          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label class="form-label">Email address</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa-solid fa-envelope"></i>
                </span>
                <input
                  type="email"
                  class="form-control"
                  v-model="email"
                  placeholder="email@tma.com"
                  required
                >
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Password</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa-solid fa-lock"></i>
                </span>
                <input
                  type="password"
                  class="form-control"
                  v-model="password"
                  placeholder="Enter password"
                  required
                >
              </div>
            </div>

            <div class="form-check mb-3">
              <input
                type="checkbox"
                class="form-check-input"
                id="rememberMe"
                v-model="rememberMe"
              >
              <label for="rememberMe" class="form-check-label">
                Remember me
              </label>
            </div>

            <button class="btn btn-primary w-100" type="submit" :disabled="loading">
              <span
                v-if="loading"
                class="spinner-border spinner-border-sm me-2"
              ></span>
              Login
            </button>
          </form>

          <div class="text-center mt-3">
            <router-link to="/register">
              Don't have an account? Register as User
            </router-link>
          </div>

          <div class="alert alert-info mt-4">
            <small>
              <b>Note:</b> Only users can register themselves.
              Staff accounts are created by admin.
            </small>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      activeRole: 'user',
      errorMessage: '',
      loading: false
    }
  },

  methods: {
    selectRole(role) {
      this.activeRole = role

      if (role == 'admin') {
        this.email = 'example@tma.com'
      } else if (role == 'staff') {
        this.email = 'example@tma.com'
      } else {
        this.email = ''
      }
    },

    async handleLogin() {
      this.loading = true
      this.errorMessage = ''

      try {
        let response = await window.apiFetch('/api/auth/login', {
          method: 'POST',
          body: {
            email: this.email,
            password: this.password
          }
        })

        let data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || 'Login failed')
        }

        localStorage.setItem('token', data.token)
        localStorage.setItem('role', data.user.role)
        localStorage.setItem('user', JSON.stringify(data.user))

        if (data.user.role == 'admin') {
          this.$router.push('/admin')
        } else if (data.user.role == 'staff') {
          this.$router.push('/staff')
        } else {
          this.$router.push('/user')
        }

      } catch (error) {
        this.errorMessage = error.message
      }

      this.loading = false
    }
  },

  created() {
    let token = localStorage.getItem('token')
    let role = localStorage.getItem('role')

    if (token && role) {
      if (role == 'admin') {
        this.$router.push('/admin')
      } else if (role == 'staff') {
        this.$router.push('/staff')
      } else {
        this.$router.push('/user')
      }
    }
  }
}
</script>

<style scoped>
.role-box {
  border: 1px solid #777;
  padding: 10px;
  border-radius: 6px;
  margin-top: 12px;
  cursor: pointer;
}

.role-box small {
  color: #ccc;
}

.active {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>