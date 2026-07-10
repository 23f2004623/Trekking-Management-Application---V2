<template>
  <div
    style="
      min-height: 100vh;
      background-color: #f2f4f7;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 25px;
      box-sizing: border-box;
      font-family: Arial, Helvetica, sans-serif;
    "
  >
    <div
      style="
        width: 100%;
        max-width: 900px;
        background-color: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
        display: flex;
        flex-wrap: wrap;
      "
    >
      <!-- left side -->
      <div
        style="
          background-color: #1a1a2e;
          color: white;
          padding: 35px;
          flex: 1;
          min-width: 280px;
          box-sizing: border-box;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        "
      >
        <div>
          <h2
            style="
              margin-top: 0;
              margin-bottom: 15px;
              color: white;
              font-size: 26px;
            "
          >
            <span style="color: #ffc107; margin-right: 8px;">▲</span>
            Trek Journey
          </h2>

          <p
            style="
              color: #c7c7d1;
              line-height: 1.6;
              font-size: 14px;
            "
          >
            Create an account and start booking your trekking journey.
          </p>
        </div>

        <div
          style="
            text-align: center;
            margin-top: 40px;
            margin-bottom: 40px;
          "
        >
          <div
            style="
              font-size: 70px;
              color: #ffc107;
              margin-bottom: 15px;
            "
          >
            ▲
          </div>

          <p
            style="
              color: #c7c7d1;
              font-size: 13px;
              line-height: 1.6;
              font-style: italic;
            "
          >
            It's not the mountain we conquer, but ourselves.
          </p>
        </div>

        <p
          style="
            color: #aaaabc;
            font-size: 12px;
            margin-bottom: 0;
          "
        >
          Registering will create a User account.
        </p>
      </div>

      <!-- right side -->
      <div
        style="
          flex: 1.4;
          min-width: 320px;
          padding: 35px;
          box-sizing: border-box;
          background-color: white;
        "
      >
      

        <h2
          style="
            margin-top: 0;
            margin-bottom: 8px;
            color: #222;
            font-size: 27px;
          "
        >
          Create User Account
        </h2>

        <p
          style="
            color: #777;
            font-size: 14px;
            margin-top: 0;
            margin-bottom: 22px;
          "
        >
          Register as a trekker to continue.
        </p>

        <!-- error message -->
        <div
          v-if="errorMessage"
          style="
            background-color: #f8d7da;
            color: #842029;
            border: 1px solid #f5c2c7;
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 16px;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          "
        >
          <span>{{ errorMessage }}</span>

          <button
            type="button"
            @click="errorMessage = ''"
            style="
              background: none;
              border: none;
              color: #842029;
              font-size: 18px;
              cursor: pointer;
            "
          >
            ×
          </button>
        </div>

        <!-- success message -->
        <div
          v-if="successMessage"
          style="
            background-color: #d1e7dd;
            color: #0f5132;
            border: 1px solid #badbcc;
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 16px;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          "
        >
          <span>{{ successMessage }}</span>

          <button
            type="button"
            @click="successMessage = ''"
            style="
              background: none;
              border: none;
              color: #0f5132;
              font-size: 18px;
              cursor: pointer;
            "
          >
            ×
          </button>
        </div>

        <form @submit.prevent="handleRegister">
          <!-- full name -->
          <div style="margin-bottom: 15px;">
            <label
              style="
                display: block;
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 6px;
              "
            >
              Full Name
            </label>

            <input
              v-model="fullName"
              type="text"
              placeholder="John Doe"
              required
              style="
                width: 100%;
                height: 41px;
                padding: 0 12px;
                border: 1px solid #cfd4da;
                border-radius: 5px;
                font-size: 14px;
                box-sizing: border-box;
                background-color: #f9f9f9;
                color: #222;
                outline: none;
              "
            >
          </div>

          <!-- username -->
          <div style="margin-bottom: 15px;">
            <label
              style="
                display: block;
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 6px;
              "
            >
              Username
            </label>

            <input
              v-model="username"
              type="text"
              placeholder="johndoe12"
              required
              style="
                width: 100%;
                height: 41px;
                padding: 0 12px;
                border: 1px solid #cfd4da;
                border-radius: 5px;
                font-size: 14px;
                box-sizing: border-box;
                background-color: #f9f9f9;
                color: #222;
                outline: none;
              "
            >
          </div>

          <!-- email -->
          <div style="margin-bottom: 15px;">
            <label
              style="
                display: block;
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 6px;
              "
            >
              Email Address
            </label>

            <input
              v-model="email"
              type="email"
              placeholder="john@email.com"
              required
              style="
                width: 100%;
                height: 41px;
                padding: 0 12px;
                border: 1px solid #cfd4da;
                border-radius: 5px;
                font-size: 14px;
                box-sizing: border-box;
                background-color: #f9f9f9;
                color: #222;
                outline: none;
              "
            >
          </div>

          <!-- contact -->
          <div style="margin-bottom: 15px;">
            <label
              style="
                display: block;
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 6px;
              "
            >
              Contact Number
            </label>

            <input
              v-model="contactNumber"
              type="text"
              placeholder="9876543210"
              required
              style="
                width: 100%;
                height: 41px;
                padding: 0 12px;
                border: 1px solid #cfd4da;
                border-radius: 5px;
                font-size: 14px;
                box-sizing: border-box;
                background-color: #f9f9f9;
                color: #222;
                outline: none;
              "
            >
          </div>

          <!-- passwords -->
          <div
            style="
              display: flex;
              gap: 12px;
              flex-wrap: wrap;
              margin-bottom: 18px;
            "
          >
            <div style="flex: 1; min-width: 180px;">
              <label
                style="
                  display: block;
                  color: #333;
                  font-size: 14px;
                  font-weight: bold;
                  margin-bottom: 6px;
                "
              >
                Password
              </label>

              <input
                v-model="password"
                type="password"
                placeholder="Enter password"
                required
                style="
                  width: 100%;
                  height: 41px;
                  padding: 0 12px;
                  border: 1px solid #cfd4da;
                  border-radius: 5px;
                  font-size: 14px;
                  box-sizing: border-box;
                  background-color: #f9f9f9;
                  color: #222;
                  outline: none;
                "
              >
            </div>

            <div style="flex: 1; min-width: 180px;">
              <label
                style="
                  display: block;
                  color: #333;
                  font-size: 14px;
                  font-weight: bold;
                  margin-bottom: 6px;
                "
              >
                Confirm Password
              </label>

              <input
                v-model="confirmPassword"
                type="password"
                placeholder="Confirm password"
                required
                style="
                  width: 100%;
                  height: 41px;
                  padding: 0 12px;
                  border: 1px solid #cfd4da;
                  border-radius: 5px;
                  font-size: 14px;
                  box-sizing: border-box;
                  background-color: #f9f9f9;
                  color: #222;
                  outline: none;
                "
              >
            </div>
          </div>

          <!-- register button -->
          <button
            type="submit"
            :disabled="loading"
            :style="{
              width: '100%',
              height: '43px',
              border: 'none',
              borderRadius: '5px',
              backgroundColor: loading ? '#7baaf7' : '#0d6efd',
              color: 'white',
              fontSize: '15px',
              fontWeight: 'bold',
              cursor: loading ? 'not-allowed' : 'pointer'
            }"
          >
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>

        <!-- login link -->
        <div
          style="
            text-align: center;
            margin-top: 18px;
          "
        >
          <router-link
            to="/login"
            style="
              color: #0d6efd;
              font-size: 14px;
              text-decoration: none;
            "
          >
            Already have an account? Login here
          </router-link>
        </div>

        <!-- note -->
        <div
          style="
            background-color: #cff4fc;
            color: #055160;
            border: 1px solid #b6effb;
            padding: 12px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 13px;
            line-height: 1.5;
          "
        >
          <b>Note:</b> Only users can register themselves. Staff and admin
          accounts are created internally.
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