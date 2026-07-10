<template>
  <div>
    <!-- navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <router-link class="navbar-brand" to="/staff">
        <i class="fa-solid fa-mountain-sun text-warning me-2"></i>
        Trek Journey
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#staffNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="staffNavbar">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link active" to="/staff">
              <i class="fa-solid fa-table-columns me-1"></i>
              My Dashboard
            </router-link>
          </li>
        </ul>

        <span class="text-white me-3 small">
          Welcome, {{ staffName }}
        </span>

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
        <div class="d-flex justify-content-between align-items-center">
          <h4 class="m-0">My Dashboard</h4>

          <span class="badge bg-success">
            <i class="fa-solid fa-person-hiking me-1"></i>
            Staff Member
          </span>
        </div>
      </div>

      <!-- loading -->
      <div v-if="loading" class="text-center p-5">
        <div class="spinner-border text-primary"></div>
      </div>

      <div v-else>
        <!-- dashboard cards -->
        <div class="row g-3 mb-4">
          <div class="col-md-4">
            <div class="card shadow-sm p-3 h-100">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="text-muted">Assigned Treks</h6>
                  <h3>{{ stats.assigned_treks_count }}</h3>
                </div>

                <i class="fa-solid fa-mountain fa-2x text-primary"></i>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card shadow-sm p-3 h-100">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="text-muted">Total Participants</h6>
                  <h3>{{ stats.total_participants }}</h3>
                </div>

                <i class="fa-solid fa-users fa-2x text-success"></i>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card shadow-sm p-3 h-100">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="text-muted">Ongoing Treks</h6>
                  <h3>{{ stats.ongoing_treks_count }}</h3>
                </div>

                <i class="fa-solid fa-route fa-2x text-warning"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- assigned treks -->
        <div class="card shadow-sm p-4">
          <h5 class="mb-3">
            <i class="fa-solid fa-folder-open text-primary me-2"></i>
            My Assigned Treks
          </h5>

          <div
            v-if="assignedTreks.length == 0"
            class="alert alert-light text-center p-4"
          >
            <i class="fa-solid fa-mountain-sun text-muted fa-2x mb-2"></i>

            <p class="text-muted mb-0">
              You are not assigned to any trek. Please contact admin.
            </p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>Trek Name</th>
                  <th>Location</th>
                  <th>Difficulty</th>
                  <th>Trek Dates</th>
                  <th>Available Slots</th>
                  <th>Status</th>
                  <th class="text-center">Action</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="trek in assignedTreks" :key="trek.id">
                  <td>
                    {{ trek.name }}
                  </td>

                  <td>
                    {{ trek.location }}
                  </td>

                  <td>
                    <span
                      class="badge"
                      :class="getDifficultyClass(trek.difficulty)"
                    >
                      {{ trek.difficulty }}
                    </span>
                  </td>

                  <td>
                    <div>{{ trek.start_date }}</div>
                    <small class="text-muted">
                      to {{ trek.end_date }}
                    </small>
                  </td>

                  <td>
                    {{ trek.available_slots }} / {{ trek.total_slots }}
                  </td>

                  <td>
                    <span
                      class="badge"
                      :class="getStatusClass(trek.status)"
                    >
                      {{ trek.status }}
                    </span>
                  </td>

                  <td class="text-center">
                    <router-link
                      :to="'/staff/trek/' + trek.id"
                      class="btn btn-primary btn-sm"
                    >
                      Manage
                      <i class="fa-solid fa-angle-right ms-1"></i>
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
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
      staffName: '',

      stats: {
        assigned_treks_count: 0,
        total_participants: 0,
        ongoing_treks_count: 0
      },

      assignedTreks: [],
      loading: true
    }
  },

  methods: {
    async fetchDashboardData() {
      this.loading = true

      try {
        let response = await window.apiFetch('/api/staff/dashboard')
        let data = await response.json()

        if (response.ok) {
          this.stats = data.stats
          this.assignedTreks = data.assigned_treks
        }
      } catch (error) {
        console.log(error)
      }

      this.loading = false
    },

    getDifficultyClass(diff) {
      if (diff == 'Easy') {
        return 'badge-easy'
      } else if (diff == 'Moderate') {
        return 'badge-moderate'
      } else if (diff == 'Hard') {
        return 'badge-hard'
      } else {
        return 'bg-secondary'
      }
    },

    getStatusClass(status) {
      if (status == 'Open') {
        return 'badge-open'
      } else if (status == 'Closed') {
        return 'badge-closed'
      } else if (status == 'Pending') {
        return 'badge-pending'
      } else if (status == 'Completed') {
        return 'badge-completed'
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
    let userData = localStorage.getItem('user')

    if (userData) {
      let user = JSON.parse(userData)
      this.staffName = user.full_name
    }

    this.fetchDashboardData()
  }
}
</script>