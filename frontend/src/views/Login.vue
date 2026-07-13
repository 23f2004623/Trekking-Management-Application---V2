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
        max-width: 850px;
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
        "
      >
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
            margin-bottom: 30px;
          "
        >
          Trekking Management Application for trek booking and management.
        </p>

        <h4
          style="
            color: #ffc107;
            margin-bottom: 15px;
            font-size: 16px;
          "
        >
          Select Role
        </h4>

        <!-- admin role -->
        <div
          @click="selectRole('admin')"
          :style="{
            border: activeRole == 'admin'
              ? '1px solid #0d6efd'
              : '1px solid #55556d',
            backgroundColor: activeRole == 'admin'
              ? '#0d6efd'
              : 'transparent',
            padding: '12px',
            borderRadius: '6px',
            marginBottom: '12px',
            cursor: 'pointer'
          }"
        >
          <div style="font-size: 15px; font-weight: bold;">
            Admin
          </div>

          <div
            style="
              color: #d2d2dc;
              font-size: 12px;
              margin-top: 5px;
            "
          >
            Manage treks, users and staff
          </div>
        </div>

        <!-- staff role -->
        <div
          @click="selectRole('staff')"
          :style="{
            border: activeRole == 'staff'
              ? '1px solid #0d6efd'
              : '1px solid #55556d',
            backgroundColor: activeRole == 'staff'
              ? '#0d6efd'
              : 'transparent',
            padding: '12px',
            borderRadius: '6px',
            marginBottom: '12px',
            cursor: 'pointer'
          }"
        >
          <div style="font-size: 15px; font-weight: bold;">
            Trekking Staff
          </div>

          <div
            style="
              color: #d2d2dc;
              font-size: 12px;
              margin-top: 5px;
            "
          >
            Manage assigned treks
          </div>
        </div>

        <!-- user role -->
        <div
          @click="selectRole('user')"
          :style="{
            border: activeRole == 'user'
              ? '1px solid #0d6efd'
              : '1px solid #55556d',
            backgroundColor: activeRole == 'user'
              ? '#0d6efd'
              : 'transparent',
            padding: '12px',
            borderRadius: '6px',
            marginBottom: '12px',
            cursor: 'pointer'
          }"
        >
          <div style="font-size: 15px; font-weight: bold;">
            User
          </div>

          <div
            style="
              color: #d2d2dc;
              font-size: 12px;
              margin-top: 5px;
            "
          >
            Book and explore treks
          </div>
        </div>

        <p
          style="
            color: #aaaabc;
            font-size: 12px;
            margin-top: 25px;
            line-height: 1.5;
          "
        >
          Selected role is only used to highlight the login profile.
        </p>
      </div>

      <!-- right side -->
      <div
        style="
          flex: 1.3;
          min-width: 300px;
          padding: 40px;
          box-sizing: border-box;
          background-color: white;
        "
      >
        <h2
          style="
            margin-top: 0;
            margin-bottom: 8px;
            color: #222;
            font-size: 28px;
          "
        >
          Welcome Back
        </h2>

        <p
          style="
            color: #777;
            font-size: 14px;
            margin-top: 0;
            margin-bottom: 25px;
          "
        >
          Login to continue your trekking journey.
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
            margin-bottom: 18px;
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

        <form @submit.prevent="handleLogin">
          <!-- email -->
          <div style="margin-bottom: 18px;">
            <label
              for="email"
              style="
                display: block;
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 7px;
              "
            >
              Email Address
            </label>

            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="email@tma.com"
              required
              style="
                width: 100%;
                height: 42px;
                padding: 0 12px;
                border: 1px solid #cfd4da;
                border-radius: 5px;
                font-size: 14px;
                box-sizing: border-box;
                outline: none;
                background-color: #f9f9f9;
                color: #222;
              "
            >
          </div>

          <!-- password -->
          <div style="margin-bottom: 16px;">
            <label
              for="password"
              style="
                display: block;
                color: #333;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 7px;
              "
            >
              Password
            </label>

            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter password"
              required
              style="
                width: 100%;
                height: 42px;
                padding: 0 12px;
                border: 1px solid #cfd4da;
                border-radius: 5px;
                font-size: 14px;
                box-sizing: border-box;
                outline: none;
                background-color: #f9f9f9;
                color: #222;
              "
            >
          </div>

          <!-- login button -->
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
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <!-- register link -->
        <div
          style="
            text-align: center;
            margin-top: 20px;
          "
        >
          <router-link
            to="/register"
            style="
              color: #0d6efd;
              font-size: 14px;
              text-decoration: none;
            "
          >
            Don't have an account? Register as User
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
            margin-top: 22px;
            font-size: 13px;
            line-height: 1.5;
          "
        >
          <b>Note:</b> Only users can register themselves. Staff accounts are
          created by admin.
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