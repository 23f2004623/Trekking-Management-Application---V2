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
            color: #d7d7df;
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
            color: white;
            background-color: #0d6efd;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Trekking History
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
      <!-- page heading -->
      <div
        style="
          background-color: white;
          padding: 18px 22px;
          border-radius: 8px;
          margin-bottom: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        <h2
          style="
            margin: 0 0 5px 0;
            font-size: 24px;
            color: #222;
          "
        >
          My Trekking History
        </h2>

        <p
          style="
            margin: 0;
            color: #777;
            font-size: 13px;
          "
        >
          Completed and cancelled trekking bookings.
        </p>
      </div>

      <!-- history card -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          box-sizing: border-box;
        "
      >
        <!-- loading -->
        <div
          v-if="loading"
          style="
            text-align: center;
            padding: 55px 20px;
            color: #0d6efd;
            font-size: 15px;
          "
        >
          Loading trekking history...
        </div>

        <!-- no history -->
        <div
          v-else-if="historyList.length == 0"
          style="
            background-color: #f8f9fa;
            color: #777;
            border-radius: 6px;
            padding: 50px 20px;
            text-align: center;
            font-size: 14px;
          "
        >
          <div
            style="
              font-size: 40px;
              color: #aaa;
              margin-bottom: 12px;
            "
          >
            ↺
          </div>

          No completed or cancelled treks found.
        </div>

        <!-- table -->
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
              min-width: 850px;
              border-collapse: collapse;
            "
          >
            <thead>
              <tr style="background-color: #f5f6f8;">
                <th :style="headingStyle">Trek Name</th>
                <th :style="headingStyle">Location</th>
                <th :style="headingStyle">Trek Dates</th>
                <th :style="headingStyle">Booking Date</th>
                <th :style="centerHeadingStyle">Status</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="booking in historyList"
                :key="booking.id"
                style="border-bottom: 1px solid #e8ebee;"
              >
                <td :style="cellStyle">
                  <b style="color: #222;">
                    {{ booking.trek_name }}
                  </b>
                </td>

                <td :style="cellStyle">
                  {{ booking.trek_location }}
                </td>

                <td :style="cellStyle">
                  <div>
                    {{ booking.trek_start_date }}
                  </div>

                  <small style="color: #777;">
                    to {{ booking.trek_end_date }}
                  </small>
                </td>

                <td :style="cellStyle">
                  {{ booking.booking_date }}
                </td>

                <td
                  style="
                    padding: 13px;
                    text-align: center;
                    font-size: 14px;
                    vertical-align: middle;
                  "
                >
                  <span :style="getStatusStyle(booking.status)">
                    {{ booking.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- info box -->
        <div
          style="
            margin-top: 20px;
            background-color: #cff4fc;
            color: #055160;
            border: 1px solid #b6effb;
            padding: 12px;
            border-radius: 5px;
            font-size: 13px;
            line-height: 1.5;
          "
        >
          <b>Info:</b> This page shows all completed and cancelled bookings.
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
      loading: true,

      headingStyle: {
        padding: '13px',
        textAlign: 'left',
        color: '#555',
        fontSize: '13px',
        borderBottom: '1px solid #dee2e6',
        whiteSpace: 'nowrap'
      },

      centerHeadingStyle: {
        padding: '13px',
        textAlign: 'center',
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

    getStatusStyle(status) {
      let backgroundColor = '#6c757d'

      if (status == 'Completed') {
        backgroundColor = '#0d6efd'
      } else if (status == 'Cancelled') {
        backgroundColor = '#dc3545'
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
    this.fetchHistory()
  }
}
</script>