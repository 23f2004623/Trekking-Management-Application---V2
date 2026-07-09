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
    <div class="container-fluid p-4">
      <nav class="navbar navbar-light bg-white shadow-sm mb-4 px-4 py-3">
        <div class="container-fluid p-0">
          <div>
            <h4 class="m-0">Manage Trekking Staff</h4>
            <small class="text-muted">
              Create and manage trekking staff members
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

      <div class="row g-4">
        <!-- create staff form -->
        <div class="col-lg-5">
          <div class="card shadow-sm p-4">
            <h5 class="mb-3">
              <i class="fa-solid fa-user-plus text-primary me-2"></i>
              Create New Staff
            </h5>

            <form @submit.prevent="createStaff">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="form.full_name"
                  placeholder="Vikram Singh"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Email address</label>
                <input
                  type="email"
                  class="form-control"
                  v-model="form.email"
                  placeholder="staff@tma.com"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Contact Number</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="form.contact_number"
                  placeholder="9876543210"
                  required
                >
              </div>

              <div class="row">
                <div class="col-6 mb-3">
                  <label class="form-label">Password</label>
                  <input
                    type="password"
                    class="form-control"
                    v-model="form.password"
                    placeholder="Password"
                    required
                  >
                </div>

                <div class="col-6 mb-3">
                  <label class="form-label">Confirm Password</label>
                  <input
                    type="password"
                    class="form-control"
                    v-model="form.confirm_password"
                    placeholder="Confirm"
                    required
                  >
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Experience</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="form.experience"
                  placeholder="5 Years"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Specialization</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="form.specialization"
                  placeholder="High Altitude Rescue"
                >
              </div>

              <div class="mb-4">
                <label class="form-label">Status</label>
                <select class="form-select" v-model="form.status">
                  <option value="active">Active</option>
                  <option value="blacklisted">Blacklisted</option>
                </select>
              </div>

              <div class="d-flex justify-content-end gap-2">
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  @click="resetForm"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="creating"
                >
                  <span
                    v-if="creating"
                    class="spinner-border spinner-border-sm me-2"
                  ></span>
                  Create Staff
                </button>
              </div>
            </form>

            <div class="alert alert-warning mt-4 mb-0">
              <small>
                Staff will get login details after successful creation.
              </small>
            </div>
          </div>
        </div>

        <!-- staff table -->
        <div class="col-lg-7">
          <div class="card shadow-sm p-4 h-100">
            <h5 class="mb-3">
              <i class="fa-solid fa-list text-primary me-2"></i>
              Staff List
            </h5>

            <div class="mb-3">
              <input
                type="text"
                class="form-control"
                v-model="searchQuery"
                placeholder="Search staff members"
                @input="fetchStaffList"
              >
            </div>

            <div v-if="loading" class="text-center p-5">
              <div class="spinner-border text-primary"></div>
            </div>

            <div v-else-if="staffList.length == 0" class="text-center p-5">
              <i class="fa-solid fa-users-slash text-muted fa-3x mb-3"></i>
              <p class="text-muted">No staff members found.</p>
            </div>

            <div v-else class="table-responsive">
              <table class="table table-hover">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Staff Name</th>
                    <th>Specialization</th>
                    <th>Status</th>
                    <th class="text-center">Action</th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-for="(staff, index) in staffList" :key="staff.id">
                    <td>
                      #ST{{ String(index + 1).padStart(3, '0') }}
                    </td>

                    <td>
                      <b>{{ staff.full_name }}</b>
                      <br>
                      <small class="text-muted">
                        {{ staff.email }} | {{ staff.contact_number }}
                      </small>
                    </td>

                    <td>
                      <small>
                        {{ staff.specialization || 'N/A' }}
                      </small>
                      <br>
                      <small class="text-muted">
                        Exp: {{ staff.experience || 'N/A' }}
                      </small>
                    </td>

                    <td>
                      <span class="badge" :class="getStatusClass(staff.status)">
                        {{ staff.status }}
                      </span>
                    </td>

                    <td class="text-center">
                      <button
                        v-if="staff.status == 'active'"
                        class="btn btn-sm btn-danger me-1"
                        @click="toggleStatus(staff, 'blacklisted')"
                      >
                        Blacklist
                      </button>

                      <button
                        v-else
                        class="btn btn-sm btn-success me-1"
                        @click="toggleStatus(staff, 'active')"
                      >
                        Whitelist
                      </button>

                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteStaff(staff.id)"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="alert alert-info mt-3 mb-0">
              <small>
                <b>Info:</b> Blacklisted staff cannot login into the system.
              </small>
            </div>
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
      staffList: [],
      searchQuery: '',
      loading: true,
      creating: false,
      successMessage: '',
      errorMessage: '',

      form: {
        full_name: '',
        email: '',
        contact_number: '',
        password: '',
        confirm_password: '',
        experience: '',
        specialization: '',
        status: 'active'
      }
    }
  },

  methods: {
    async fetchStaffList() {
      this.loading = true

      try {
        let endpoint = '/api/admin/staff'

        if (this.searchQuery.trim() != '') {
          endpoint = '/api/admin/search?type=staff&q=' + encodeURIComponent(this.searchQuery)
        }

        let response = await window.apiFetch(endpoint)
        let data = await response.json()

        if (response.ok) {
          this.staffList = data
        }
      } catch (error) {
        console.log(error)
      }

      this.loading = false
    },

    async createStaff() {
      if (this.form.password != this.form.confirm_password) {
        this.errorMessage = 'Passwords do not match.'
        return
      }

      this.creating = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch('/api/admin/staff', {
          method: 'POST',
          body: this.form
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.resetForm()
          this.fetchStaffList()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to create staff member.'
      }

      this.creating = false
    },

    async toggleStatus(staff, newStatus) {
      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch('/api/admin/staff/' + staff.id + '/status', {
          method: 'PUT',
          body: {
            status: newStatus
          }
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.fetchStaffList()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to change status.'
      }
    },

    async deleteStaff(staffId) {
      let check = confirm('Are you sure you want to delete this staff?')

      if (check == false) {
        return
      }

      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch('/api/admin/staff/' + staffId, {
          method: 'DELETE'
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.fetchStaffList()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to delete staff member.'
      }
    },

    resetForm() {
      this.form = {
        full_name: '',
        email: '',
        contact_number: '',
        password: '',
        confirm_password: '',
        experience: '',
        specialization: '',
        status: 'active'
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
    this.fetchStaffList()
  }
}
</script>

<style scoped>
.x-text {
  font-size: 0.8rem;
}

.x-small {
  font-size: 0.7rem;
}
</style>