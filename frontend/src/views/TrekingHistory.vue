<template>
  <div>
    <!-- navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <router-link class="navbar-brand" to="/user">
        <i class="fa-solid fa-mountain-sun text-warning me-2"></i>
        Trek Journey
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#userNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="userNavbar">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/user">
              <i class="fa-solid fa-house me-1"></i>
              Home
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/user/browse">
              <i class="fa-solid fa-magnifying-glass me-1"></i>
              Browse Treks
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link active" to="/user/history">
              <i class="fa-solid fa-clock-rotate-left me-1"></i>
              Trekking History
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
    <div class="container-fluid p-4">
      <!-- page heading -->
      <div class="bg-white shadow-sm p-3 mb-4">
        <h4 class="m-0">My Trekking History</h4>

        <small class="text-muted">
          Completed and cancelled trekking bookings
        </small>
      </div>

      <!-- history table -->
      <div class="card shadow-sm p-4">
        <div v-if="loading" class="text-center p-5">
          <div class="spinner-border text-primary"></div>
        </div>

        <div
          v-else-if="historyList.length == 0"
          class="text-center p-5"
        >
          <i class="fa-solid fa-history text-muted fa-3x mb-3"></i>

          <p class="text-muted">
            No completed or cancelled treks found.
          </p>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Trek Name</th>
                <th>Location</th>
                <th>Trek Dates</th>
                <th>Booking Date</th>
                <th class="text-center">Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="booking in historyList" :key="booking.id">
                <td>
                  {{ booking.trek_name }}
                </td>

                <td>
                  {{ booking.trek_location }}
                </td>

                <td>
                  {{ booking.trek_start_date }}
                  to
                  {{ booking.trek_end_date }}
                </td>

                <td>
                  {{ booking.booking_date }}
                </td>

                <td class="text-center">
                  <span
                    class="badge"
                    :class="getStatusClass(booking.status)"
                  >
                    {{ booking.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="alert alert-info mt-4 mb-0">
          <small>
            <b>Info:</b> This page shows all completed and cancelled bookings.
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      historyList: [],
      loading: true
    }
  },

  methods: {
    async fetchHistory() {
      this.loading = true

      try {
        let response = await window.apiFetch('/api/user/history')
        let data = await response.json()

        if (response.ok) {
          this.historyList = data
        }
      } catch (error) {
        console.log(error)
      }

      this.loading = false
    },

    getStatusClass(status) {
      if (status == 'Completed') {
        return 'bg-primary'
      } else if (status == 'Cancelled') {
        return 'bg-danger'
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
    this.fetchHistory()
  }
}
</script>