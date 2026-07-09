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
    <div class="main-wrapper">
      <nav class="navbar navbar-light bg-white shadow-sm mb-4 px-4 py-3">
        <div class="container-fluid p-0 d-flex justify-content-between align-items-center">
          <h4 class="m-0">Manage Treks</h4>

          <button class="btn btn-primary" @click="openCreateModal">
            <i class="fa-solid fa-plus me-1"></i>
            Add New Trek
          </button>
        </div>
      </nav>

      <!-- search -->
      <div class="card shadow-sm p-3 mb-4">
        <div class="row g-2">
          <div class="col-md-9">
            <input
              type="text"
              class="form-control"
              v-model="searchQuery"
              placeholder="Search treks by name or location"
              @input="handleSearch"
            >
          </div>

          <div class="col-md-3">
            <select
              class="form-select"
              v-model="difficultyFilter"
              @change="filterTreks"
            >
              <option value="All">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
        <button class="btn-close float-end" @click="successMessage = ''"></button>
      </div>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
        <button class="btn-close float-end" @click="errorMessage = ''"></button>
      </div>

      <!-- trek table -->
      <div class="card shadow-sm p-4">
        <div v-if="loading" class="text-center p-5">
          <div class="spinner-border text-primary"></div>
        </div>

        <div v-else-if="paginatedTreks.length == 0" class="text-center p-5">
          <i class="fa-solid fa-mountain text-muted fa-3x mb-3"></i>
          <p class="text-muted">No treks found.</p>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Trek Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Duration</th>
                <th>Slots</th>
                <th>Staff</th>
                <th>Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="trek in paginatedTreks" :key="trek.id">
                <td>#{{ trek.id }}</td>

                <td>
                  {{ trek.name }}
                </td>

                <td>
                  {{ trek.location }}
                </td>

                <td>
                  <span class="badge" :class="getDifficultyClass(trek.difficulty)">
                    {{ trek.difficulty }}
                  </span>
                </td>

                <td>
                  {{ trek.duration_days }} Days
                </td>

                <td>
                  {{ trek.available_slots }} / {{ trek.total_slots }}
                </td>

                <td>
                  {{ trek.assigned_staff_name || 'Unassigned' }}
                </td>

                <td>
                  <span class="badge" :class="getStatusClass(trek.status)">
                    {{ trek.status }}
                  </span>
                </td>

                <td class="text-center">
                  <button
                    class="btn btn-sm btn-outline-secondary me-1"
                    @click="openEditModal(trek)"
                  >
                    <i class="fa-solid fa-pen-to-square"></i>
                  </button>

                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="confirmDelete(trek)"
                  >
                    <i class="fa-solid fa-trash-can"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- pagination -->
        <nav
          v-if="totalPages > 1"
          class="d-flex justify-content-between align-items-center mt-3"
        >
          <span class="text-muted small">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }}
            to {{ Math.min(currentPage * itemsPerPage, filteredTreks.length) }}
            of {{ filteredTreks.length }} treks
          </span>

          <ul class="pagination pagination-sm m-0">
            <li class="page-item" :class="{ disabled: currentPage == 1 }">
              <button class="page-link" @click="currentPage--">
                Previous
              </button>
            </li>

            <li
              v-for="page in totalPages"
              :key="page"
              class="page-item"
              :class="{ active: currentPage == page }"
            >
              <button class="page-link" @click="currentPage = page">
                {{ page }}
              </button>
            </li>

            <li class="page-item" :class="{ disabled: currentPage == totalPages }">
              <button class="page-link" @click="currentPage++">
                Next
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- add/edit modal -->
    <div class="modal fade" id="trekModal" tabindex="-1" ref="trekModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              {{ isEditing ? 'Edit Trek' : 'Add New Trek' }}
            </h5>

            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <form @submit.prevent="saveTrek">
            <div class="modal-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Trek Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="form.name"
                    placeholder="Everest Base Camp"
                    required
                  >
                </div>

                <div class="col-md-6">
                  <label class="form-label">Location</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="form.location"
                    placeholder="Nepal"
                    required
                  >
                </div>

                <div class="col-md-4">
                  <label class="form-label">Difficulty</label>
                  <select class="form-select" v-model="form.difficulty" required>
                    <option value="Easy">Easy</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>

                <div class="col-md-4">
                  <label class="form-label">Duration Days</label>
                  <input
                    type="number"
                    class="form-control"
                    v-model.number="form.duration_days"
                    min="1"
                    required
                  >
                </div>

                <div class="col-md-4">
                  <label class="form-label">Total Slots</label>
                  <input
                    type="number"
                    class="form-control"
                    v-model.number="form.total_slots"
                    min="1"
                    required
                  >
                </div>

                <div class="col-md-6">
                  <label class="form-label">Start Date</label>
                  <input
                    type="date"
                    class="form-control"
                    v-model="form.start_date"
                    required
                  >
                </div>

                <div class="col-md-6">
                  <label class="form-label">End Date</label>
                  <input
                    type="date"
                    class="form-control"
                    v-model="form.end_date"
                    required
                  >
                </div>

                <div class="col-md-6">
                  <label class="form-label">Assigned Staff</label>
                  <select class="form-select" v-model="form.assigned_staff_id">
                    <option :value="null">Select Staff</option>

                    <option
                      v-for="staff in staffList"
                      :key="staff.id"
                      :value="staff.id"
                    >
                      {{ staff.full_name }} (Exp: {{ staff.experience || 'N/A' }})
                    </option>
                  </select>
                </div>

                <div class="col-md-6">
                  <label class="form-label">Status</label>
                  <select class="form-select" v-model="form.status" required>
                    <option value="Open">Open</option>
                    <option value="Closed">Closed</option>
                    <option value="Pending">Pending</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>

                <div class="col-md-12">
                  <label class="form-label">Description</label>
                  <textarea
                    class="form-control"
                    rows="3"
                    v-model="form.description"
                    placeholder="Enter trek details"
                  ></textarea>
                </div>

                <div class="col-md-12">
                  <label class="form-label">Image URL</label>
                  <input
                    type="url"
                    class="form-control"
                    v-model="form.image_url"
                    placeholder="https://example.com/image.jpg"
                  >
                  <small class="text-muted">
                    Leave blank if no image is available.
                  </small>
                </div>
              </div>
            </div>

            <div class="modal-footer bg-light">
              <button
                type="button"
                class="btn btn-outline-secondary"
                data-bs-dismiss="modal"
              >
                Cancel
              </button>

              <button type="submit" class="btn btn-primary">
                {{ isEditing ? 'Update Trek' : 'Create Trek' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      treks: [],
      filteredTreks: [],
      staffList: [],

      searchQuery: '',
      difficultyFilter: 'All',

      currentPage: 1,
      itemsPerPage: 5,
      totalPages: 1,

      isEditing: false,
      editingTrekId: null,
      bsModal: null,

      form: {
        name: '',
        location: '',
        difficulty: 'Easy',
        duration_days: 5,
        total_slots: 20,
        start_date: '',
        end_date: '',
        assigned_staff_id: null,
        status: 'Open',
        description: '',
        image_url: ''
      },

      loading: true,
      successMessage: '',
      errorMessage: ''
    }
  },

  computed: {
    paginatedTreks() {
      let start = (this.currentPage - 1) * this.itemsPerPage
      let end = start + this.itemsPerPage

      return this.filteredTreks.slice(start, end)
    }
  },

  methods: {
    async fetchTreks() {
      this.loading = true

      try {
        let response = await window.apiFetch('/api/admin/treks')
        let data = await response.json()

        if (response.ok) {
          this.treks = data
          this.filterTreks()
        }
      } catch (error) {
        this.errorMessage = 'Failed to load treks.'
      }

      this.loading = false
    },

    async fetchStaff() {
      try {
        let response = await window.apiFetch('/api/admin/staff')
        let data = await response.json()

        if (response.ok) {
          this.staffList = data.filter((staff) => {
            return staff.status == 'active'
          })
        }
      } catch (error) {
        console.log(error)
      }
    },

    filterTreks() {
      let result = this.treks

      if (this.difficultyFilter != 'All') {
        result = result.filter((trek) => {
          return trek.difficulty == this.difficultyFilter
        })
      }

      if (this.searchQuery.trim() != '') {
        let searchText = this.searchQuery.toLowerCase()

        result = result.filter((trek) => {
          return (
            trek.name.toLowerCase().includes(searchText) ||
            trek.location.toLowerCase().includes(searchText)
          )
        })
      }

      this.filteredTreks = result
      this.currentPage = 1
      this.totalPages = Math.ceil(this.filteredTreks.length / this.itemsPerPage)
    },

    handleSearch() {
      this.filterTreks()
    },

    openCreateModal() {
      this.isEditing = false
      this.editingTrekId = null

      this.form = {
        name: '',
        location: '',
        difficulty: 'Easy',
        duration_days: 5,
        total_slots: 20,
        start_date: '',
        end_date: '',
        assigned_staff_id: null,
        status: 'Open',
        description: '',
        image_url: ''
      }

      this.bsModal.show()
    },

    openEditModal(trek) {
      this.isEditing = true
      this.editingTrekId = trek.id

      this.form = {
        name: trek.name,
        location: trek.location,
        difficulty: trek.difficulty,
        duration_days: trek.duration_days,
        total_slots: trek.total_slots,
        start_date: trek.start_date,
        end_date: trek.end_date,
        assigned_staff_id: trek.assigned_staff_id,
        status: trek.status,
        description: trek.description || '',
        image_url: trek.image_url || ''
      }

      this.bsModal.show()
    },

    async saveTrek() {
      this.errorMessage = ''
      this.successMessage = ''

      let method = 'POST'
      let endpoint = '/api/admin/treks'

      if (this.isEditing == true) {
        method = 'PUT'
        endpoint = '/api/admin/treks/' + this.editingTrekId
      }

      try {
        let response = await window.apiFetch(endpoint, {
          method: method,
          body: this.form
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.fetchTreks()
          this.bsModal.hide()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to save trek details.'
      }
    },

    async confirmDelete(trek) {
      let check = confirm('Are you sure you want to delete this trek?')

      if (check == true) {
        try {
          let response = await window.apiFetch('/api/admin/treks/' + trek.id, {
            method: 'DELETE'
          })

          let data = await response.json()

          if (response.ok) {
            this.successMessage = 'Trek deleted successfully.'
            this.fetchTreks()
          } else {
            this.errorMessage = data.message
          }
        } catch (error) {
          this.errorMessage = 'Failed to delete trek.'
        }
      }
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

  mounted() {
    let modalBox = this.$refs.trekModal
    this.bsModal = new bootstrap.Modal(modalBox)

    this.fetchTreks()
    this.fetchStaff()
  }
}
</script>