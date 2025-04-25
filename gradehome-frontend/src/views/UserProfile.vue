<template>
  <div class="profile-page" :class="{ 'dark-mode': darkMode }">
    <!-- Dashboard NavBar at the top - reuse the existing component -->
    <DashboardNavBar
        :userName="userProfile.firstName || 'User'"
        :userEmail="userProfile.email || 'user@example.com'"
        :userAvatar="userProfile.avatar"
        :isMobile="isMobile"
        @logout="handleLogout"
    />

    <div class="dashboard-layout">
      <!-- Main Content Area -->
      <div class="dashboard-main-content expanded">
        <div class="dashboard-header">
          <h1>My Profile</h1>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading your profile...</p>
        </div>

        <!-- Not Logged In State -->
        <div v-else-if="notLoggedIn" class="center-content auth-prompt">
          <div class="auth-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <h2>Welcome to GradeGuard</h2>
            <p>Please sign in to access your profile.</p>
            <a href="/login" class="login-button">Go to Login</a>
          </div>
        </div>

        <!-- Profile Content when logged in -->
        <div v-else class="profile-content">
          <!-- Avatar and Basic Info Card -->
          <div class="profile-card avatar-card">
            <div class="avatar-section">
              <div class="avatar-container">
                <img v-if="userProfile.avatar" :src="userProfile.avatar" alt="Profile avatar" class="profile-avatar" />
                <div v-else class="avatar-placeholder">
                  {{ getInitials(userProfile.firstName, userProfile.lastName) }}
                </div>
                <button @click="triggerFileInput" class="avatar-upload-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                </button>
                <input
                    type="file"
                    ref="fileInput"
                    style="display: none"
                    accept="image/*"
                    @change="handleFileChange"
                />
              </div>
              <div class="avatar-info">
                <h2>{{ userProfile.firstName }} {{ userProfile.lastName }}</h2>
                <p class="user-email">{{ userProfile.email }}</p>
                <p class="user-details">
                  {{ userProfile.university || 'University not set' }} | {{ userProfile.degree || 'Degree not set' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Personal Information Card -->
          <div class="profile-card">
            <div class="card-header">
              <h2>Personal Information</h2>
              <button @click="toggleEditMode" class="edit-button" v-if="!editMode">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
                Edit Profile
              </button>
            </div>

            <!-- View mode -->
            <div v-if="!editMode" class="profile-details">
              <div class="detail-row">
                <div class="detail-item">
                  <label>First Name</label>
                  <p>{{ userProfile.firstName || 'Not provided' }}</p>
                </div>
                <div class="detail-item">
                  <label>Last Name</label>
                  <p>{{ userProfile.lastName || 'Not provided' }}</p>
                </div>
              </div>

              <div class="detail-row">
                <div class="detail-item">
                  <label>Email Address</label>
                  <p>{{ userProfile.email }}</p>
                </div>
                <div class="detail-item">
                  <label>Phone Number</label>
                  <p>{{ userProfile.phone || 'Not provided' }}</p>
                </div>
              </div>

              <div class="detail-row">
                <div class="detail-item">
                  <label>Date of Birth</label>
                  <p>{{ formatDate(userProfile.dateOfBirth) || 'Not provided' }}</p>
                </div>
                <div class="detail-item">
                  <label>University</label>
                  <p>{{ userProfile.university || 'Not provided' }}</p>
                </div>
              </div>

              <div class="detail-row">
                <div class="detail-item full-width">
                  <label>Bio</label>
                  <p class="bio-text">{{ userProfile.bio || 'No bio provided' }}</p>
                </div>
              </div>
            </div>

            <!-- Edit mode -->
            <div v-else class="profile-form">
              <div class="form-row">
                <div class="form-group">
                  <label for="firstName">First Name</label>
                  <input
                      type="text"
                      id="firstName"
                      v-model="editedProfile.firstName"
                      placeholder="Enter your first name"
                  />
                </div>
                <div class="form-group">
                  <label for="lastName">Last Name</label>
                  <input
                      type="text"
                      id="lastName"
                      v-model="editedProfile.lastName"
                      placeholder="Enter your last name"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="email">Email Address</label>
                  <input
                      type="email"
                      id="email"
                      v-model="userProfile.email"
                      disabled
                  />
                  <small>Email cannot be changed</small>
                </div>
                <div class="form-group">
                  <label for="phone">Phone Number</label>
                  <input
                      type="tel"
                      id="phone"
                      v-model="editedProfile.phone"
                      placeholder="Enter your phone number"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="dob">Date of Birth</label>
                  <input
                      type="date"
                      id="dob"
                      v-model="editedProfile.dateOfBirth"
                  />
                </div>
                <div class="form-group">
                  <label>University</label>
                  <input
                      type="text"
                      disabled
                      :value="userProfile.university"
                  />
                  <small>Set in account settings</small>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group full-width">
                  <label for="bio">Bio</label>
                  <textarea
                      id="bio"
                      v-model="editedProfile.bio"
                      rows="4"
                      placeholder="Tell us about yourself"
                  ></textarea>
                </div>
              </div>

              <div class="form-actions">
                <button @click="cancelEdit" class="cancel-button">
                  Cancel
                </button>
                <button @click="saveProfile" class="save-button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                    <polyline points="17 21 17 13 7 13 7 21"></polyline>
                    <polyline points="7 3 7 8 15 8"></polyline>
                  </svg>
                  Save Changes
                </button>
              </div>
            </div>
          </div>

          <!-- Account Security Card -->
          <div class="profile-card">
            <div class="card-header">
              <h2>Account Security</h2>
            </div>
            <div class="security-section">
              <div class="security-item">
                <div class="security-info">
                  <h3>Password</h3>
                  <p>Last changed: {{ passwordLastChanged || 'Never' }}</p>
                </div>
                <button @click="showChangePasswordModal = true" class="change-password-btn">
                  Change Password
                </button>
              </div>
            </div>
          </div>

          <!-- GradeRadar Settings Card (NEW) -->
          <div class="profile-card">
            <div class="card-header">
              <h2>GradeRadar Settings</h2>
              <button @click="toggleGradeRadarEditMode" class="edit-button" v-if="!gradeRadarEditMode">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
                Edit Settings
              </button>
            </div>

            <!-- View mode -->
            <div v-if="!gradeRadarEditMode" class="profile-details">
              <div class="detail-row">
                <div class="detail-item">
                  <label>University</label>
                  <p>{{ gradeRadarProfile.university || 'Not set' }}</p>
                </div>
                <div class="detail-item">
                  <label>Degree Program</label>
                  <p>{{ gradeRadarProfile.degree || 'Not set' }}</p>
                </div>
              </div>

              <div class="detail-row">
                <div class="detail-item full-width">
                  <p class="info-text">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="16" x2="12" y2="12"></line>
                      <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                    These settings are used for GradeRadar community features. Your university and degree help categorize modules you add or review.
                  </p>
                </div>
              </div>
            </div>

            <!-- Edit mode -->
            <div v-else class="profile-form">
              <div class="form-row">
                <div class="form-group">
                  <label for="grUniversity">University</label>
                  <select 
                    id="grUniversity" 
                    v-model="editedGradeRadarProfile.university"
                    @change="onUniversityChange"
                  >
                    <option value="">Select University</option>
                    <option v-for="uni in universities" :key="uni.id" :value="uni.name">
                      {{ uni.name }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="grDegree">Degree Program</label>
                  <select 
                    id="grDegree" 
                    v-model="editedGradeRadarProfile.degree"
                    :disabled="!editedGradeRadarProfile.university"
                  >
                    <option value="">Select Degree Program</option>
                    <option v-for="deg in degreesForSelectedUniversity" :key="deg.id" :value="deg.name">
                      {{ deg.name }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group full-width">
                  <p class="info-text">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="16" x2="12" y2="12"></line>
                      <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                    Can't find your university or degree? You can add them when writing your first module review.
                  </p>
                </div>
              </div>

              <div class="form-actions">
                <button @click="cancelGradeRadarEdit" class="cancel-button">
                  Cancel
                </button>
                <button @click="saveGradeRadarProfile" class="save-button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                    <polyline points="17 21 17 13 7 13 7 21"></polyline>
                    <polyline points="7 3 7 8 15 8"></polyline>
                  </svg>
                  Save Settings
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <div v-if="showChangePasswordModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h2>Change Password</h2>
          <button @click="showChangePasswordModal = false" class="close-modal-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="currentPassword">Current Password</label>
            <input
                type="password"
                id="currentPassword"
                v-model="passwordForm.current_password"
                placeholder="Enter your current password"
            />
          </div>
          <div class="form-group">
            <label for="newPassword">New Password</label>
            <input
                type="password"
                id="newPassword"
                v-model="passwordForm.new_password"
                placeholder="Enter your new password"
            />
            <small>Password must contain at least 8 characters, one uppercase letter, one number, and one special character.</small>
          </div>
          <div class="form-group">
            <label for="confirmPassword">Confirm New Password</label>
            <input
                type="password"
                id="confirmPassword"
                v-model="passwordForm.confirm_password"
                placeholder="Confirm your new password"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showChangePasswordModal = false" class="cancel-button">
            Cancel
          </button>
          <button @click="changePassword" class="save-button" :disabled="changePasswordLoading">
            <span v-if="changePasswordLoading">Saving...</span>
            <span v-else>Change Password</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "UserProfile",
  components: { DashboardNavBar },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      loading: true,
      isMobile: false,
      editMode: false,
      userProfile: {
        firstName: "",
        lastName: "",
        email: "",
        avatar: "",
        dateOfBirth: "",
        phone: "",
        bio: "",
        university: "",
        degree: ""
      },
      editedProfile: {
        firstName: "",
        lastName: "",
        dateOfBirth: "",
        phone: "",
        bio: ""
      },
      showChangePasswordModal: false,
      passwordForm: {
        current_password: "",
        new_password: "",
        confirm_password: ""
      },
      changePasswordLoading: false,
      passwordLastChanged: null,
      avatarUploading: false,

      gradeRadarEditMode: false,
      gradeRadarProfile: {
        university: "",
        degree: ""
      },
      editedGradeRadarProfile: {
        university: "",
        degree: ""
      },
      universities: [],
      degreesForSelectedUniversity: [],
      loadingUniversities: false,
      loadingDegrees: false
    };
  },
  async mounted() {
    // Check mobile
    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);

    // Handle dark mode
    this.darkMode = getDarkModePreference();
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Fetch user profile
    await this.fetchUserProfile();
    await this.fetchGradeRadarProfile();
    await this.fetchUniversities();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },
    handleLogout() {
      this.notLoggedIn = true;
    },
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },
    async fetchUserProfile() {
      try {
        this.loading = true;
        const response = await axios.get(`${API_URL}/user/profile`, {
          withCredentials: true,
        });

        this.userProfile = response.data;
        this.initEditForm();
        this.notLoggedIn = false;
      } catch (error) {
        console.error("Error fetching user profile:", error);
        if (error.response?.status === 401) {
          this.notLoggedIn = true;
          this.$router.push("/login");
        } else {
          notify({ type: "error", message: "Failed to load profile. Please try again." });
        }
      } finally {
        this.loading = false;
      }
    },
    
    async fetchGradeRadarProfile() {
      try {
        const response = await gradeRadarService.getUserProfile();
        this.gradeRadarProfile = {
          university: response.data.university || "",
          degree: response.data.degree || ""
        };
        this.initGradeRadarEditForm();
      } catch (error) {
        console.error("Error fetching GradeRadar profile:", error);
      }
    },
    
    initGradeRadarEditForm() {
      this.editedGradeRadarProfile = {
        university: this.gradeRadarProfile.university || "",
        degree: this.gradeRadarProfile.degree || ""
      };
    },
    
    toggleGradeRadarEditMode() {
      this.gradeRadarEditMode = !this.gradeRadarEditMode;
      if (this.gradeRadarEditMode) {
        this.initGradeRadarEditForm();
      }
    },
    
    cancelGradeRadarEdit() {
      this.gradeRadarEditMode = false;
    },
    
    async saveGradeRadarProfile() {
      try {
        await gradeRadarService.updateUserProfile(this.editedGradeRadarProfile);
        this.gradeRadarProfile = { ...this.editedGradeRadarProfile };
        this.gradeRadarEditMode = false;
        notify({ type: "success", message: "GradeRadar settings updated successfully!" });
      } catch (error) {
        console.error("Error updating GradeRadar profile:", error);
        notify({ type: "error", message: "Failed to update GradeRadar settings. Please try again." });
      }
    },
    
    async fetchUniversities() {
      try {
        this.loadingUniversities = true;
        const response = await gradeRadarService.getUniversities();
        this.universities = response.data || [];
      } catch (error) {
        console.error("Error fetching universities:", error);
      } finally {
        this.loadingUniversities = false;
      }
    },

    async onUniversityChange() {
      if (!this.editedGradeRadarProfile.university) {
        this.degreesForSelectedUniversity = [];
        this.editedGradeRadarProfile.degree = "";
        return;
      }
      
      try {
        this.loadingDegrees = true;
        this.editedGradeRadarProfile.degree = ""; // Reset degree when university changes
        const response = await gradeRadarService.getUniversityDegrees(this.editedGradeRadarProfile.university);
        this.degreesForSelectedUniversity = response.data.degrees || [];
      } catch (error) {
        console.error("Error fetching degrees:", error);
        this.degreesForSelectedUniversity = [];
      } finally {
        this.loadingDegrees = false;
      }
    },

    initEditForm() {
      this.editedProfile = {
        firstName: this.userProfile.firstName || "",
        lastName: this.userProfile.lastName || "",
        dateOfBirth: this.userProfile.dateOfBirth || "",
        phone: this.userProfile.phone || "",
        bio: this.userProfile.bio || ""
      };
    },
    toggleEditMode() {
      this.editMode = !this.editMode;
      if (this.editMode) {
        this.initEditForm();
      }
    },
    cancelEdit() {
      this.editMode = false;
    },
    async saveProfile() {
      try {
        const response = await axios.put(
            `${API_URL}/user/profile`,
            this.editedProfile,
            { withCredentials: true }
        );

        this.userProfile = response.data;
        this.editMode = false;
        notify({ type: "success", message: "Profile updated successfully!" });
      } catch (error) {
        console.error("Error updating profile:", error);
        notify({ type: "error", message: "Failed to update profile. Please try again." });
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    async handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;

      // Validate file type and size
      if (!file.type.match('image.*')) {
        notify({ type: "error", message: "Please select an image file." });
        return;
      }

      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        notify({ type: "error", message: "Image size should be less than 5MB." });
        return;
      }

      try {
        this.avatarUploading = true;

        // Get upload URL from backend
        const uploadUrlResponse = await axios.post(
            `${API_URL}/user/avatar-upload`,
            { filename: file.name },
            { withCredentials: true }
        );

        const { uploadUrl, avatarUrl } = uploadUrlResponse.data;

        // Debug logging
        console.log('Upload URL:', uploadUrl);
        console.log('Avatar URL:', avatarUrl);

        // Use the returned URL to upload the file directly to blob storage
        const uploadResponse = await fetch(uploadUrl, {
          method: 'PUT',
          headers: {
            'x-ms-blob-type': 'BlockBlob',
            'Content-Type': file.type
          },
          body: file
        });

        // Check upload response
        if (!uploadResponse.ok) {
          const errorText = await uploadResponse.text();
          console.error('Upload failed:', errorText);
          throw new Error(`Upload failed: ${errorText}`);
        }

        // Update profile with new avatar URL
        const profileUpdateResponse = await axios.put(
            `${API_URL}/user/profile`,
            { avatar: avatarUrl },
            { withCredentials: true }
        );

        // Update local state
        this.userProfile.avatar = avatarUrl;
        notify({ type: "success", message: "Profile picture updated successfully!" });
      } catch (error) {
        console.error("Error uploading avatar:", error);

        // More detailed error logging
        if (error.response) {
          // The request was made and the server responded with a status code
          console.error("Server response error:", error.response.data);
          console.error("Status code:", error.response.status);
        } else if (error.request) {
          // The request was made but no response was received
          console.error("No response received:", error.request);
        } else {
          // Something happened in setting up the request
          console.error("Error setting up request:", error.message);
        }

        notify({
          type: "error",
          message: error.response?.data?.error || "Failed to update profile picture. Please try again."
        });
      } finally {
        this.avatarUploading = false;
        // Reset the file input
        this.$refs.fileInput.value = '';
      }
    },
    async changePassword() {
      // Validate passwords
      if (!this.passwordForm.current_password) {
        notify({ type: "warning", message: "Current password is required." });
        return;
      }

      if (!this.passwordForm.new_password) {
        notify({ type: "warning", message: "New password is required." });
        return;
      }

      if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        notify({ type: "warning", message: "New passwords do not match." });
        return;
      }

      // Validate password strength
      const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;
      if (!passwordRegex.test(this.passwordForm.new_password)) {
        notify({
          type: "warning",
          message: "Password must contain at least 8 characters, one uppercase letter, one number, and one special character."
        });
        return;
      }

      try {
        this.changePasswordLoading = true;
        await axios.put(
            `${API_URL}/user/password`,
            {
              current_password: this.passwordForm.current_password,
              new_password: this.passwordForm.new_password
            },
            { withCredentials: true }
        );

        notify({ type: "success", message: "Password changed successfully!" });
        this.showChangePasswordModal = false;
        this.passwordForm = {
          current_password: "",
          new_password: "",
          confirm_password: ""
        };

        // Update last changed date
        this.passwordLastChanged = new Date().toLocaleDateString();
      } catch (error) {
        console.error("Error changing password:", error);
        if (error.response?.status === 400) {
          notify({ type: "error", message: error.response.data.error || "Current password is incorrect." });
        } else {
          notify({ type: "error", message: "Failed to change password. Please try again." });
        }
      } finally {
        this.changePasswordLoading = false;
      }
    },
    getInitials(firstName, lastName) {
      let initials = '';
      if (firstName) initials += firstName.charAt(0).toUpperCase();
      if (lastName) initials += lastName.charAt(0).toUpperCase();
      return initials || 'U';
    },
    formatDate(dateString) {
      if (!dateString) return '';

      try {
        const date = new Date(dateString);
        return date.toLocaleDateString(undefined, {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
      } catch (e) {
        return dateString;
      }
    }
  }
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
}

