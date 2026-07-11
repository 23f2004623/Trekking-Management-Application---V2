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
        to="/admin"
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
          gap: 5px;
        "
      >
        <router-link
          to="/admin"
          style="
            color: #d7d7df;
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
            color: white;
            background-color: #0d6efd;
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
      <!-- heading -->
      <div
        style="
          background-color: white;
          padding: 18px 22px;
          border-radius: 8px;
          margin-bottom: 20px;
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
          Manage Trekking Staff
        </h2>

        <p
          style="
            margin: 0;
            color: #777;
            font-size: 13px;
          "
        >
          Create and manage trekking staff members.
        </p>
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

      <!-- page columns -->
      <div
        style="
          display: flex;
          gap: 22px;
          align-items: flex-start;
          flex-wrap: wrap;
        "
      >
        <!-- create staff form -->
        <div
          style="
            flex: 1;
            min-width: 330px;
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
              font-size: 19px;
              color: #222;
              border-bottom: 1px solid #e6e8eb;
              padding-bottom: 12px;
            "
          >
            Create New Staff
          </h3>

          <form @submit.prevent="createStaff">
            <div style="margin-bottom: 15px;">
              <label :style="labelStyle">Full Name</label>

              <input
                v-model="form.full_name"
                type="text"
                placeholder="Vikram Singh"
                required
                :style="inputStyle"
              >
            </div>

            <div style="margin-bottom: 15px;">
              <label :style="labelStyle">Email Address</label>

              <input
                v-model="form.email"
                type="email"
                placeholder="staff@tma.com"
                required
                :style="inputStyle"
              >
            </div>

            <div style="margin-bottom: 15px;">
              <label :style="labelStyle">Contact Number</label>

              <input
                v-model="form.contact_number"
                type="text"
                placeholder="9876543210"
                required
                :style="inputStyle"
              >
            </div>

            <!-- password fields -->
            <div
              style="
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
                margin-bottom: 15px;
              "
            >
              <div style="flex: 1; min-width: 150px;">
                <label :style="labelStyle">Password</label>

                <input
                  v-model="form.password"
                  type="password"
                  placeholder="Password"
                  required
                  :style="inputStyle"
                >
              </div>

              <div style="flex: 1; min-width: 150px;">
                <label :style="labelStyle">Confirm Password</label>

                <input
                  v-model="form.confirm_password"
                  type="password"
                  placeholder="Confirm"
                  required
                  :style="inputStyle"
                >
              </div>
            </div>

            <div style="margin-bottom: 15px;">
              <label :style="labelStyle">Experience</label>

              <input
                v-model="form.experience"
                type="text"
                placeholder="5 Years"
                :style="inputStyle"
              >
            </div>

            <div style="margin-bottom: 15px;">
              <label :style="labelStyle">Specialization</label>

              <input
                v-model="form.specialization"
                type="text"
                placeholder="High Altitude Rescue"
                :style="inputStyle"
              >
            </div>

            <div style="margin-bottom: 20px;">
              <label :style="labelStyle">Status</label>

              <select
                v-model="form.status"
                :style="inputStyle"
              >
                <option value="active">Active</option>
                <option value="blacklisted">Blacklisted</option>
              </select>
            </div>

            <div
              style="
                display: flex;
                justify-content: flex-end;
                gap: 10px;
              "
            >
              <button
                type="button"
                @click="resetForm"
                style="
                  background-color: white;
                  color: #555;
                  border: 1px solid #777;
                  padding: 9px 15px;
                  border-radius: 5px;
                  cursor: pointer;
                "
              >
                Cancel
              </button>

              <button
                type="submit"
                :disabled="creating"
                :style="{
                  backgroundColor: creating ? '#7baaf7' : '#0d6efd',
                  color: 'white',
                  border: 'none',
                  padding: '9px 17px',
                  borderRadius: '5px',
                  cursor: creating ? 'not-allowed' : 'pointer',
                  fontWeight: 'bold'
                }"
              >
                {{ creating ? 'Creating...' : 'Create Staff' }}
              </button>
            </div>
          </form>

          <div
            style="
              margin-top: 22px;
              background-color: #fff3cd;
              color: #664d03;
              border: 1px solid #ffecb5;
              padding: 12px;
              border-radius: 5px;
              font-size: 13px;
              line-height: 1.5;
            "
          >
            Staff will receive login details after successful creation.
          </div>
        </div>

        <!-- staff list -->
        <div
          style="
            flex: 1.6;
            min-width: 450px;
            background-color: white;
            border-radius: 8px;
            padding: 22px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            box-sizing: border-box;
          "
        >
          <h3
            style="
              margin: 0 0 18px 0;
              font-size: 19px;
              color: #222;
            "
          >
            Staff List
          </h3>

          <!-- search -->
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search staff members"
            @input="fetchStaffList"
            style="
              width: 100%;
              height: 42px;
              padding: 0 12px;
              border: 1px solid #ced4da;
              border-radius: 5px;
              font-size: 14px;
              color: #222;
              background-color: #fafafa;
              outline: none;
              box-sizing: border-box;
              margin-bottom: 20px;
            "
          >

          <!-- loading -->
          <div
            v-if="loading"
            style="
              text-align: center;
              padding: 50px;
              color: #0d6efd;
              font-size: 15px;
            "
          >
            Loading staff list...
          </div>

          <!-- empty -->
          <div
            v-else-if="staffList.length == 0"
            style="
              text-align: center;
              padding: 50px;
              color: #777;
              font-size: 14px;
            "
          >
            No staff members found.
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
                min-width: 800px;
                border-collapse: collapse;
              "
            >
              <thead>
                <tr style="background-color: #f5f6f8;">
                  <th :style="headingStyle">ID</th>
                  <th :style="headingStyle">Staff Name</th>
                  <th :style="headingStyle">Specialization</th>
                  <th :style="headingStyle">Status</th>
                  <th :style="headingStyle">Action</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="(staff, index) in staffList"
                  :key="staff.id"
                  style="border-bottom: 1px solid #e8ebee;"
                >
                  <td :style="cellStyle">
                    <b>
                      #ST{{ String(index + 1).padStart(3, '0') }}
                    </b>
                  </td>

                  <td :style="cellStyle">
                    <b style="color: #222;">
                      {{ staff.full_name }}
                    </b>

                    <br>

                    <small style="color: #777;">
                      {{ staff.email }} | {{ staff.contact_number }}
                    </small>
                  </td>

                  <td :style="cellStyle">
                    {{ staff.specialization || 'N/A' }}

                    <br>

                    <small style="color: #777;">
                      Exp: {{ staff.experience || 'N/A' }}
                    </small>
                  </td>

                  <td :style="cellStyle">
                    <span :style="getStatusStyle(staff.status)">
                      {{ staff.status }}
                    </span>
                  </td>

                  <td
                    style="
                      padding: 13px;
                      text-align: center;
                      white-space: nowrap;
                    "
                  >
                    <button
                      v-if="staff.status == 'active'"
                      type="button"
                      @click="toggleStatus(staff, 'blacklisted')"
                      style="
                        background-color: #dc3545;
                        color: white;
                        border: none;
                        padding: 7px 10px;
                        border-radius: 4px;
                        margin-right: 5px;
                        cursor: pointer;
                      "
                    >
                      Blacklist
                    </button>

                    <button
                      v-else
                      type="button"
                      @click="toggleStatus(staff, 'active')"
                      style="
                        background-color: #198754;
                        color: white;
                        border: none;
                        padding: 7px 10px;
                        border-radius: 4px;
                        margin-right: 5px;
                        cursor: pointer;
                      "
                    >
                      Whitelist
                    </button>

                    <button
                      type="button"
                      @click="deleteStaff(staff.id)"
                      style="
                        background-color: white;
                        color: #dc3545;
                        border: 1px solid #dc3545;
                        padding: 7px 10px;
                        border-radius: 4px;
                        cursor: pointer;
                      "
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

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
            <b>Info:</b> Blacklisted staff cannot login into the system.
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
        height: '41px',
        padding: '0 11px',
        border: '1px solid #ced4da',
        borderRadius: '5px',
        fontSize: '14px',
        color: '#222',
        backgroundColor: 'white',
        boxSizing: 'border-box',
        outline: 'none'
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
      }
    }
  },

  methods: {
    async fetchStaffList() {
      this.loading = true

      try {
        let endpoint = '/api/admin/staff'

        if (this.searchQuery.trim() != '') {
          endpoint =
            '/api/admin/search?type=staff&q=' +
            encodeURIComponent(this.searchQuery)
        }

        let response = await window.apiFetch(endpoint)
        let data = await response.json()

        if (response.ok) {
          this.staffList = data
        } else {
          this.errorMessage = data.message || 'Failed to load staff list.'
        }
      } catch (error) {
        this.errorMessage = 'Failed to load staff list.'
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
        let response = await window.apiFetch(
          '/api/admin/staff/' + staff.id + '/status',
          {
            method: 'PUT',
            body: {
              status: newStatus
            }
          }
        )

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
        let response = await window.apiFetch(
          '/api/admin/staff/' + staffId,
          {
            method: 'DELETE'
          }
        )

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

    getStatusStyle(status) {
      let backgroundColor = '#dc3545'

      if (status == 'active') {
        backgroundColor = '#198754'
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