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
            <router-link class="nav-link active" to="/user">
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
            <router-link class="nav-link" to="/user/history">
              <i class="fa-solid fa-clock-rotate-left me-1"></i>
              Trekking History
            </router-link>
          </li>
        </ul>

        <span class="text-white small me-3">
          Welcome, {{ trekkerName }}
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
          <h4 class="m-0">
            Welcome, {{ trekkerName }}!
          </h4>

          <div class="d-flex gap-2">
            <button
              class="btn btn-outline-secondary btn-sm"
              data-bs-toggle="modal"
              data-bs-target="#profileModal"
            >
              <i class="fa-solid fa-user-gear me-1"></i>
              Edit Profile
            </button>

            <button
              class="btn btn-primary btn-sm"
              :disabled="exporting"
              @click="triggerCSVExport"
            >
              <span
                v-if="exporting"
                class="spinner-border spinner-border-sm me-1"
              ></span>

              <i
                v-else
                class="fa-solid fa-file-csv me-1"
              ></i>

              Export History
            </button>
          </div>
        </div>
      </div>

      <!-- success message -->
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}

        <button
          class="btn-close float-end"
          @click="successMessage = ''"
        ></button>
      </div>

      <!-- error message -->
      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}

        <button
          class="btn-close float-end"
          @click="errorMessage = ''"
        ></button>
      </div>

      <!-- export loading -->
      <div v-if="exportStatus == 'pending'" class="alert alert-warning">
        <span class="spinner-border spinner-border-sm me-2"></span>
        Generating CSV report. Please wait.
      </div>

      <!-- download export -->
      <div
        v-if="exportDownloadUrl"
        class="alert alert-success d-flex justify-content-between align-items-center"
      >
        <span>
          Your booking history file is ready.
        </span>

        <a
          :href="exportDownloadUrl"
          download
          class="btn btn-success btn-sm"
        >
          <i class="fa-solid fa-download me-1"></i>
          Download CSV
        </a>
      </div>

      <!-- featured treks -->
      <div class="mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="mb-0">
            Featured Treks
          </h5>

          <router-link to="/user/browse">
            View All Treks
          </router-link>
        </div>

        <div v-if="loadingTreks" class="text-center p-5">
          <div class="spinner-border text-primary"></div>
        </div>

        <div
          v-else-if="featuredTreks.length == 0"
          class="alert alert-light text-center"
        >
          No treks are available for booking.
        </div>

        <div v-else class="row g-3">
          <div
            v-for="trek in featuredTreks.slice(0, 3)"
            :key="trek.id"
            class="col-md-4"
          >
            <div class="card shadow-sm h-100">
              <img
                :src="trek.image_url || 'https://picsum.photos/400/220?random=' + (trek.id + 10)"
                @error="$event.target.src = 'https://picsum.photos/400/220?random=' + (trek.id + 10)"
                class="card-img-top"
                style="height: 160px; object-fit: cover;"
              >

              <div class="card-body d-flex flex-column justify-content-between">
                <div>
                  <div class="d-flex justify-content-between mb-2">
                    <span
                      class="badge"
                      :class="getDifficultyClass(trek.difficulty)"
                    >
                      {{ trek.difficulty }}
                    </span>

                    <small class="text-muted">
                      {{ trek.duration_days }} Days
                    </small>
                  </div>

                  <h6>
                    {{ trek.name }}
                  </h6>

                  <p class="text-muted small">
                    <i class="fa-solid fa-location-dot text-danger me-1"></i>
                    {{ trek.location }}
                  </p>

                  <p class="text-muted small line-clamp">
                    {{ trek.description || 'No description available.' }}
                  </p>
                </div>

                <div class="d-flex justify-content-between align-items-center border-top pt-2">
                  <small>
                    <b>{{ trek.available_slots }}</b> slots left
                  </small>

                  <button
                    v-if="trek.available_slots > 0"
                    class="btn btn-primary btn-sm"
                    @click="bookTrek(trek.id)"
                  >
                    Book Now
                  </button>

                  <button
                    v-else
                    class="btn btn-secondary btn-sm"
                    disabled
                  >
                    Not Available
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- bookings -->
      <div class="card shadow-sm p-4">
        <h5 class="mb-3">
          <i class="fa-solid fa-ticket text-primary me-2"></i>
          My Bookings
        </h5>

        <div v-if="loadingBookings" class="text-center p-4">
          <div class="spinner-border text-primary"></div>
        </div>

        <div
          v-else-if="bookings.length == 0"
          class="text-center p-4"
        >
          <i class="fa-solid fa-receipt text-muted fa-2x mb-2"></i>

          <p class="text-muted">
            You have not made any bookings.
          </p>

          <router-link
            to="/user/browse"
            class="btn btn-primary btn-sm"
          >
            Browse Treks
          </router-link>
        </div>

        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Trek Name</th>
                <th>Booking Date</th>
                <th>Trek Dates</th>
                <th>Location</th>
                <th>Status</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="booking in bookings" :key="booking.id">
                <td>
                  {{ booking.trek_name }}
                </td>

                <td>
                  {{ booking.booking_date }}
                </td>

                <td>
                  {{ booking.trek_start_date }}
                  to
                  {{ booking.trek_end_date }}
                </td>

                <td>
                  {{ booking.trek_location }}
                </td>

                <td>
                  <span
                    class="badge"
                    :class="getStatusClass(booking.status)"
                  >
                    {{ booking.status }}
                  </span>
                </td>

                <td class="text-center">
                  <button
                    v-if="booking.status == 'Booked'"
                    class="btn btn-danger btn-sm"
                    @click="cancelBooking(booking.id)"
                  >
                    Cancel
                  </button>

                  <span v-else class="text-muted small">
                    N/A
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- profile modal -->
    <div
      class="modal fade"
      id="profileModal"
      tabindex="-1"
      ref="profileModal"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              Edit Profile
            </h5>

            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <form @submit.prevent="updateProfile">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">
                  Full Name
                </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="profileForm.full_name"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label">
                  Email
                </label>

                <input
                  type="email"
                  class="form-control"
                  v-model="profileForm.email"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label">
                  Contact Number
                </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="profileForm.contact_number"
                  required
                >
              </div>
            </div>

            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-outline-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>

              <button
                type="submit"
                class="btn btn-primary"
                :disabled="updatingProfile"
              >
                Save Changes
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
      trekkerName: '',
      featuredTreks: [],
      bookings: [],

      loadingTreks: true,
      loadingBookings: true,

      successMessage: '',
      errorMessage: '',

      exporting: false,
      exportStatus: '',
      exportDownloadUrl: '',
      exportTaskId: null,
      pollInterval: null,

      updatingProfile: false,

      profileForm: {
        full_name: '',
        email: '',
        contact_number: ''
      }
    }
  },

  methods: {
    async fetchFeaturedTreks() {
      this.loadingTreks = true

      try {
        let response = await window.apiFetch('/api/user/treks')
        let data = await response.json()

        if (response.ok) {
          this.featuredTreks = data
        }
      } catch (error) {
        console.log(error)
      }

      this.loadingTreks = false
    },

    async fetchBookings() {
      this.loadingBookings = true

      try {
        let response = await window.apiFetch('/api/user/bookings')
        let data = await response.json()

        if (response.ok) {
          this.bookings = data
        }
      } catch (error) {
        console.log(error)
      }

      this.loadingBookings = false
    },

    async bookTrek(trekId) {
      this.successMessage = ''
      this.errorMessage = ''

      try {
        let response = await window.apiFetch('/api/user/bookings', {
          method: 'POST',
          body: {
            trek_id: trekId
          }
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message

          this.fetchFeaturedTreks()
          this.fetchBookings()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to book trek.'
      }
    },

    async triggerCSVExport() {
      this.exporting = true
      this.exportStatus = 'pending'
      this.exportDownloadUrl = ''

      try {
        let response = await window.apiFetch('/api/user/export-history')
        let data = await response.json()

        if (response.ok) {
          this.exportTaskId = data.task_id

          this.pollInterval = setInterval(() => {
            this.pollExportStatus()
          }, 2000)
        } else {
          this.exportStatus = 'failed'
          this.exporting = false
          this.errorMessage = data.message
        }
      } catch (error) {
        this.exportStatus = 'failed'
        this.exporting = false
        this.errorMessage = 'Failed to start export.'
      }
    },

    async pollExportStatus() {
      if (!this.exportTaskId) {
        return
      }

      try {
        let response = await window.apiFetch(
          '/api/user/export-status/' + this.exportTaskId
        )

        let data = await response.json()

        if (response.ok) {
          if (data.status == 'ready') {
            clearInterval(this.pollInterval)

            this.exportStatus = 'success'
            this.exportDownloadUrl = data.result.download_url
            this.exporting = false
          } else if (data.status == 'failed') {
            clearInterval(this.pollInterval)

            this.exportStatus = 'failed'
            this.exporting = false
            this.errorMessage = 'CSV export failed.'
          }
        }
      } catch (error) {
        clearInterval(this.pollInterval)

        this.exportStatus = 'failed'
        this.exporting = false
        this.errorMessage = 'Failed to check export status.'
      }
    },

    async updateProfile() {
      this.updatingProfile = true
      this.successMessage = ''
      this.errorMessage = ''

      try {
        let response = await window.apiFetch('/api/user/profile', {
          method: 'PUT',
          body: this.profileForm
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.trekkerName = data.user.full_name

          localStorage.setItem(
            'user',
            JSON.stringify(data.user)
          )

          let modal = bootstrap.Modal.getInstance(
            this.$refs.profileModal
          )

          modal.hide()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to update profile.'
      }

      this.updatingProfile = false
    },

    async cancelBooking(bookingId) {
      let check = confirm(
        'Are you sure you want to cancel this booking?'
      )

      if (check == false) {
        return
      }

      this.successMessage = ''
      this.errorMessage = ''

      try {
        let response = await window.apiFetch(
          '/api/user/bookings/' + bookingId,
          {
            method: 'DELETE'
          }
        )

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message

          this.fetchBookings()
          this.fetchFeaturedTreks()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to cancel booking.'
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
    let userData = localStorage.getItem('user')

    if (userData) {
      let user = JSON.parse(userData)

      this.trekkerName = user.full_name
      this.profileForm.full_name = user.full_name
      this.profileForm.email = user.email
      this.profileForm.contact_number = user.contact_number || ''
    }

    this.fetchFeaturedTreks()
    this.fetchBookings()
  },

  beforeUnmount() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval)
    }
  }
}
</script>

<style scoped>
.line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>