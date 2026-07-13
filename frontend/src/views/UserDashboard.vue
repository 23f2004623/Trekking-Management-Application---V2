<template>
  <div
    style="
      min-height: 100vh;
      background-color: #f2f4f7;
      font-family: Arial, Helvetica, sans-serif;
      color: #222;
    "
  >
    <!-- navbar -->
    <nav
      style="
        min-height: 65px;
        background-color: #1a1a2e;
        padding: 0 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        box-sizing: border-box;
      "
    >
      <router-link
        to="/user"
        style="
          color: white;
          text-decoration: none;
          font-size: 21px;
          font-weight: bold;
          padding: 18px 0;
        "
      >
        <span style="color: #ffc107; margin-right: 7px;">▲</span>
        Trek Journey
      </router-link>

      <div
        style="
          display: flex;
          align-items: center;
          flex-wrap: wrap;
          gap: 6px;
        "
      >
        <router-link
          to="/user"
          style="
            color: white;
            background-color: #0d6efd;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Home
        </router-link>

        <router-link
          to="/user/treks"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Browse Treks
        </router-link>

        <router-link
          to="/user/trek_history"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Trekking History
        </router-link>

        <span
          style="
            color: #d7d7df;
            font-size: 14px;
            margin-left: 10px;
          "
        >
          Welcome, {{ trekkerName }}
        </span>

        <button
          type="button"
          @click="handleLogout"
          style="
            background-color: transparent;
            color: #ff6b75;
            border: 1px solid #dc3545;
            padding: 8px 13px;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            margin-left: 5px;
          "
        >
          Logout
        </button>
      </div>
    </nav>

    <!-- main content -->
    <div
      style="
        width: 100%;
        max-width: 1450px;
        margin: auto;
        padding: 25px;
        box-sizing: border-box;
      "
    >
      <!-- page heading -->
      <div
        style="
          background-color: white;
          padding: 18px 22px;
          border-radius: 8px;
          margin-bottom: 20px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 12px;
        "
      >
        <div>
          <h2
            style="
              margin: 0 0 5px 0;
              font-size: 24px;
              color: #222;
            "
          >
            Welcome, {{ trekkerName }}!
          </h2>

          <p
            style="
              margin: 0;
              color: #777;
              font-size: 13px;
            "
          >
            Explore treks and manage your bookings.
          </p>
        </div>

        <div
          style="
            display: flex;
            gap: 9px;
            flex-wrap: wrap;
          "
        >
          <button
            type="button"
            @click="openProfileModal"
            style="
              background-color: white;
              color: #555;
              border: 1px solid #777;
              padding: 9px 14px;
              border-radius: 5px;
              font-size: 13px;
              cursor: pointer;
            "
          >
            Edit Profile
          </button>

          <button
            type="button"
            :disabled="exporting"
            @click="triggerCSVExport"
            :style="{
              backgroundColor: exporting ? '#7baaf7' : '#0d6efd',
              color: 'white',
              border: 'none',
              padding: '9px 14px',
              borderRadius: '5px',
              fontSize: '13px',
              cursor: exporting ? 'not-allowed' : 'pointer'
            }"
          >
            {{ exporting ? 'Exporting...' : 'Export History' }}
          </button>
        </div>
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
          margin-bottom: 18px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 14px;
        "
      >
        <span>{{ successMessage }}</span>

        <button
          type="button"
          @click="successMessage = ''"
          style="
            border: none;
            background: none;
            color: #0f5132;
            font-size: 18px;
            cursor: pointer;
          "
        >
          ×
        </button>
      </div>

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
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 14px;
        "
      >
        <span>{{ errorMessage }}</span>

        <button
          type="button"
          @click="errorMessage = ''"
          style="
            border: none;
            background: none;
            color: #842029;
            font-size: 18px;
            cursor: pointer;
          "
        >
          ×
        </button>
      </div>

      <!-- export pending message -->
      <div
        v-if="exportStatus == 'pending'"
        style="
          background-color: #fff3cd;
          color: #664d03;
          border: 1px solid #ffecb5;
          padding: 12px;
          border-radius: 5px;
          margin-bottom: 18px;
          font-size: 14px;
        "
      >
        Generating CSV report. Please wait...
      </div>

      <!-- export download -->
      <div
        v-if="exportDownloadUrl"
        style="
          background-color: #d1e7dd;
          color: #0f5132;
          border: 1px solid #badbcc;
          padding: 12px;
          border-radius: 5px;
          margin-bottom: 18px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 10px;
          font-size: 14px;
        "
      >
        <span>
          Your booking history file is ready.
        </span>

        <a
          :href="exportDownloadUrl"
          download
          style="
            background-color: #198754;
            color: white;
            text-decoration: none;
            padding: 8px 13px;
            border-radius: 5px;
            font-size: 13px;
          "
        >
          Download CSV
        </a>
      </div>

      <!-- featured trek heading -->
      <div
        style="
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 10px;
          margin-bottom: 15px;
        "
      >
        <h3
          style="
            margin: 0;
            color: #222;
            font-size: 20px;
          "
        >
          Featured Treks
        </h3>

        <router-link
          to="/user/browse"
          style="
            color: #0d6efd;
            text-decoration: none;
            font-size: 14px;
          "
        >
          View All Treks →
        </router-link>
      </div>

      <!-- loading featured treks -->
      <div
        v-if="loadingTreks"
        style="
          background-color: white;
          border-radius: 8px;
          padding: 50px;
          margin-bottom: 25px;
          text-align: center;
          color: #0d6efd;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        Loading treks...
      </div>

      <!-- no treks -->
      <div
        v-else-if="featuredTreks.length == 0"
        style="
          background-color: white;
          border-radius: 8px;
          padding: 35px;
          margin-bottom: 25px;
          text-align: center;
          color: #777;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          font-size: 14px;
        "
      >
        No treks are available for booking.
      </div>

      <!-- trek cards -->
      <div
        v-else
        style="
          display: flex;
          gap: 18px;
          flex-wrap: wrap;
          margin-bottom: 28px;
        "
      >
        <div
          v-for="trek in featuredTreks.slice(0, 3)"
          :key="trek.id"
          style="
            flex: 1;
            min-width: 280px;
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            display: flex;
            flex-direction: column;
          "
        >

          <div
            style="
              padding: 17px;
              display: flex;
              flex-direction: column;
              justify-content: space-between;
              flex: 1;
            "
          >
            <div>
              <div
                style="
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  gap: 10px;
                  margin-bottom: 10px;
                "
              >
                <span :style="getDifficultyStyle(trek.difficulty)">
                  {{ trek.difficulty }}
                </span>

                <span
                  style="
                    color: #777;
                    font-size: 12px;
                  "
                >
                  {{ trek.duration_days }} Days
                </span>
              </div>

              <h3
                style="
                  margin: 0 0 7px 0;
                  color: #222;
                  font-size: 18px;
                "
              >
                {{ trek.name }}
              </h3>

              <p
                style="
                  margin: 0 0 10px 0;
                  color: #dc3545;
                  font-size: 13px;
                "
              >
                {{ trek.location }}
              </p>

              <p
                style="
                  margin: 0 0 15px 0;
                  color: #777;
                  font-size: 13px;
                  line-height: 1.5;
                  max-height: 58px;
                  overflow: hidden;
                "
              >
                {{ trek.description || 'No description available.' }}
              </p>
            </div>

            <div
              style="
                border-top: 1px solid #e6e8eb;
                padding-top: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
              "
            >
              <span
                style="
                  color: #555;
                  font-size: 13px;
                "
              >
                <b>{{ trek.available_slots }}</b> slots left
              </span>

              <button
                v-if="trek.is_booked"
                type="button"
                disabled
                style="
                  background-color: #198754;
                  color: white;
                  border: none;
                  padding: 8px 13px;
                  border-radius: 5px;
                  cursor: not-allowed;
                  font-size: 13px;
                "
              >
                Booked
              </button>

              <button
                v-else-if="trek.can_book"
                type="button"
                @click="bookTrek(trek.id)"
                style="
                  background-color: #0d6efd;
                  color: white;
                  border: none;
                  padding: 8px 13px;
                  border-radius: 5px;
                  cursor: pointer;
                  font-size: 13px;
                "
              >
                Book Now
              </button>

              <button
                v-else-if="trek.available_slots <= 0"
                type="button"
                disabled
                style="
                  background-color: #6c757d;
                  color: white;
                  border: none;
                  padding: 8px 13px;
                  border-radius: 5px;
                  cursor: not-allowed;
                  font-size: 13px;
                "
              >
                Fully Booked
              </button>

              <button
                v-else
                type="button"
                disabled
                style="
                  background-color: #6c757d;
                  color: white;
                  border: none;
                  padding: 8px 13px;
                  border-radius: 5px;
                  cursor: not-allowed;
                  font-size: 13px;
                "
              >
                Not Open
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- bookings section -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          box-sizing: border-box;
        "
      >
        <h3
          style="
            margin: 0 0 20px 0;
            font-size: 20px;
            color: #222;
            border-bottom: 1px solid #e6e8eb;
            padding-bottom: 12px;
          "
        >
          My Bookings
        </h3>

        <!-- loading bookings -->
        <div
          v-if="loadingBookings"
          style="
            text-align: center;
            padding: 45px;
            color: #0d6efd;
            font-size: 14px;
          "
        >
          Loading bookings...
        </div>

        <!-- no bookings -->
        <div
          v-else-if="bookings.length == 0"
          style="
            text-align: center;
            padding: 40px;
            color: #777;
            font-size: 14px;
          "
        >
          <p style="margin-bottom: 15px;">
            You have not made any bookings.
          </p>

          <router-link
            to="/user/treks"
            style="
              display: inline-block;
              background-color: #0d6efd;
              color: white;
              padding: 8px 14px;
              border-radius: 5px;
              text-decoration: none;
              font-size: 13px;
            "
          >
            Browse Treks
          </router-link>
        </div>

        <!-- bookings table -->
        <div
          v-else
          style="
            width: 100%;
            overflow-x: auto;
          "
        >
          <table
            style="
              width: 100%;
              min-width: 950px;
              border-collapse: collapse;
            "
          >
            <thead>
              <tr style="background-color: #f5f6f8;">
                <th :style="headingStyle">Trek Name</th>
                <th :style="headingStyle">Booking Date</th>
                <th :style="headingStyle">Trek Dates</th>
                <th :style="headingStyle">Location</th>
                <th :style="headingStyle">Trek Status</th>
                <th :style="headingStyle">Status</th>
                <th :style="headingStyle">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="booking in bookings"
                :key="booking.id"
                style="border-bottom: 1px solid #e8ebee;"
              >
                <td :style="cellStyle">
                  <b style="color: #222;">
                    {{ booking.trek_name }}
                  </b>
                </td>

                <td :style="cellStyle">
                  {{ booking.booking_date }}
                </td>

                <td :style="cellStyle">
                  {{ booking.trek_start_date }}
                  to
                  {{ booking.trek_end_date }}
                </td>

                <td :style="cellStyle">
                  {{ booking.trek_location }}
                </td>

                <td :style="cellStyle">
                  <span :style="getTrekStatusStyle(booking.trek_status)">
                    {{ booking.trek_status }}
                  </span>
                </td>

                <td :style="cellStyle">
                  <span :style="getStatusStyle(booking.status)">
                    {{ booking.status }}
                  </span>
                </td>

                <td
                  style="
                    padding: 13px;
                    text-align: center;
                  "
                >
                  <button
                    v-if="booking.status == 'Booked'"
                    type="button"
                    @click="cancelBooking(booking.id)"
                    style="
                      background-color: #dc3545;
                      color: white;
                      border: none;
                      padding: 7px 11px;
                      border-radius: 5px;
                      cursor: pointer;
                      font-size: 13px;
                    "
                  >
                    Cancel
                  </button>

                  <span
                    v-else
                    style="
                      color: #888;
                      font-size: 12px;
                    "
                  >
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
      v-if="showProfileModal"
      style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.55);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        padding: 20px;
        box-sizing: border-box;
      "
      @click.self="closeProfileModal"
    >
      <div
        style="
          width: 100%;
          max-width: 500px;
          background-color: white;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        "
      >
        <!-- modal header -->
        <div
          style="
            background-color: #0d6efd;
            color: white;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          "
        >
          <h3
            style="
              margin: 0;
              color: white;
              font-size: 19px;
            "
          >
            Edit Profile
          </h3>

          <button
            type="button"
            @click="closeProfileModal"
            style="
              background: none;
              color: white;
              border: none;
              font-size: 23px;
              cursor: pointer;
            "
          >
            ×
          </button>
        </div>

        <form @submit.prevent="updateProfile">
          <div style="padding: 22px;">
            <div style="margin-bottom: 16px;">
              <label :style="labelStyle">
                Full Name
              </label>

              <input
                v-model="profileForm.full_name"
                type="text"
                required
                :style="inputStyle"
              >
            </div>

            <div style="margin-bottom: 16px;">
              <label :style="labelStyle">
                Email
              </label>

              <input
                v-model="profileForm.email"
                type="email"
                required
                :style="inputStyle"
              >
            </div>

            <div style="margin-bottom: 5px;">
              <label :style="labelStyle">
                Contact Number
              </label>

              <input
                v-model="profileForm.contact_number"
                type="text"
                required
                :style="inputStyle"
              >
            </div>
          </div>

          <!-- modal buttons -->
          <div
            style="
              background-color: #f6f7f8;
              padding: 15px 22px;
              display: flex;
              justify-content: flex-end;
              gap: 10px;
            "
          >
            <button
              type="button"
              @click="closeProfileModal"
              style="
                background-color: white;
                color: #555;
                border: 1px solid #777;
                padding: 9px 15px;
                border-radius: 5px;
                cursor: pointer;
              "
            >
              Close
            </button>

            <button
              type="submit"
              :disabled="updatingProfile"
              :style="{
                backgroundColor: updatingProfile ? '#7baaf7' : '#0d6efd',
                color: 'white',
                border: 'none',
                padding: '9px 16px',
                borderRadius: '5px',
                cursor: updatingProfile ? 'not-allowed' : 'pointer'
              }"
            >
              {{ updatingProfile ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
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
      showProfileModal: false,

      profileForm: {
        full_name: '',
        email: '',
        contact_number: ''
      },

      headingStyle: {
        padding: '13px',
        textAlign: 'left',
        color: '#555',
        fontSize: '13px',
        borderBottom: '1px solid #dee2e6',
        whiteSpace: 'nowrap'
      },

      cellStyle: {
        padding: '13px',
        color: '#333',
        fontSize: '14px',
        verticalAlign: 'middle'
      },

      labelStyle: {
        display: 'block',
        color: '#333',
        fontSize: '14px',
        fontWeight: 'bold',
        marginBottom: '6px'
      },

      inputStyle: {
        width: '100%',
        height: '42px',
        padding: '0 11px',
        border: '1px solid #ced4da',
        borderRadius: '5px',
        fontSize: '14px',
        color: '#222',
        backgroundColor: 'white',
        boxSizing: 'border-box',
        outline: 'none'
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
        } else {
          this.errorMessage = data.message || 'Failed to load treks.'
        }
      } catch (error) {
        this.errorMessage = 'Failed to load treks.'
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
        } else {
          this.errorMessage = data.message || 'Failed to load bookings.'
        }
      } catch (error) {
        this.errorMessage = 'Failed to load bookings.'
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

          if (this.pollInterval) {
            clearInterval(this.pollInterval)
          }

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

    openProfileModal() {
      this.showProfileModal = true
    },

    closeProfileModal() {
      this.showProfileModal = false
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

          this.closeProfileModal()
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

    getDifficultyStyle(diff) {
      let backgroundColor = '#6c757d'
      let color = 'white'

      if (diff == 'Easy') {
        backgroundColor = '#198754'
      } else if (diff == 'Moderate') {
        backgroundColor = '#ffc107'
        color = '#222'
      } else if (diff == 'Hard') {
        backgroundColor = '#dc3545'
      }

      return {
        display: 'inline-block',
        backgroundColor: backgroundColor,
        color: color,
        padding: '6px 10px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: 'bold'
      }
    },

    getStatusStyle(status) {
      let backgroundColor = '#6c757d'

      if (status == 'Booked') {
        backgroundColor = '#198754'
      } else if (status == 'Cancelled') {
        backgroundColor = '#dc3545'
      } else if (status == 'Completed') {
        backgroundColor = '#0d6efd'
      }

      return {
        display: 'inline-block',
        backgroundColor: backgroundColor,
        color: 'white',
        padding: '6px 10px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: 'bold'
      }
    },

    getTrekStatusStyle(status) {
      let backgroundColor = '#6c757d'
      let color = 'white'

      if (status == 'Approved') {
        backgroundColor = '#20c997'
      } else if (status == 'Open') {
        backgroundColor = '#198754'
      } else if (status == 'Closed') {
        backgroundColor = '#dc3545'
      } else if (status == 'Pending') {
        backgroundColor = '#ffc107'
        color = '#222'
      } else if (status == 'Completed') {
        backgroundColor = '#0d6efd'
      } else if (status == 'Ongoing') {
        backgroundColor = '#6610f2'
      }

      return {
        display: 'inline-block',
        backgroundColor: backgroundColor,
        color: color,
        padding: '6px 10px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: 'bold'
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