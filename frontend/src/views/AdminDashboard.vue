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
        background-color: #1a1a2e;
        min-height: 65px;
        padding: 0 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        box-sizing: border-box;
      "
    >
      <!-- website name -->
      <router-link
        to="/admin"
        style="
          color: white;
          font-size: 21px;
          font-weight: bold;
          text-decoration: none;
          padding: 18px 0;
        "
      >
        <span style="color: #ffc107; margin-right: 7px;">▲</span>
        Trek Journey
      </router-link>

      <!-- navigation links -->
      <div
        style="
          display: flex;
          align-items: center;
          flex-wrap: wrap;
          gap: 5px;
        "
      >
        <router-link
          to="/admin"
          style="
            color: white;
            background-color: #0d6efd;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Dashboard
        </router-link>

        <router-link
          to="/admin/manage_treks"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Treks
        </router-link>

        <router-link
          to="/admin/manage_staff"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Trekking Staff
        </router-link>

        <router-link
          to="/admin/manage_users"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Users
        </router-link>

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
            margin-left: 8px;
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
      <!-- dashboard heading -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 18px 22px;
          margin-bottom: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 12px;
        "
      >
        <h2
          style="
            margin: 0;
            color: #222;
            font-size: 24px;
          "
        >
          Dashboard Overview
        </h2>

        <div
          style="
            display: flex;
            align-items: center;
            gap: 10px;
          "
        >
          <span
            style="
              background-color: #0d6efd;
              color: white;
              padding: 7px 13px;
              border-radius: 20px;
              font-size: 12px;
              font-weight: bold;
            "
          >
            Admin Panel
          </span>

          <span
            style="
              color: #777;
              font-size: 14px;
            "
          >
            Welcome, Admin
          </span>
        </div>
      </div>

      <!-- statistic cards -->
      <div
        style="
          display: flex;
          flex-wrap: wrap;
          gap: 18px;
          margin-bottom: 25px;
        "
      >
        <!-- total treks -->
        <div
          style="
            flex: 1;
            min-width: 210px;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
          "
        >
          <div>
            <p
              style="
                color: #777;
                font-size: 13px;
                margin: 0 0 8px 0;
              "
            >
              TOTAL TREKS
            </p>

            <h2
              style="
                margin: 0;
                color: #222;
                font-size: 30px;
              "
            >
              {{ stats.total_treks }}
            </h2>
          </div>

          <div
            style="
              width: 52px;
              height: 52px;
              background-color: #dbeafe;
              color: #0d6efd;
              border-radius: 50%;
              display: flex;
              justify-content: center;
              align-items: center;
              font-size: 25px;
            "
          >
            ▲
          </div>
        </div>

        <!-- total users -->
        <div
          style="
            flex: 1;
            min-width: 210px;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
          "
        >
          <div>
            <p
              style="
                color: #777;
                font-size: 13px;
                margin: 0 0 8px 0;
              "
            >
              TOTAL USERS
            </p>

            <h2
              style="
                margin: 0;
                color: #222;
                font-size: 30px;
              "
            >
              {{ stats.total_users }}
            </h2>
          </div>

          <div
            style="
              width: 52px;
              height: 52px;
              background-color: #d1e7dd;
              color: #198754;
              border-radius: 50%;
              display: flex;
              justify-content: center;
              align-items: center;
              font-size: 25px;
            "
          >
            👥
          </div>
        </div>

        <!-- total staff -->
        <div
          style="
            flex: 1;
            min-width: 210px;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
          "
        >
          <div>
            <p
              style="
                color: #777;
                font-size: 13px;
                margin: 0 0 8px 0;
              "
            >
              TOTAL STAFF
            </p>

            <h2
              style="
                margin: 0;
                color: #222;
                font-size: 30px;
              "
            >
              {{ stats.total_staff }}
            </h2>
          </div>

          <div
            style="
              width: 52px;
              height: 52px;
              background-color: #fff3cd;
              color: #b78103;
              border-radius: 50%;
              display: flex;
              justify-content: center;
              align-items: center;
              font-size: 25px;
            "
          >
            🥾
          </div>
        </div>

        <!-- total bookings -->
        <div
          style="
            flex: 1;
            min-width: 210px;
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
          "
        >
          <div>
            <p
              style="
                color: #777;
                font-size: 13px;
                margin: 0 0 8px 0;
              "
            >
              TOTAL BOOKINGS
            </p>

            <h2
              style="
                margin: 0;
                color: #222;
                font-size: 30px;
              "
            >
              {{ stats.total_bookings }}
            </h2>
          </div>

          <div
            style="
              width: 52px;
              height: 52px;
              background-color: #cff4fc;
              color: #087990;
              border-radius: 50%;
              display: flex;
              justify-content: center;
              align-items: center;
              font-size: 25px;
            "
          >
            ✓
          </div>
        </div>
      </div>

      <!-- booking table card -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          box-sizing: border-box;
        "
      >
        <!-- table heading -->
        <div
          style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 20px;
          "
        >
          <h3
            style="
              margin: 0;
              color: #222;
              font-size: 19px;
            "
          >
            Recent Booking Log
          </h3>

          <button
            type="button"
            @click="toggleViewMode"
            style="
              background-color: white;
              color: #0d6efd;
              border: 1px solid #0d6efd;
              padding: 8px 14px;
              border-radius: 5px;
              font-size: 13px;
              cursor: pointer;
            "
          >
            {{ showAllBookings ? 'Show Recent' : 'View All Bookings' }}
          </button>
        </div>

        <!-- loading -->
        <div
          v-if="loading"
          style="
            text-align: center;
            padding: 50px 20px;
            color: #0d6efd;
            font-size: 15px;
          "
        >
          Loading booking data...
        </div>

        <!-- no bookings -->
        <div
          v-else-if="filteredBookings.length == 0"
          style="
            background-color: #f8f9fa;
            color: #777;
            border-radius: 6px;
            padding: 30px;
            text-align: center;
            font-size: 14px;
          "
        >
          No bookings exist in the system yet.
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
              border-collapse: collapse;
              min-width: 800px;
            "
          >
            <thead>
              <tr style="background-color: #f5f6f8;">
                <th :style="headingStyle">Booking ID</th>
                <th :style="headingStyle">User</th>
                <th :style="headingStyle">Trek Name</th>
                <th :style="headingStyle">Booking Date</th>
                <th :style="headingStyle">Status</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="booking in filteredBookings"
                :key="booking.id"
                style="border-bottom: 1px solid #e9ecef;"
              >
                <td :style="cellStyle">
                  <b>#B{{ String(booking.id).padStart(4, '0') }}</b>
                </td>

                <td :style="cellStyle">
                  <b style="color: #222;">
                    {{ booking.user_name }}
                  </b>

                  <br>

                  <small style="color: #777;">
                    {{ booking.user_email }}
                  </small>
                </td>

                <td :style="cellStyle">
                  <b style="color: #222;">
                    {{ booking.trek_name }}
                  </b>

                  <br>

                  <small style="color: #777;">
                    {{ booking.trek_location }}
                    |
                    Starts: {{ booking.trek_start_date }}
                  </small>
                </td>

                <td :style="cellStyle">
                  {{ booking.booking_date }}
                </td>

                <td
                  :style="{
                    padding: '13px',
                    textAlign: 'center',
                    fontSize: '14px'
                  }"
                >
                  <span :style="getStatusStyle(booking.status)">
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
      loading: true,

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
      }
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
        padding: '6px 11px',
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
    this.fetchDashboardStats()
  }
}
</script>