.dashboard-layout {
  display: flex;
  flex-direction: row;
  position: relative;
  padding-top: 70px; /* Space for fixed navbar */
  min-height: calc(100vh - 70px);
}

.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all var(--transition-speed) ease;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-dark);
  margin: 0;
}

/* Loading state */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Profile content */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border-color);
}

.card-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-dark);
}

/* Avatar section */
.avatar-card {
  padding: 2rem;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.avatar-container {
  position: relative;
}

.profile-avatar, .avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: var(--shadow-sm);
}

.avatar-placeholder {
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 600;
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.avatar-upload-btn:hover {
  background-color: var(--primary-dark);
  transform: scale(1.1);
}

.avatar-info h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.user-email {
  color: var(--text-secondary);
  margin: 0 0 0.5rem;
}

.user-details {
  margin: 0;
}

/* Profile details */
.profile-details {
  padding: 2rem;
}

.detail-row {
  display: flex;
  margin-bottom: 1.5rem;
  gap: 2rem;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-item {
  flex: 1;
}

.detail-item.full-width {
  flex: 1 1 100%;
}

.detail-item label {
  display: block;
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.detail-item p {
  margin: 0;
  font-weight: 500;
}

.bio-text {
  line-height: 1.6;
  white-space: pre-line;
}

/* Edit button */
.edit-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.edit-button:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

/* Form styling */
.profile-form {
  padding: 2rem;
}

.form-row {
  display: flex;
  margin-bottom: 1.5rem;
  gap: 2rem;
}

.form-group {
  flex: 1;
}

.form-group.full-width {
  flex: 1 1 100%;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus, .form-group textarea:focus {
  border-color: var(--primary-color);
  outline: none;
}

.form-group input:disabled {
  background-color: rgba(0, 0, 0, 0.05);
  cursor: not-allowed;
}

.form-group small {
  display: block;
  margin-top: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.75rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

/* Security section */
.security-section {
  padding: 2rem;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.security-info h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 600;
}

.security-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.change-password-btn {
  padding: 0.5rem 1rem;
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.change-password-btn:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

/* Buttons */
.save-button, .cancel-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

.save-button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
  transform: none;
}

.cancel-button {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 500px;
  animation: modalAppear 0.3s ease;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-modal-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-modal-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
}

/* Auth prompt */
.auth-prompt {
  padding: 2rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 3rem 2rem;
  box-shadow: var(--shadow-md);
  text-align: center;
  max-width: 400px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.auth-card svg {
  color: var(--primary-color);
}

.auth-card h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.auth-card p {
  margin: 0;
  color: var(--text-secondary);
}

.login-button {
  display: inline-block;
  background: var(--primary-color);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 24px;
  text-decoration: none;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.login-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

/* Responsive styles */
@media (max-width: 768px) {
  .dashboard-main-content {
    padding: 1.5rem;
  }

  .avatar-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1rem;
  }

  .form-row, .detail-row {
    flex-direction: column;
    gap: 1.5rem;
  }

  .security-item {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .change-password-btn {
    align-self: flex-start;
  }
}

@media (max-width: 480px) {
  .dashboard-layout, .dashboard-main-content {
    padding: 1rem;
  }

  .profile-card {
    padding: 1rem;
  }

  .card-header {
    padding: 1rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .profile-details, .profile-form, .security-section {
    padding: 1rem;
  }

  .avatar-container, .profile-avatar, .avatar-placeholder {
    width: 100px;
    height: 100px;
  }

  .form-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .save-button, .cancel-button {
    width: 100%;
  }
}
</style>