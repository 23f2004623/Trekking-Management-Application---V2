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
            <router-link class="nav-link" to="/admin/treks">
              <i class="fa-solid fa-mountain"></i>
              Treks
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/admin/staff">
              <i class="fa-solid fa-person-hiking"></i>
              Trekking Staff
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link active" to="/admin/users">
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
    <div class="container-fluid p-4">
      <nav class="navbar navbar-light bg-white shadow-sm mb-4 px-4 py-3">
        <div class="container-fluid p-0">
          <div>
            <h4 class="m-0">Manage Users</h4>
            <small class="text-muted">
              View and manage registered trekkers
            </small>
          </div>
        </div>
      </nav>

      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
        <button class="btn-close float-end" @click="successMessage = ''"></button>
      </div>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
        <button class="btn-close float-end" @click="errorMessage = ''"></button>
      </div>

      <div class="card shadow-sm p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="mb-0">Registered Trekkers</h5>

          <div style="max-width: 300px; width: 100%;">
            <input
              type="text"
              class="form-control"
              v-model="searchQuery"
              placeholder="Search users"
              @input="fetchUsers"
            >
          </div>
        </div>

        <div v-if="loading" class="text-center p-5">
          <div class="spinner-border text-primary"></div>
        </div>

        <div v-else-if="usersList.length == 0" class="text-center p-5">
          <i class="fa-solid fa-users-slash text-muted fa-3x mb-3"></i>
          <p class="text-muted">No users found.</p>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>User ID</th>
                <th>Username</th>
                <th>Full Name</th>
                <th>Email</th>
                <th>Contact</th>
                <th>Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(user, index) in usersList" :key="user.id">
                <td>
                  #US{{ String(index + 1).padStart(4, '0') }}
                </td>

                <td>
                  {{ user.username }}
                </td>

                <td>
                  {{ user.full_name }}
                </td>

                <td>
                  {{ user.email }}
                </td>

                <td>
                  {{ user.contact_number || 'N/A' }}
                </td>

                <td>
                  <span class="badge" :class="getStatusClass(user.status)">
                    {{ user.status }}
                  </span>
                </td>

                <td class="text-center">
                  <button
                    v-if="user.status == 'active'"
                    class="btn btn-sm btn-danger me-1"
                    @click="toggleUserStatus(user, 'blacklisted')"
                  >
                    Blacklist
                  </button>

                  <button
                    v-else
                    class="btn btn-sm btn-success me-1"
                    @click="toggleUserStatus(user, 'active')"
                  >
                    Whitelist
                  </button>

                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="deleteUser(user.id)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="alert alert-info mt-4 mb-0">
          <small>
            <b>Info:</b> Blacklisted users cannot login or make bookings.
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
      usersList: [],
      searchQuery: '',
      loading: true,
      successMessage: '',
      errorMessage: ''
    }
  },

  methods: {
    async fetchUsers() {
      this.loading = true

      try {
        let endpoint = '/api/admin/users'

        if (this.searchQuery.trim() != '') {
          endpoint = '/api/admin/search?type=user&q=' + encodeURIComponent(this.searchQuery)
        }

        let response = await window.apiFetch(endpoint)
        let data = await response.json()

        if (response.ok) {
          this.usersList = data
        }
      } catch (error) {
        console.log(error)
      }

      this.loading = false
    },

    async toggleUserStatus(user, newStatus) {
      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch('/api/admin/users/' + user.id + '/status', {
          method: 'PUT',
          body: {
            status: newStatus
          }
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.fetchUsers()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to change user status.'
      }
    },

    async deleteUser(userId) {
      let check = confirm('Are you sure you want to delete this user?')

      if (check == false) {
        return
      }

      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch('/api/admin/users/' + userId, {
          method: 'DELETE'
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.fetchUsers()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to delete user.'
      }
    },

    getStatusClass(status) {
      if (status == 'active') {
        return 'bg-success'
      } else {
        return 'bg-danger'
      }
    },

    handleLogout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },

  created() {
    this.fetchUsers()
  }
}
</script>