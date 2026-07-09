<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height: 90vh;">
    <div class="card shadow" style="max-width: 850px; width: 100%;">
      <div class="row g-0">

        <!-- left side -->
        <div class="col-md-5 text-white p-4" style="background-color: #1a1a2e;">
          <h3 class="mb-3">
            <i class="fa-solid fa-mountain-sun text-warning me-2"></i>
            Trek Journey
          </h3>

          <p class="text-white-50">
            Create an account and start booking your trekking journey.
          </p>

          <div class="text-center mt-5 mb-5">
            <i class="fa-solid fa-person-hiking fa-5x text-warning mb-3"></i>
            <p class="small text-white-50">
              It's not the mountain we conquer, but ourselves.
            </p>
          </div>

          <p class="small text-white-50">
            Registering will create a User account.
          </p>
        </div>

        <!-- right side -->
        <div class="col-md-7 p-4 bg-white">
          <p class="text-end text-muted small">
            College Project (23f2004623)
          </p>

          <h2>Create User Account</h2>
          <p class="text-muted">
            Register as a trekker to continue.
          </p>

          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }} 
            <button
              type="button"
              class="btn-close float-end"
              @click="errorMessage = ''"
            ></button>
          </div>

          <div v-if="successMessage" class="alert alert-success">
            {{ successMessage }}
            <button
              type="button"
              class="btn-close float-end"
              @click="successMessage = ''"
            ></button>
          </div>

          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label class="form-label">Full Name</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa-solid fa-user"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  v-model="fullName"
                  placeholder="John Doe"
                  required
                >
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Username</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa-solid fa-user-tag"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  v-model="username"
                  placeholder="johndoe12"
                  required
                >
              </div>
            </div>

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
                  placeholder="john@email.com"
                  required
                >
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Contact Number</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fa-solid fa-phone"></i>
                </span>
                <input
                  type="text"
                  class="form-control"
                  v-model="contactNumber"
                  placeholder="9876543210"
                  required
                >
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
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

              <div class="col-md-6 mb-3">
                <label class="form-label">Confirm Password</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="fa-solid fa-lock"></i>
                  </span>
                  <input
                    type="password"
                    class="form-control"
                    v-model="confirmPassword"
                    placeholder="Confirm password"
                    required
                  >
                </div>
              </div>
            </div>

            <button
              type="submit"
              class="btn btn-primary w-100 mt-2"
              :disabled="loading"
            >
              <span
                v-if="loading"
                class="spinner-border spinner-border-sm me-2"
              ></span>
              Register
            </button>
          </form>

          <div class="text-center mt-3">
            <router-link to="/login">
              Already have an account? Login here
            </router-link>
          </div>

          <div class="alert alert-info mt-4">
            <small>
              <b>Note:</b> Only users can register themselves.
              Staff and admin accounts are created internally.
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
      fullName: '',
      username: '',
      email: '',
      contactNumber: '',
      password: '',
      confirmPassword: '',
      errorMessage: '',
      successMessage: '',
      loading: false
    }
  },

  methods: {
    async handleRegister() {
      if (this.password != this.confirmPassword) {
        this.errorMessage = 'Passwords do not match.'
        return
      }

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch('/api/auth/register', {
          method: 'POST',
          body: {
            fullName: this.fullName,
            full_name: this.fullName,
            username: this.username,
            email: this.email,
            contact_number: this.contactNumber,
            password: this.password,
            confirm_password: this.confirmPassword
          }
        })

        let data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || 'Registration failed')
        }

        this.successMessage = data.message

        this.fullName = ''
        this.username = ''
        this.email = ''
        this.contactNumber = ''
        this.password = ''
        this.confirmPassword = ''

        setTimeout(() => {
          this.$router.push('/login')
        }, 1500)

      } catch (error) {
        this.errorMessage = error.message
      }

      this.loading = false
    }
  }
}
</script>