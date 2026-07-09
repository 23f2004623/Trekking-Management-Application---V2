<template>
  <div>
    <!-- navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <router-link class="navbar-brand" to="/admin">
        <i class="fa-solid fa-mountain-sun text-warning me-2"></i>
        Trek Journey
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#adminNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="adminNavbar">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin">
              <i class="fa-solid fa-chart-line"></i>
              Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/admin/manage_treks">
              <i class="fa-solid fa-mountain"></i>
              Treks
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link active" to="/admin/manage_staff">
              <i class="fa-solid fa-person-hiking"></i>
              Trekking Staff
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/admin/manage_users">
              <i class="fa-solid fa-users"></i>
              Users
            </router-link>
          </li>
        </ul>

        <button class="btn btn-outline-danger btn-sm" @click="handleLogout">
          <i class="fa-solid fa-right-from-bracket me-1"></i>
          Logout
        </button>
      </div>
    </nav>

    <!-- main content -->
    <div class="main-wrapper">
      <nav class="navbar navbar-light bg-white shadow-sm mb-4 px-4 py-3">
        <div class="container-fluid p-0">
          <h4 class="m-0">Dashboard Overview</h4>

          <div>
            <span class="badge bg-primary me-2">
              Admin Panel
            </span>
            <span class="text-muted small">
              Welcome, Admin
            </span>
          </div>
        </div>
      </nav>

      <!-- cards -->
      <div class="row g-3 mb-4">
        <div class="col-md-3">
          <div class="card shadow-sm p-3">
            <h6 class="text-muted">Total Treks</h6>
            <h3>{{ stats.total_treks }}</h3>
            <i class="fa-solid fa-mountain fa-2x text-primary"></i>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm p-3">
            <h6 class="text-muted">Total Users</h6>
            <h3>{{ stats.total_users }}</h3>
            <i class="fa-solid fa-users fa-2x text-success"></i>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm p-3">
            <h6 class="text-muted">Total Staff</h6>
            <h3>{{ stats.total_staff }}</h3>
            <i class="fa-solid fa-person-hiking fa-2x text-warning"></i>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm p-3">
            <h6 class="text-muted">Total Bookings</h6>
            <h3>{{ stats.total_bookings }}</h3>
            <i class="fa-solid fa-calendar-check fa-2x text-info"></i>
          </div>
        </div>
      </div>

      <!-- booking table -->
      <div class="card shadow-sm p-4 mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5>Recent Booking Log</h5>

          <button class="btn btn-outline-primary btn-sm" @click="toggleViewMode">
            {{ showAllBookings ? 'Show Recent' : 'View All Bookings' }}
          </button>
        </div>

        <div v-if="loading" class="text-center p-5">
          <div class="spinner-border text-primary"></div>
        </div>

        <div v-else-if="filteredBookings.length == 0" class="alert alert-light text-center">
          No bookings exist in the system yet.
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Booking ID</th>
                <th>User</th>
                <th>Trek Name</th>
                <th>Booking Date</th>
                <th class="text-center">Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="booking in filteredBookings" :key="booking.id">
                <td>
                  #B{{ String(booking.id).padStart(4, '0') }}
                </td>

                <td>
                  <b>{{ booking.user_name }}</b>
                  <br>
                  <small class="text-muted">{{ booking.user_email }}</small>
                </td>

                <td>
                  <b>{{ booking.trek_name }}</b>
                  <br>
                  <small class="text-muted">
                    {{ booking.trek_location }} | Starts: {{ booking.trek_start_date }}
                  </small>
                </td>

                <td>
                  {{ booking.booking_date }}
                </td>

                <td class="text-center">
                  <span class="badge" :class="getStatusClass(booking.status)">
                    {{ booking.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stats: {
        total_treks: 0,
        total_users: 0,
        total_staff: 0,
        total_bookings: 0
      },

      recentBookings: [],
      allBookings: [],
      showAllBookings: false,
      loading: true
    }
  },

  computed: {
    filteredBookings() {
      if (this.showAllBookings) {
        return this.allBookings
      } else {
        return this.recentBookings
      }
    }
  },

  methods: {
    async fetchDashboardStats() {
      this.loading = true

      try {
        let response = await window.apiFetch('/api/admin/dashboard')
        let data = await response.json()

        if (response.ok) {
          this.stats = data.stats
          this.recentBookings = data.recent_bookings
        }
      } catch (error) {
        console.log(error)
      }

      this.loading = false
    },

    async fetchAllBookings() {
      try {
        let response = await window.apiFetch('/api/admin/bookings')
        let data = await response.json()

        if (response.ok) {
          this.allBookings = data
        }
      } catch (error) {
        console.log(error)
      }
    },

    async toggleViewMode() {
      if (this.showAllBookings == true) {
        this.showAllBookings = false
      } else {
        this.showAllBookings = true

        if (this.allBookings.length == 0) {
          this.loading = true
          await this.fetchAllBookings()
          this.loading = false
        }
      }
    },

    getStatusClass(status) {
      if (status == 'Booked') {
        return 'bg-success'
      } else if (status == 'Cancelled') {
        return 'bg-danger'
      } else if (status == 'Completed') {
        return 'bg-primary'
      } else {
        return 'bg-secondary'
      }
    },

    handleLogout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },

  created() {
    this.fetchDashboardStats()
  }
}
</script>