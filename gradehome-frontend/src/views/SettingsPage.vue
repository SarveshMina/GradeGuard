<template>
  <div class="settings-page" :class="{ 'dark-mode': darkMode }">
    <!-- Dashboard NavBar at the top -->
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
          <h1>Settings</h1>
          <p class="settings-subtitle">Customize your GradeGuard experience</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading settings...</p>
        </div>

        <!-- Not Logged In State -->
        <div v-else-if="notLoggedIn" class="center-content auth-prompt">
          <div class="auth-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <h2>Welcome to GradeGuard</h2>
            <p>Please sign in to access your settings.</p>
            <a href="/login" class="login-button" aria-label="Go to login page">Go to Login</a>
          </div>
        </div>

        <!-- Settings Content -->
        <div v-else class="settings-content">
          <!-- Mobile Settings Dropdown (shown only on mobile) -->
          <div class="mobile-settings-dropdown" v-if="isMobile">
            <div class="dropdown-selector" @click="toggleMobileNav" aria-haspopup="true" :aria-expanded="mobileNavOpen">
              <span>{{ getCurrentSectionName() }}</span>
              <svg class="dropdown-icon" :class="{ 'open': mobileNavOpen }" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
            <div class="mobile-nav-menu" v-if="mobileNavOpen" role="menu">
              <button
                  v-for="(section, index) in sections"
                  :key="index"
                  @click="selectMobileSection(section.id)"
                  class="mobile-nav-item"
                  :class="{ active: activeSection === section.id }"
                  role="menuitem"
                  :aria-current="activeSection === section.id"
              >
                <span class="icon" v-html="section.icon"></span>
                <span class="text">{{ section.name }}</span>
              </button>
            </div>
          </div>

          <!-- Desktop Settings Navigation (hidden on mobile) -->
          <div class="settings-navigation" v-if="!isMobile" role="navigation" aria-label="Settings sections">
            <button
                v-for="(section, index) in sections"
                :key="index"
                @click="activeSection = section.id"
                class="nav-button"
                :class="{ active: activeSection === section.id }"
                role="tab"
                :aria-selected="activeSection === section.id"
                :aria-controls="`${section.id}-panel`"
            >
              <span class="icon" v-html="section.icon"></span>
              <span class="text">{{ section.name }}</span>
            </button>
          </div>

          <!-- Settings Panels -->
          <div class="settings-panel" role="tabpanel" :aria-labelledby="activeSection">
            <!-- Appearance Settings -->
            <div v-if="activeSection === 'appearance'" id="appearance-panel" class="settings-section">
              <h2>Appearance Settings</h2>

              <!-- Theme Selection -->
              <div class="setting-group">
                <h3>Theme</h3>
                <div class="theme-selector">
                  <button
                      @click="setTheme('light')"
                      class="theme-option"
                      :class="{ active: !darkMode }"
                      aria-pressed="!darkMode"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="5"></circle>
                      <line x1="12" y1="1" x2="12" y2="3"></line>
                      <line x1="12" y1="21" x2="12" y2="23"></line>
                      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                      <line x1="1" y1="12" x2="3" y2="12"></line>
                      <line x1="21" y1="12" x2="23" y2="12"></line>
                      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                    </svg>
                    <span>Light</span>
                  </button>
                  <button
                      @click="setTheme('dark')"
                      class="theme-option"
                      :class="{ active: darkMode }"
                      aria-pressed="darkMode"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                    </svg>
                    <span>Dark</span>
                  </button>
                </div>
              </div>

              <!-- Accent Color -->
              <div class="setting-group">
                <h3>Accent Color</h3>
                <div class="color-options">
                  <button
                      v-for="color in accentColors"
                      :key="color.id"
                      @click="setAccentColor(color.id)"
                      class="color-option"
                      :class="{ active: settings.appearance.accentColor === color.id }"
                      :style="{ backgroundColor: color.value }"
                      :aria-label="`${color.id} color`"
                      :aria-pressed="settings.appearance.accentColor === color.id"
                  ></button>
                </div>
              </div>

              <!-- Font Size -->
              <div class="setting-group">
                <h3>Font Size</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.appearance.fontSize"
                        value="small"
                        @change="applyFontSize(settings.appearance.fontSize)"
                    />
                    <span>Small</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.appearance.fontSize"
                        value="medium"
                        @change="applyFontSize(settings.appearance.fontSize)"
                    />
                    <span>Medium</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.appearance.fontSize"
                        value="large"
                        @change="applyFontSize(settings.appearance.fontSize)"
                    />
                    <span>Large</span>
                  </label>
                </div>
              </div>

              <!-- High Contrast Mode -->
              <div class="setting-group">
                <h3>High Contrast Mode</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.appearance.highContrast"
                        @change="toggleHighContrast"
                        aria-label="Enable high contrast mode"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable high contrast for better visibility</span>
                </div>
              </div>

              <!-- NEW: UI Animation Control -->
              <div class="setting-group">
                <h3>Interface Animations</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.appearance.enableAnimations"
                        @change="toggleAnimations"
                        aria-label="Enable interface animations"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable interface animations and transitions</span>
                </div>
              </div>
            </div>

            <!-- Academic Settings -->
            <div v-if="activeSection === 'academic'" id="academic-panel" class="settings-section">
              <h2>Academic Settings</h2>

              <!-- NEW: Academic Level and Enrollment Type Section -->
              <div class="setting-group">
                <h3>Academic Profile</h3>
                <div class="academic-profile-section">
                  <!-- Academic Level -->
                  <div class="profile-item">
                    <h4>Academic Level</h4>
                    <div class="select-group">
                      <button class="select-btn"
                              :class="{ active: settings.academic.academicLevel === 'Undergraduate' }"
                              @click="settings.academic.academicLevel = 'Undergraduate'"
                              aria-pressed="settings.academic.academicLevel === 'Undergraduate'"
                      >
                        <span class="btn-icon">🎓</span>
                        <span class="btn-text">Undergraduate</span>
                      </button>
                      <button class="select-btn"
                              :class="{ active: settings.academic.academicLevel === 'Postgraduate (Masters)' }"
                              @click="settings.academic.academicLevel = 'Postgraduate (Masters)'"
                              aria-pressed="settings.academic.academicLevel === 'Postgraduate (Masters)'"
                      >
                        <span class="btn-icon">🧑‍🎓</span>
                        <span class="btn-text">Masters</span>
                      </button>
                      <button class="select-btn"
                              :class="{ active: settings.academic.academicLevel === 'Postgraduate (PhD)' }"
                              @click="settings.academic.academicLevel = 'Postgraduate (PhD)'"
                              aria-pressed="settings.academic.academicLevel === 'Postgraduate (PhD)'"
                      >
                        <span class="btn-icon">👨‍🎓</span>
                        <span class="btn-text">PhD</span>
                      </button>
                    </div>
                  </div>

                  <!-- Enrollment Type -->
                  <div class="profile-item">
                    <h4>Enrollment Type</h4>
                    <div class="select-group">
                      <button class="select-btn"
                              :class="{ active: settings.academic.enrollmentType === 'Full time' }"
                              @click="settings.academic.enrollmentType = 'Full time'"
                              aria-pressed="settings.academic.enrollmentType === 'Full time'"
                      >
                        <span class="btn-icon">✅</span>
                        <span class="btn-text">Full time</span>
                      </button>
                      <button class="select-btn"
                              :class="{ active: settings.academic.enrollmentType === 'Part time' }"
                              @click="settings.academic.enrollmentType = 'Part time'"
                              aria-pressed="settings.academic.enrollmentType === 'Part time'"
                      >
                        <span class="btn-icon">⏳</span>
                        <span class="btn-text">Part time</span>
                      </button>
                    </div>
                  </div>

                  <!-- Study Preferences (MULTIPLE SELECTION ALLOWED) -->
                  <div class="profile-item">
                    <h4>Study Preferences</h4>
                    <div class="select-group">
                      <button class="select-btn"
                              :class="{ active: settings.academic.studyPreferences.includes('Mornings') }"
                              @click="toggleStudyPreference('Mornings')"
                              aria-pressed="settings.academic.studyPreferences.includes('Mornings')"
                      >
                        <span class="btn-icon">🌅</span>
                        <span class="btn-text">Mornings</span>
                      </button>
                      <button class="select-btn"
                              :class="{ active: settings.academic.studyPreferences.includes('Afternoons') }"
                              @click="toggleStudyPreference('Afternoons')"
                              aria-pressed="settings.academic.studyPreferences.includes('Afternoons')"
                      >
                        <span class="btn-icon">☀️</span>
                        <span class="btn-text">Afternoons</span>
                      </button>
                      <button class="select-btn"
                              :class="{ active: settings.academic.studyPreferences.includes('Evenings') }"
                              @click="toggleStudyPreference('Evenings')"
                              aria-pressed="settings.academic.studyPreferences.includes('Evenings')"
                      >
                        <span class="btn-icon">🌆</span>
                        <span class="btn-text">Evenings</span>
                      </button>
                      <button class="select-btn"
                              :class="{ active: settings.academic.studyPreferences.includes('Late Night') }"
                              @click="toggleStudyPreference('Late Night')"
                              aria-pressed="settings.academic.studyPreferences.includes('Late Night')"
                      >
                        <span class="btn-icon">🌙</span>
                        <span class="btn-text">Late Night</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- NEW: Degree Configuration Section -->
              <div class="setting-group">
                <h3>Degree Configuration</h3>
                <div class="degree-config-section">
                  <!-- Current Year -->
                  <div class="form-row">
                    <div class="form-group">
                      <label for="currentYear">Current Year</label>
                      <select id="currentYear" v-model="settings.academic.currentYear">
                        <option v-for="n in 7" :key="`year-${n}`" :value="n">Year {{ n }}</option>
                      </select>
                    </div>

                    <!-- Total Years in Program -->
                    <div class="form-group">
                      <label for="totalYears">Years in Program</label>
                      <select id="totalYears" v-model="settings.academic.totalYears" @change="updateYearWeightsBasedOnTotalYears">
                        <option v-for="n in 7" :key="`total-${n}`" :value="n">{{ n }} {{ n === 1 ? 'Year' : 'Years' }}</option>
                      </select>
                    </div>
                  </div>

                  <div class="form-row">
                    <!-- Semesters per Year -->
                    <div class="form-group">
                      <label for="semestersPerYear">Semesters per Year</label>
                      <select id="semestersPerYear" v-model="settings.academic.semestersPerYear">
                        <option value="1">1 Semester</option>
                        <option value="2">2 Semesters</option>
                        <option value="3">3 Semesters</option>
                        <option value="4">4 Semesters</option>
                      </select>
                    </div>

                    <!-- Credits per Year -->
                    <div class="form-group">
                      <label for="creditsPerYear">Credits per Year</label>
                      <select id="creditsPerYear" v-model="settings.academic.creditsPerYear">
                        <option value="30">30 Credits</option>
                        <option value="60">60 Credits</option>
                        <option value="90">90 Credits</option>
                        <option value="120">120 Credits</option>
                        <option value="180">180 Credits</option>
                        <option value="custom">Custom</option>
                      </select>
                      <input
                          v-if="settings.academic.creditsPerYear === 'custom'"
                          type="number"
                          v-model.number="settings.academic.customCreditsPerYear"
                          class="custom-value-input"
                          placeholder="Enter credits"
                      />
                    </div>
                  </div>

                  <!-- Target Grade -->
                  <div class="form-group target-grade-section">
                    <label>Target Grade</label>
                    <div class="select-group">
                      <button class="select-btn target-grade-btn"
                              :class="{ active: settings.academic.targetGrade === 70 }"
                              @click="settings.academic.targetGrade = 70; settings.academic.customTargetGrade = null"
                              aria-pressed="settings.academic.targetGrade === 70"
                      >
                        <span class="btn-text">First Class (70%+)</span>
                      </button>
                      <button class="select-btn target-grade-btn"
                              :class="{ active: settings.academic.targetGrade === 60 }"
                              @click="settings.academic.targetGrade = 60; settings.academic.customTargetGrade = null"
                              aria-pressed="settings.academic.targetGrade === 60"
                      >
                        <span class="btn-text">2:1 (60-69%)</span>
                      </button>
                      <button class="select-btn target-grade-btn"
                              :class="{ active: settings.academic.targetGrade === 50 }"
                              @click="settings.academic.targetGrade = 50; settings.academic.customTargetGrade = null"
                              aria-pressed="settings.academic.targetGrade === 50"
                      >
                        <span class="btn-text">2:2 (50-59%)</span>
                      </button>
                      <button class="select-btn target-grade-btn"
                              :class="{ active: settings.academic.targetGrade === 40 }"
                              @click="settings.academic.targetGrade = 40; settings.academic.customTargetGrade = null"
                              aria-pressed="settings.academic.targetGrade === 40"
                      >
                        <span class="btn-text">Third (40-49%)</span>
                      </button>
                      <button class="select-btn target-grade-btn"
                              :class="{ active: settings.academic.targetGrade === 'custom' }"
                              @click="settings.academic.targetGrade = 'custom'"
                              aria-pressed="settings.academic.targetGrade === 'custom'"
                      >
                        <span class="btn-text">Custom</span>
                      </button>
                    </div>
                    <input
                        v-if="settings.academic.targetGrade === 'custom'"
                        type="number"
                        v-model.number="settings.academic.customTargetGrade"
                        class="custom-value-input"
                        placeholder="Enter target percentage"
                        min="0"
                        max="100"
                    />
                  </div>
                </div>
              </div>

              <!-- Year Weights Configuration -->
              <div class="setting-group">
                <h3>Year Weightings</h3>
                <p class="setting-description">Specify how much each year contributes to your final grade.</p>
                <div class="year-weights-container">
                  <div class="year-weights-header">
                    <div class="year-column">Year</div>
                    <div class="weight-column">Weight (%)</div>
                    <div class="active-column">Active</div>
                  </div>

                  <div v-for="(year, index) in settings.academic.yearWeights" :key="index" class="year-weight-row">
                    <div class="year-column">Year {{ index + 1 }}</div>
                    <div class="weight-column">
                      <input
                          type="number"
                          v-model.number="year.weight"
                          min="0"
                          max="100"
                          @input="validateYearWeights"
                          :disabled="!year.active"
                      />
                    </div>
                    <div class="active-column">
                      <label class="toggle-container">
                        <input type="checkbox" v-model="year.active" @change="validateYearWeights">
                        <span class="toggle-switch"></span>
                      </label>
                    </div>
                  </div>

                  <div class="total-weight" :class="{ 'weight-error': totalWeight !== 100 && hasActiveYears }">
                    Total Weight: {{ totalWeight }}% {{ totalWeight !== 100 && hasActiveYears ? '(Should be 100%)' : '' }}
                  </div>
                </div>
              </div>

              <!-- Grading Scale -->
              <div class="setting-group">
                <h3>Grading Scale</h3>
                <div class="grading-scale">
                  <div class="grade-row header">
                    <div class="grade-letter">Grade</div>
                    <div class="grade-min">Minimum %</div>
                    <div class="grade-gpa">GPA Value</div>
                    <div class="grade-action"></div>
                  </div>
                  <div
                      v-for="(grade, index) in settings.academic.gradingScale"
                      :key="index"
                      class="grade-row"
                  >
                    <div class="grade-letter">
                      <input
                          type="text"
                          v-model="grade.letter"
                          maxlength="2"
                          aria-label="Grade letter"
                      />
                    </div>
                    <div class="grade-min">
                      <input
                          type="number"
                          v-model.number="grade.minPercentage"
                          min="0"
                          max="100"
                          step="0.1"
                          aria-label="Minimum percentage"
                      />
                    </div>
                    <div class="grade-gpa">
                      <input
                          type="number"
                          v-model.number="grade.gpaValue"
                          min="0"
                          max="4"
                          step="0.1"
                          aria-label="GPA value"
                      />
                    </div>
                    <div class="grade-action">
                      <button
                          v-if="index > 0"
                          @click="removeGrade(index)"
                          class="remove-grade"
                          aria-label="Remove grade"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
                <button @click="addGrade" class="add-grade-btn" aria-label="Add grade">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  Add Grade
                </button>
              </div>

              <!-- Term Dates -->
              <div class="setting-group">
                <h3>Term Dates</h3>
                <div class="term-dates">
                  <div class="form-row">
                    <div class="form-group">
                      <label for="term-start">Term Start Date</label>
                      <input
                          type="date"
                          id="term-start"
                          v-model="settings.academic.termStartDate"
                      />
                    </div>
                    <div class="form-group">
                      <label for="term-end">Term End Date</label>
                      <input
                          type="date"
                          id="term-end"
                          v-model="settings.academic.termEndDate"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <!-- Holidays and Breaks -->
              <div class="setting-group">
                <h3>Holidays and Break Periods</h3>
                <div class="holidays-list">
                  <div
                      v-for="(holiday, index) in settings.academic.holidays"
                      :key="index"
                      class="holiday-item"
                  >
                    <div class="holiday-header">
                      <input
                          type="text"
                          v-model="holiday.name"
                          placeholder="Holiday Name"
                          class="holiday-name"
                          aria-label="Holiday name"
                      />
                      <button
                          @click="removeHoliday(index)"
                          class="remove-holiday"
                          aria-label="Remove holiday"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </div>
                    <div class="holiday-dates">
                      <div class="form-group">
                        <label>Start Date</label>
                        <input
                            type="date"
                            v-model="holiday.startDate"
                            aria-label="Holiday start date"
                        />
                      </div>
                      <div class="form-group">
                        <label>End Date</label>
                        <input
                            type="date"
                            v-model="holiday.endDate"
                            aria-label="Holiday end date"
                        />
                      </div>
                    </div>
                  </div>
                  <button @click="addHoliday" class="add-holiday-btn" aria-label="Add holiday or break">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Add Holiday or Break
                  </button>
                </div>
              </div>
            </div>

            <!-- Account & Security Settings -->
            <div v-if="activeSection === 'account'" id="account-panel" class="settings-section">
              <h2>Account & Security</h2>

              <!-- Password Change -->
              <div class="setting-group">
                <h3>Change Password</h3>
                <form @submit.prevent="changePassword" class="password-form">
                  <div class="form-group">
                    <label for="current-password">Current Password</label>
                    <div class="password-input-wrapper">
                      <input
                          :type="showPassword.current ? 'text' : 'password'"
                          id="current-password"
                          v-model="passwordForm.currentPassword"
                          required
                          autocomplete="current-password"
                      />
                      <button
                          type="button"
                          class="toggle-password"
                          @click="showPassword.current = !showPassword.current"
                          aria-label="Toggle password visibility"
                      >
                        <svg v-if="!showPassword.current" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                          <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                          <line x1="1" y1="1" x2="23" y2="23"></line>
                        </svg>
                      </button>
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="new-password">New Password</label>
                    <div class="password-input-wrapper">
                      <input
                          :type="showPassword.new ? 'text' : 'password'"
                          id="new-password"
                          v-model="passwordForm.newPassword"
                          required
                          autocomplete="new-password"
                      />
                      <button
                          type="button"
                          class="toggle-password"
                          @click="showPassword.new = !showPassword.new"
                          aria-label="Toggle password visibility"
                      >
                        <svg v-if="!showPassword.new" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                          <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                          <line x1="1" y1="1" x2="23" y2="23"></line>
                        </svg>
                      </button>
                    </div>
                    <small>Password must be at least 8 characters with a mix of letters, numbers, and symbols</small>
                  </div>
                  <div class="form-group">
                    <label for="confirm-password">Confirm New Password</label>
                    <div class="password-input-wrapper">
                      <input
                          :type="showPassword.confirm ? 'text' : 'password'"
                          id="confirm-password"
                          v-model="passwordForm.confirmPassword"
                          required
                          autocomplete="new-password"
                      />
                      <button
                          type="button"
                          class="toggle-password"
                          @click="showPassword.confirm = !showPassword.confirm"
                          aria-label="Toggle password visibility"
                      >
                        <svg v-if="!showPassword.confirm" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                          <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                          <line x1="1" y1="1" x2="23" y2="23"></line>
                        </svg>
                      </button>
                    </div>
                  </div>
                  <button
                      type="submit"
                      class="save-button"
                      :disabled="passwordForm.isSubmitting"
                  >
                    <span v-if="passwordForm.isSubmitting">Updating...</span>
                    <span v-else>Update Password</span>
                  </button>
                </form>
              </div>

              <!-- NEW: Two-Factor Authentication -->
              <div class="setting-group">
                <h3>Two-Factor Authentication</h3>
                <p class="setting-description">Add an extra layer of security to your account by enabling two-factor authentication.</p>

                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.security.twoFactorEnabled"
                        @change="toggleTwoFactor"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable Two-Factor Authentication</span>
                </div>

                <div v-if="settings.security.twoFactorEnabled" class="tfa-setup-section">
                  <p>Two-factor authentication is enabled. Use your authenticator app to generate codes when signing in.</p>
                  <button @click="resetTwoFactor" class="reset-tfa-btn">Reset Two-Factor Setup</button>
                </div>

                <div v-else-if="showTfaSetup" class="tfa-setup-section">
                  <h4>Setup Instructions</h4>
                  <ol class="setup-steps">
                    <li>Install an authenticator app like Google Authenticator or Authy</li>
                    <li>Scan the QR code with your app</li>
                    <li>Enter the 6-digit code from your app below to verify</li>
                  </ol>

                  <div class="qr-code-container">
                    <!-- Sample QR code placeholder - would be generated dynamically -->
                    <div class="qr-code-placeholder">QR Code</div>
                  </div>

                  <div class="verification-code-section">
                    <label for="verification-code">Enter 6-digit code</label>
                    <input type="text" id="verification-code" v-model="tfaVerificationCode" maxlength="6" placeholder="000000" />
                    <button @click="verifyTfaCode" class="verify-code-btn">Verify & Enable</button>
                  </div>
                </div>
              </div>

              <!-- NEW: Account Preferences -->
              <div class="setting-group">
                <h3>Account Preferences</h3>

                <div class="form-group">
                  <label for="notification-email">Notification Email</label>
                  <input type="email" id="notification-email" v-model="settings.security.notificationEmail" placeholder="your@email.com" />
                </div>

                <div class="toggle-option">
                  <label class="toggle">
                    <input type="checkbox" v-model="settings.security.emailNotifications" />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Receive email notifications</span>
                </div>

                <div class="toggle-option">
                  <label class="toggle">
                    <input type="checkbox" v-model="settings.security.activityAlerts" />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Receive alerts for unusual account activity</span>
                </div>
              </div>
            </div>

            <!-- Accessibility Settings -->
            <div v-if="activeSection === 'accessibility'" id="accessibility-panel" class="settings-section">
              <h2>Accessibility Features</h2>

              <!-- NEW: Color Vision Deficiency Support -->
              <div class="setting-group">
                <h3>Color Vision Deficiency Support</h3>
                <p class="setting-description">Select a color blindness correction to optimize the interface for your needs.</p>

                <div class="select-wrapper">
                  <select
                      v-model="settings.accessibility.colorBlindMode"
                      @change="applyColorBlindMode"
                      aria-label="Color blindness mode">
                    <option value="none">No Adjustment (Default)</option>
                    <option value="protanopia">Protanopia (Red-Blind)</option>
                    <option value="deuteranopia">Deuteranopia (Green-Blind)</option>
                    <option value="tritanopia">Tritanopia (Blue-Blind)</option>
                    <option value="achromatopsia">Achromatopsia (Monochromacy)</option>
                  </select>
                </div>

                <div class="color-blind-preview">
                  <div class="preview-title">Color Preview:</div>
                  <div class="color-samples">
                    <div class="color-sample" style="background-color: #ff0000;">Red</div>
                    <div class="color-sample" style="background-color: #00ff00;">Green</div>
                    <div class="color-sample" style="background-color: #0000ff;">Blue</div>
                    <div class="color-sample" style="background-color: #ffff00;">Yellow</div>
                    <div class="color-sample" style="background-color: #ff00ff;">Magenta</div>
                  </div>
                </div>
              </div>

              <!-- Screen Reader Optimization -->
              <div class="setting-group">
                <h3>Screen Reader Support</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.screenReaderOptimized"
                        @change="applyAccessibilitySettings"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Optimize interface for screen readers</span>
                </div>

                <!-- NEW: Screen Reader Verbosity -->
                <div v-if="settings.accessibility.screenReaderOptimized" class="indented-option">
                  <label for="screen-reader-verbosity">Verbosity Level</label>
                  <select id="screen-reader-verbosity" v-model="settings.accessibility.screenReaderVerbosity" @change="applyAccessibilitySettings">
                    <option value="low">Low (Essential Information Only)</option>
                    <option value="medium">Medium (Default)</option>
                    <option value="high">High (Detailed Descriptions)</option>
                  </select>
                </div>
              </div>

              <!-- NEW: Motion & Animation Settings -->
              <div class="setting-group">
                <h3>Motion & Animation</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.reduceMotion"
                        @change="applyReduceMotion"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Reduce motion and animations</span>
                </div>

                <div class="motion-level" v-if="!settings.accessibility.reduceMotion">
                  <label for="motion-intensity">Animation Intensity</label>
                  <input
                      type="range"
                      id="motion-intensity"
                      v-model="settings.accessibility.motionIntensity"
                      min="0"
                      max="100"
                      step="25"
                      @change="applyMotionIntensity"
                  />
                  <div class="range-labels">
                    <span>Minimal</span>
                    <span>Full</span>
                  </div>
                </div>
              </div>

              <!-- Keyboard Shortcuts -->
              <div class="setting-group">
                <h3>Keyboard Shortcuts</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.keyboardShortcuts"
                        @change="applyAccessibilitySettings"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable keyboard shortcuts</span>
                </div>
                <div class="shortcuts-list" v-if="settings.accessibility.keyboardShortcuts">
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">D</span>
                    </div>
                    <div class="shortcut-desc">Go to Dashboard</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">C</span>
                    </div>
                    <div class="shortcut-desc">Go to Calendar</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">G</span>
                    </div>
                    <div class="shortcut-desc">Go to Grades</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">S</span>
                    </div>
                    <div class="shortcut-desc">Go to Settings</div>
                  </div>
                  <div class="shortcut-item">
                    <div class="shortcut-keys">
                      <span class="key">Alt</span> + <span class="key">N</span>
                    </div>
                    <div class="shortcut-desc">Create New Event</div>
                  </div>
                </div>
              </div>

              <!-- Focus Mode -->
              <div class="setting-group">
                <h3>Focus Mode</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.focusMode"
                        @change="applyAccessibilitySettings"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Reduce UI distractions for better focus</span>
                </div>
              </div>

              <!-- NEW: Text-to-Speech -->
              <div class="setting-group">
                <h3>Text-to-Speech</h3>
                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.accessibility.textToSpeech"
                        @change="toggleTextToSpeech"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable text-to-speech for selected text</span>
                </div>

                <div v-if="settings.accessibility.textToSpeech" class="tts-options">
                  <div class="form-group">
                    <label for="tts-voice">Voice</label>
                    <select id="tts-voice" v-model="settings.accessibility.ttsVoice">
                      <option value="default">Default</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="tts-rate">Speaking Rate</label>
                    <input
                        type="range"
                        id="tts-rate"
                        v-model="settings.accessibility.ttsRate"
                        min="0.5"
                        max="2"
                        step="0.1"
                    />
                    <div class="range-labels">
                      <span>Slower</span>
                      <span>Normal</span>
                      <span>Faster</span>
                    </div>
                  </div>

                  <div class="form-group">
                    <label for="tts-pitch">Pitch</label>
                    <input
                        type="range"
                        id="tts-pitch"
                        v-model="settings.accessibility.ttsPitch"
                        min="0.5"
                        max="2"
                        step="0.1"
                    />
                    <div class="range-labels">
                      <span>Lower</span>
                      <span>Normal</span>
                      <span>Higher</span>
                    </div>
                  </div>

                  <button @click="testTextToSpeech" class="test-tts-btn">Test Speech</button>
                </div>
              </div>
            </div>

            <!-- Calendar & Events Settings -->
            <div v-if="activeSection === 'calendar'" id="calendar-panel" class="settings-section">
              <h2>Calendar & Events</h2>

              <!-- First Day of Week -->
              <div class="setting-group">
                <h3>First Day of Week</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.firstDayOfWeek"
                        value="sunday"
                        @change="applyCalendarSettings"
                    />
                    <span>Sunday</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.firstDayOfWeek"
                        value="monday"
                        @change="applyCalendarSettings"
                    />
                    <span>Monday</span>
                  </label>
                </div>
              </div>

              <!-- Default Event Duration -->
              <div class="setting-group">
                <h3>Default Event Duration</h3>
                <div class="select-wrapper">
                  <select v-model="settings.calendar.defaultEventDuration" @change="applyCalendarSettings">
                    <option value="30">30 minutes</option>
                    <option value="60">1 hour</option>
                    <option value="90">1.5 hours</option>
                    <option value="120">2 hours</option>
                    <option value="180">3 hours</option>
                  </select>
                </div>
              </div>

              <!-- Default Event Type -->
              <div class="setting-group">
                <h3>Default Event Type</h3>
                <div class="select-wrapper">
                  <select v-model="settings.calendar.defaultEventType" @change="applyCalendarSettings">
                    <option value="general">General</option>
                    <option value="study">Study Session</option>
                    <option value="assignment">Assignment</option>
                    <option value="exam">Exam</option>
                    <option value="meeting">Meeting</option>
                    <option value="celebration">Celebration</option>
                  </select>
                </div>
              </div>

              <!-- Time Format -->
              <div class="setting-group">
                <h3>Time Format</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.timeFormat"
                        value="12h"
                        @change="applyCalendarSettings"
                    />
                    <span>12-hour (1:00 PM)</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.timeFormat"
                        value="24h"
                        @change="applyCalendarSettings"
                    />
                    <span>24-hour (13:00)</span>
                  </label>
                </div>
              </div>

              <!-- Date Format -->
              <div class="setting-group">
                <h3>Date Format</h3>
                <div class="radio-options">
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.dateFormat"
                        value="MM/DD/YYYY"
                        @change="applyCalendarSettings"
                    />
                    <span>MM/DD/YYYY</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.dateFormat"
                        value="DD/MM/YYYY"
                        @change="applyCalendarSettings"
                    />
                    <span>DD/MM/YYYY</span>
                  </label>
                  <label class="radio-option">
                    <input
                        type="radio"
                        v-model="settings.calendar.dateFormat"
                        value="YYYY-MM-DD"
                        @change="applyCalendarSettings"
                    />
                    <span>YYYY-MM-DD</span>
                  </label>
                </div>
              </div>

              <!-- NEW: Calendar Display Settings -->
              <div class="setting-group">
                <h3>Calendar Display</h3>

                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.calendar.showWeekNumbers"
                        @change="applyCalendarSettings"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Show week numbers</span>
                </div>

                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.calendar.showCompleted"
                        @change="applyCalendarSettings"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Show completed tasks/events</span>
                </div>

                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.calendar.highlightToday"
                        @change="applyCalendarSettings"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Highlight current day</span>
                </div>

                <div class="form-group">
                  <label for="default-calendar-view">Default Calendar View</label>
                  <select id="default-calendar-view" v-model="settings.calendar.defaultView" @change="applyCalendarSettings">
                    <option value="month">Month</option>
                    <option value="week">Week</option>
                    <option value="day">Day</option>
                    <option value="agenda">Agenda</option>
                  </select>
                </div>
              </div>

              <!-- NEW: Event Notifications -->
              <div class="setting-group">
                <h3>Event Notifications</h3>

                <div class="toggle-option">
                  <label class="toggle">
                    <input
                        type="checkbox"
                        v-model="settings.calendar.enableNotifications"
                        @change="applyCalendarSettings"
                    />
                    <span class="toggle-slider"></span>
                  </label>
                  <span>Enable event notifications</span>
                </div>

                <div v-if="settings.calendar.enableNotifications" class="form-group">
                  <label for="notification-time">Default Notification Time</label>
                  <select id="notification-time" v-model="settings.calendar.defaultNotificationTime">
                    <option value="0">At time of event</option>
                    <option value="5">5 minutes before</option>
                    <option value="15">15 minutes before</option>
                    <option value="30">30 minutes before</option>
                    <option value="60">1 hour before</option>
                    <option value="120">2 hours before</option>
                    <option value="1440">1 day before</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Save Button (Fixed at Bottom) -->
        <div v-if="!notLoggedIn && !loading" class="settings-actions">
          <button
              @click="resetSettings"
              class="reset-button"
              aria-label="Reset all settings to defaults"
          >
            Reset to Defaults
          </button>
          <button
              @click="saveSettings"
              class="save-button"
              :disabled="isSaving"
              aria-label="Save all settings"
          >
            <span v-if="isSaving">Saving...</span>
            <span v-else>Save Settings</span>
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
import { userSettingsService } from '@/services/userSettingsService.js';
import { getDarkModePreference, setDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

export default {
  name: "Settings",
  components: { DashboardNavBar },
  data() {
    return {
      darkMode: false,
      notLoggedIn: false,
      loading: true,
      isMobile: false,
      isSaving: false,
      activeSection: 'appearance',
      mobileNavOpen: false,
      showPassword: {
        current: false,
        new: false,
        confirm: false
      },

      // TFA setup
      showTfaSetup: false,
      tfaVerificationCode: '',

      // Test TTS
      testTtsText: "This is a test of the text-to-speech feature.",

      // User profile
      userProfile: {
        firstName: "",
        email: "",
        avatar: ""
      },

      // Password change form
      passwordForm: {
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
        isSubmitting: false
      },

      // Settings sections
      sections: [
        {
          id: 'appearance',
          name: 'Appearance',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
        },
        {
          id: 'academic',
          name: 'Academic',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>'
        },
        {
          id: 'account',
          name: 'Account & Security',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
        },
        {
          id: 'accessibility',
          name: 'Accessibility',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4"></path><path d="M12 16h.01"></path></svg>'
        },
        {
          id: 'calendar',
          name: 'Calendar & Events',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>'
        }
      ],

      // Available accent colors
      accentColors: [
        { id: 'purple', value: '#7b49ff' },
        { id: 'blue', value: '#2196f3' },
        { id: 'green', value: '#4caf50' },
        { id: 'red', value: '#f44336' },
        { id: 'orange', value: '#ff9800' },
        { id: 'pink', value: '#e91e63' },
        { id: 'teal', value: '#009688' }
      ],

      // Settings object
      settings: {
        appearance: {
          accentColor: 'purple',
          fontSize: 'medium',
          highContrast: false,
          darkMode: false,
          enableAnimations: true
        },
        academic: {
          gradingScale: [
            { letter: 'A', minPercentage: 90, gpaValue: 4.0 },
            { letter: 'B', minPercentage: 80, gpaValue: 3.0 },
            { letter: 'C', minPercentage: 70, gpaValue: 2.0 },
            { letter: 'D', minPercentage: 60, gpaValue: 1.0 },
            { letter: 'F', minPercentage: 0, gpaValue: 0.0 }
          ],
          termStartDate: '',
          termEndDate: '',
          holidays: [],
          // New fields for academic profile
          academicLevel: 'Undergraduate',
          enrollmentType: 'Full time',
          studyPreferences: ['Mornings'], // Allow multiple preferences
          // New fields for degree configuration
          currentYear: 1,
          totalYears: 3,
          semestersPerYear: 2,
          creditsPerYear: 120,
          customCreditsPerYear: null,
          targetGrade: 70,
          customTargetGrade: null,
          // Year weights
          yearWeights: [
            { year: 1, weight: 33, active: true },
            { year: 2, weight: 33, active: true },
            { year: 3, weight: 34, active: true }
          ]
        },
        accessibility: {
          screenReaderOptimized: false,
          keyboardShortcuts: true,
          focusMode: false,
          // New accessibility settings
          colorBlindMode: 'none',
          reduceMotion: false,
          motionIntensity: 75,
          textToSpeech: false,
          ttsVoice: 'default',
          ttsRate: 1,
          ttsPitch: 1,
          screenReaderVerbosity: 'medium'
        },
        calendar: {
          firstDayOfWeek: 'sunday',
          defaultEventDuration: '60',
          defaultEventType: 'general',
          timeFormat: '12h',
          dateFormat: 'MM/DD/YYYY',
          // New calendar settings
          showWeekNumbers: false,
          showCompleted: true,
          highlightToday: true,
          defaultView: 'month',
          enableNotifications: true,
          defaultNotificationTime: 15
        },
        security: {
          twoFactorEnabled: false,
          notificationEmail: '',
          emailNotifications: true,
          activityAlerts: true
        }
      },

      // Default settings for reset functionality
      defaultSettings: null
    };
  },
  computed: {
    // Calculate total weight for year weights
    totalWeight() {
      if (!this.settings.academic.yearWeights?.length) return 0;

      return this.settings.academic.yearWeights.reduce((sum, year) => {
        return sum + (year.active ? year.weight : 0);
      }, 0);
    },

    // Check if any years are active
    hasActiveYears() {
      return this.settings.academic.yearWeights?.some(year => year.active);
    }
  },
  mounted() {
    // Initialize dark mode from localStorage
    this.darkMode = getDarkModePreference();
    // Set initial value in the settings object
    this.settings.appearance.darkMode = this.darkMode;

    // Check if there's a saved accent color
    const savedAccentColor = localStorage.getItem('accentColor');
    if (savedAccentColor) {
      this.settings.appearance.accentColor = savedAccentColor;
    }

    // Apply the accent color
    this.applyAccentColor(this.settings.appearance.accentColor);

    this.checkMobile();

    // Set a localStorage item so App.vue can read it
    localStorage.setItem('keyboardShortcuts', this.settings.accessibility.keyboardShortcuts);

    // Add event listeners
    window.addEventListener("resize", this.checkMobile);
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Store default settings for reset functionality
    this.defaultSettings = JSON.parse(JSON.stringify(this.settings));

    // Fetch user profile and settings
    this.fetchUserProfile();
    this.fetchSettings();

    // Apply color blind mode
    this.applyColorBlindMode();

    // Apply animation settings
    this.toggleAnimations();

    // Apply reduce motion
    this.applyReduceMotion();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);

    // Cleanup for text-to-speech
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }

    // Remove text selection handler for TTS
    document.removeEventListener('mouseup', this.handleTextSelection);
  },
  methods: {
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
      // When dark mode changes, we need to reapply the accent color
      this.$nextTick(() => {
        this.applyAccentColor(this.settings.appearance.accentColor);
        // Reapply color blind adjustments if needed
        if (this.settings.accessibility.colorBlindMode !== 'none') {
          this.applyColorBlindMode();
        }
      });
    },
    handleLogout() {
      this.notLoggedIn = true;
      this.$router.push("/login");
    },
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
      // Close mobile nav when switching to desktop view
      if (!this.isMobile) {
        this.mobileNavOpen = false;
      }
    },
    toggleMobileNav() {
      this.mobileNavOpen = !this.mobileNavOpen;
    },
    selectMobileSection(sectionId) {
      this.activeSection = sectionId;
      this.mobileNavOpen = false; // Close the dropdown after selection
    },
    getCurrentSectionName() {
      const section = this.sections.find(s => s.id === this.activeSection);
      return section ? section.name : 'Settings';
    },
    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_URL}/user/profile`, {
          withCredentials: true,
        });

        if (response.data) {
          this.userProfile = response.data;
          this.notLoggedIn = false;
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
        if (error.response?.status === 401) {
          this.notLoggedIn = true;
        }
      }
    },
    async fetchSettings() {
      try {
        const userSettings = await userSettingsService.fetchSettings();

        if (userSettings) {
          // Merge received settings with defaults to ensure all properties exist
          this.settings = this.mergeDeep(this.settings, userSettings);

          // Make sure the year weights array is properly initialized
          if (!this.settings.academic.yearWeights || !this.settings.academic.yearWeights.length) {
            this.updateYearWeightsBasedOnTotalYears();
          }

          // Make sure study preferences is an array
          if (!Array.isArray(this.settings.academic.studyPreferences)) {
            this.settings.academic.studyPreferences =
                this.settings.academic.studyPreference ?
                    [this.settings.academic.studyPreference] :
                    ['Mornings'];
          }

          // Apply settings after they're loaded
          this.applySettings();
        }
      } catch (error) {
        console.error("Error fetching settings:", error);

        // Use defaults if settings can't be fetched
        if (error.response?.status === 401) {
          this.notLoggedIn = true;
          notify({ type: "warning", message: "Please log in to access settings" });
        } else if (error.response?.status === 404) {
          // First time user, using defaults is fine
          console.log("No settings found, using defaults");
          this.updateYearWeightsBasedOnTotalYears();
        } else {
          notify({ type: "error", message: "Failed to load settings. Using defaults." });
        }
      } finally {
        this.loading = false;
      }
    },
    async saveSettings() {
      this.isSaving = true;
      try {
        const response = await axios.put(
            `${API_URL}/user/settings`,
            this.settings,
            { withCredentials: true }
        );

        // Apply settings using the service
        userSettingsService.applySettings(this.settings);

        // Store accent color in localStorage for persistence
        localStorage.setItem('accentColor', this.settings.appearance.accentColor);

        // Make sure we update the year-dependent components in the UI
        window.dispatchEvent(new CustomEvent('yearSettingsUpdated', {
          detail: {
            yearWeights: this.settings.academic.yearWeights,
            totalYears: this.settings.academic.totalYears,
            creditsPerYear: this.getEffectiveCreditsPerYear()
          }
        }));

        notify({ type: "success", message: "Settings saved successfully!" });
      } catch (error) {
        console.error("Error saving settings:", error);

        if (error.response?.status === 401) {
          this.notLoggedIn = true;
          notify({ type: "error", message: "Please log in to save settings." });
        } else {
          notify({ type: "error", message: "Failed to save settings. Please try again." });
        }
      } finally {
        this.isSaving = false;
      }
    },
    applySettings() {
      // Apply theme from settings instead of always reading from localStorage
      if (this.settings.appearance.darkMode !== undefined) {
        this.darkMode = this.settings.appearance.darkMode;
        setDarkModePreference(this.darkMode); // Update localStorage to match
      } else {
        // Fallback only if setting doesn't exist yet (backward compatibility)
        this.darkMode = getDarkModePreference();
        this.settings.appearance.darkMode = this.darkMode; // Update settings to match
      }

      // Apply accent color with a slight delay to ensure dark mode is applied first
      setTimeout(() => {
        this.applyAccentColor(this.settings.appearance.accentColor);
      }, 50);

      // Apply font size
      this.applyFontSize(this.settings.appearance.fontSize);

      // Apply high contrast if enabled
      if (this.settings.appearance.highContrast) {
        document.documentElement.classList.add('high-contrast');
      } else {
        document.documentElement.classList.remove('high-contrast');
      }

      // Apply keyboard shortcuts (emit event for App.vue)
      window.dispatchEvent(new CustomEvent('settingsChange', {
        detail: {
          setting: 'keyboardShortcuts',
          value: this.settings.accessibility.keyboardShortcuts
        }
      }));

      // Apply focus mode if enabled
      if (this.settings.accessibility.focusMode) {
        document.documentElement.classList.add('focus-mode');
      } else {
        document.documentElement.classList.remove('focus-mode');
      }

      // Apply color blind mode
      this.applyColorBlindMode();

      // Apply reduce motion settings
      this.applyReduceMotion();

      // Apply animation settings
      this.toggleAnimations();

      // Apply calendar settings
      this.applyCalendarSettings();

      // Apply text-to-speech settings
      if (this.settings.accessibility.textToSpeech) {
        this.toggleTextToSpeech();
      }
    },
    resetSettings() {
      // Reset to default settings
      this.settings = JSON.parse(JSON.stringify(this.defaultSettings));

      // Apply reset settings
      this.applySettings();

      // If default theme isn't saved in settings, use system preference
      if (this.defaultSettings.appearance.darkMode === undefined) {
        this.darkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        this.settings.appearance.darkMode = this.darkMode;
        setDarkModePreference(this.darkMode);
      }

      notify({ type: "info", message: "Settings reset to defaults" });
    },
    setTheme(theme) {
      this.darkMode = theme === 'dark';
      this.settings.appearance.darkMode = this.darkMode; // Store in settings object
      setDarkModePreference(this.darkMode); // Still update localStorage for app-wide state

      // Dispatch dark mode change event
      window.dispatchEvent(new CustomEvent('darkModeChange', {
        detail: { isDark: this.darkMode }
      }));

      // Reapply accent color after theme change to ensure proper rendering
      this.$nextTick(() => {
        this.applyAccentColor(this.settings.appearance.accentColor);
        // Reapply color blind mode after theme change
        this.applyColorBlindMode();
      });
    },
    setAccentColor(colorId) {
      this.settings.appearance.accentColor = colorId;
      localStorage.setItem('accentColor', colorId); // Store in localStorage for persistence
      this.applyAccentColor(colorId);
    },
    applyAccentColor(colorId) {
      const color = this.accentColors.find(c => c.id === colorId);
      if (color) {
        // Set the primary color value
        document.documentElement.style.setProperty('--primary-color', color.value);

        // Calculate darker variant for hover states
        const darkerColor = this.adjustColor(color.value, -20);
        document.documentElement.style.setProperty('--primary-dark', darkerColor);

        // Calculate lighter variant
        const lighterColor = this.adjustColor(color.value, 20);
        document.documentElement.style.setProperty('--primary-light', lighterColor);

        // Apply to active elements that might need the color in dark mode
        document.documentElement.style.setProperty('--active-color', color.value);

        // Also set RGB values for transparency
        const rgb = this.hexToRgb(color.value);
        if (rgb) {
          document.documentElement.style.setProperty('--primary-color-rgb', `${rgb.r}, ${rgb.g}, ${rgb.b}`);
        }

        // Force update of elements that might be using the accent color
        this.$forceUpdate();
      }
    },
    // Helper to convert hex to RGB
    hexToRgb(hex) {
      // Remove # if present
      hex = hex.replace(/^#/, '');

      // Parse hex values
      const bigint = parseInt(hex, 16);
      const r = (bigint >> 16) & 255;
      const g = (bigint >> 8) & 255;
      const b = bigint & 255;

      return { r, g, b };
    },
    adjustColor(hex, amount) {
      // Convert hex to RGB
      let r = parseInt(hex.slice(1, 3), 16);
      let g = parseInt(hex.slice(3, 5), 16);
      let b = parseInt(hex.slice(5, 7), 16);

      // In dark mode, we might want slightly different adjustment logic
      if (this.darkMode && amount < 0) {
        // For dark mode, make darker colors even more distinct
        amount = amount * 1.5;
      } else if (this.darkMode && amount > 0) {
        // For dark mode, make lighter colors more pronounced
        amount = amount * 1.2;
      }

      // Adjust colors
      r = Math.max(0, Math.min(255, r + amount));
      g = Math.max(0, Math.min(255, g + amount));
      b = Math.max(0, Math.min(255, b + amount));

      // Store RGB values as CSS variables for easier alpha adjustments
      const rgbValue = `${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}`;
      document.documentElement.style.setProperty('--primary-color-rgb', rgbValue);

      // Convert back to hex
      return `#${Math.round(r).toString(16).padStart(2, '0')}${Math.round(g).toString(16).padStart(2, '0')}${Math.round(b).toString(16).padStart(2, '0')}`;
    },
    applyFontSize(size) {
      const sizeMap = {
        'small': '14px',
        'medium': '16px',
        'large': '18px'
      };

      document.documentElement.style.setProperty('--font-size-base', sizeMap[size] || '16px');

      // Dispatch an event so other components can update if needed
      window.dispatchEvent(new CustomEvent('fontSizeChanged', {
        detail: { size: size }
      }));
    },
    toggleHighContrast() {
      if (this.settings.appearance.highContrast) {
        document.documentElement.classList.add('high-contrast');
      } else {
        document.documentElement.classList.remove('high-contrast');
      }

      // Dispatch an event so other components can update if needed
      window.dispatchEvent(new CustomEvent('highContrastChanged', {
        detail: { enabled: this.settings.appearance.highContrast }
      }));
    },
    toggleAnimations() {
      // Apply animation setting
      if (!this.settings.appearance.enableAnimations) {
        document.documentElement.classList.add('disable-animations');
      } else {
        document.documentElement.classList.remove('disable-animations');
      }

      window.dispatchEvent(new CustomEvent('animationsChanged', {
        detail: { enabled: this.settings.appearance.enableAnimations }
      }));
    },
    applyColorBlindMode() {
      // Remove any existing filters
      const existingFilter = document.getElementById('color-blind-filter');
      if (existingFilter) {
        existingFilter.remove();
      }

      // If no color blind mode selected, we're done
      if (this.settings.accessibility.colorBlindMode === 'none') {
        document.documentElement.style.filter = '';
        return;
      }

      // Create SVG filter element
      const svgFilter = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svgFilter.setAttribute('id', 'color-blind-filter');
      svgFilter.style.position = 'absolute';
      svgFilter.style.height = '0';
      svgFilter.style.width = '0';
      svgFilter.style.overflow = 'hidden';

      // Add filter definitions based on selected mode
      let filterContent = '';

      switch (this.settings.accessibility.colorBlindMode) {
        case 'protanopia':
          // Red-blind
          filterContent = `
            <filter id="protanopia">
              <feColorMatrix
                type="matrix"
                values="0.567, 0.433, 0,     0, 0
                        0.558, 0.442, 0,     0, 0
                        0,     0.242, 0.758, 0, 0
                        0,     0,     0,     1, 0"/>
            </filter>
          `;
          break;
        case 'deuteranopia':
          // Green-blind
          filterContent = `
            <filter id="deuteranopia">
              <feColorMatrix
                type="matrix"
                values="0.625, 0.375, 0,   0, 0
                        0.7,   0.3,   0,   0, 0
                        0,     0.3,   0.7, 0, 0
                        0,     0,     0,   1, 0"/>
            </filter>
          `;
          break;
        case 'tritanopia':
          // Blue-blind
          filterContent = `
            <filter id="tritanopia">
              <feColorMatrix
                type="matrix"
                values="0.95, 0.05,  0,     0, 0
                        0,    0.433, 0.567, 0, 0
                        0,    0.475, 0.525, 0, 0
                        0,    0,     0,     1, 0"/>
            </filter>
          `;
          break;
        case 'achromatopsia':
          // Monochrome
          filterContent = `
            <filter id="achromatopsia">
              <feColorMatrix
                type="matrix"
                values="0.299, 0.587, 0.114, 0, 0
                        0.299, 0.587, 0.114, 0, 0
                        0.299, 0.587, 0.114, 0, 0
                        0,     0,     0,     1, 0"/>
            </filter>
          `;
          break;
      }

      svgFilter.innerHTML = filterContent;
      document.body.appendChild(svgFilter);

      // Apply filter to the entire document
      document.documentElement.style.filter = `url(#${this.settings.accessibility.colorBlindMode})`;

      // Dispatch event for other components
      window.dispatchEvent(new CustomEvent('colorBlindModeChanged', {
        detail: { mode: this.settings.accessibility.colorBlindMode }
      }));
    },
    applyReduceMotion() {
      if (this.settings.accessibility.reduceMotion) {
        document.documentElement.classList.add('reduce-motion');
        // Force all animations to be turned off
        document.documentElement.style.setProperty('--transition-speed', '0s');
      } else {
        document.documentElement.classList.remove('reduce-motion');
        // Restore normal transitions
        document.documentElement.style.setProperty('--transition-speed', '0.3s');

        // Apply motion intensity if applicable
        this.applyMotionIntensity();
      }

      window.dispatchEvent(new CustomEvent('reduceMotionChanged', {
        detail: { enabled: this.settings.accessibility.reduceMotion }
      }));
    },
    applyMotionIntensity() {
      if (!this.settings.accessibility.reduceMotion) {
        // Scale transition duration based on intensity (0-100)
        const intensity = this.settings.accessibility.motionIntensity / 100;
        const transitionDuration = 0.1 + (intensity * 0.4); // Range from 0.1s to 0.5s

        document.documentElement.style.setProperty('--transition-speed', `${transitionDuration}s`);
      }
    },
    toggleTextToSpeech() {
      // When enabled, initialize the speech synthesis
      if (this.settings.accessibility.textToSpeech && window.speechSynthesis) {
        // Add event listener for text selection
        document.addEventListener('mouseup', this.handleTextSelection);
      } else {
        // Remove event listener when disabled
        document.removeEventListener('mouseup', this.handleTextSelection);

        // Cancel any ongoing speech
        if (window.speechSynthesis) {
          window.speechSynthesis.cancel();
        }
      }
    },
    handleTextSelection() {
      const selectedText = window.getSelection().toString().trim();

      if (selectedText && this.settings.accessibility.textToSpeech) {
        this.speakText(selectedText);
      }
    },
    speakText(text) {
      if (!window.speechSynthesis) return;

      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);

      // Apply voice settings
      utterance.rate = parseFloat(this.settings.accessibility.ttsRate);
      utterance.pitch = parseFloat(this.settings.accessibility.ttsPitch);

      // Set voice if available
      if (this.settings.accessibility.ttsVoice !== 'default') {
        const voices = window.speechSynthesis.getVoices();
        const voiceType = this.settings.accessibility.ttsVoice;

        // Try to find appropriate voice
        const voiceFound = voices.find(voice => {
          if (voiceType === 'male') {
            return voice.name.toLowerCase().includes('male');
          } else if (voiceType === 'female') {
            return voice.name.toLowerCase().includes('female');
          }
          return false;
        });

        if (voiceFound) {
          utterance.voice = voiceFound;
        }
      }

      window.speechSynthesis.speak(utterance);
    },
    testTextToSpeech() {
      this.speakText(this.testTtsText);
    },
    toggleTwoFactor() {
      if (this.settings.security.twoFactorEnabled) {
        // If enabling 2FA, show setup UI
        this.showTfaSetup = true;
      } else {
        // If disabling 2FA, hide setup UI
        this.showTfaSetup = false;
      }
    },
    verifyTfaCode() {
      // This would verify with the backend in a real implementation
      if (this.tfaVerificationCode.length === 6) {
        // Simulate successful verification
        this.settings.security.twoFactorEnabled = true;
        this.showTfaSetup = false;
        notify({ type: "success", message: "Two-factor authentication enabled!" });
      } else {
        notify({ type: "error", message: "Please enter a valid 6-digit code" });
      }
    },
    resetTwoFactor() {
      // This would reset 2FA on the backend in a real implementation
      this.settings.security.twoFactorEnabled = false;
      this.showTfaSetup = true;
      notify({ type: "info", message: "Two-factor authentication has been reset" });
    },
    applyAccessibilitySettings() {
      // Apply keyboard shortcuts
      window.dispatchEvent(new CustomEvent('settingsChange', {
        detail: {
          setting: 'keyboardShortcuts',
          value: this.settings.accessibility.keyboardShortcuts
        }
      }));

      // Apply screen reader optimization
      window.dispatchEvent(new CustomEvent('settingsChange', {
        detail: {
          setting: 'screenReaderOptimized',
          value: this.settings.accessibility.screenReaderOptimized
        }
      }));

      // Apply screen reader verbosity setting
      if (this.settings.accessibility.screenReaderOptimized) {
        window.dispatchEvent(new CustomEvent('screenReaderVerbosityChanged', {
          detail: { level: this.settings.accessibility.screenReaderVerbosity }
        }));
      }

      // Apply focus mode
      if (this.settings.accessibility.focusMode) {
        document.documentElement.classList.add('focus-mode');
      } else {
        document.documentElement.classList.remove('focus-mode');
      }

      window.dispatchEvent(new CustomEvent('settingsChange', {
        detail: {
          setting: 'focusMode',
          value: this.settings.accessibility.focusMode
        }
      }));
    },
    applyCalendarSettings() {
      // Dispatch calendar settings event for the calendar component to pick up
      window.dispatchEvent(new CustomEvent('calendarSettingsChanged', {
        detail: {
          firstDayOfWeek: this.settings.calendar.firstDayOfWeek,
          defaultEventDuration: this.settings.calendar.defaultEventDuration,
          defaultEventType: this.settings.calendar.defaultEventType,
          timeFormat: this.settings.calendar.timeFormat,
          dateFormat: this.settings.calendar.dateFormat,
          // New settings
          showWeekNumbers: this.settings.calendar.showWeekNumbers,
          showCompleted: this.settings.calendar.showCompleted,
          highlightToday: this.settings.calendar.highlightToday,
          defaultView: this.settings.calendar.defaultView,
          enableNotifications: this.settings.calendar.enableNotifications,
          defaultNotificationTime: this.settings.calendar.defaultNotificationTime
        }
      }));
    },
    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        notify({ type: "error", message: "New passwords do not match" });
        return;
      }

      this.passwordForm.isSubmitting = true;
      try {
        await axios.put(
            `${API_URL}/user/password`,
            {
              current_password: this.passwordForm.currentPassword,
              new_password: this.passwordForm.newPassword
            },
            { withCredentials: true }
        );

        notify({ type: "success", message: "Password changed successfully!" });

        // Reset form
        this.passwordForm.currentPassword = "";
        this.passwordForm.newPassword = "";
        this.passwordForm.confirmPassword = "";
      } catch (error) {
        console.error("Error changing password:", error);

        if (error.response?.status === 400) {
          notify({ type: "error", message: error.response.data.message || "Current password is incorrect" });
        } else {
          notify({ type: "error", message: "Failed to change password. Please try again." });
        }
      } finally {
        this.passwordForm.isSubmitting = false;
      }
    },
    // Academic-specific methods
    toggleStudyPreference(preference) {
      // Initialize array if it doesn't exist
      if (!Array.isArray(this.settings.academic.studyPreferences)) {
        this.settings.academic.studyPreferences = [];
      }

      // Toggle (add/remove) the preference
      const index = this.settings.academic.studyPreferences.indexOf(preference);
      if (index === -1) {
        // Add the preference
        this.settings.academic.studyPreferences.push(preference);
      } else {
        // Remove the preference only if it's not the last one
        if (this.settings.academic.studyPreferences.length > 1) {
          this.settings.academic.studyPreferences.splice(index, 1);
        } else {
          notify({ type: "warning", message: "You must have at least one study preference selected." });
        }
      }
    },
    updateYearWeightsBasedOnTotalYears() {
      const totalYears = typeof this.settings.academic.totalYears === 'number' ?
          this.settings.academic.totalYears : 3;

      // Create default year weights array if it doesn't exist
      if (!this.settings.academic.yearWeights) {
        this.settings.academic.yearWeights = [];
      }

      // Calculate default weight per year
      const defaultWeight = Math.floor(100 / totalYears);
      const remainder = 100 - (defaultWeight * totalYears);

      // Create a new array with the correct number of years
      const newYearWeights = [];

      for (let i = 0; i < totalYears; i++) {
        // If existing year weight is available, use it
        if (i < this.settings.academic.yearWeights.length) {
          newYearWeights.push(this.settings.academic.yearWeights[i]);
        } else {
          // Add new year weight with default values
          newYearWeights.push({
            year: i + 1,
            weight: i === totalYears - 1 ? defaultWeight + remainder : defaultWeight,
            active: true
          });
        }
      }

      // Update the settings object
      this.settings.academic.yearWeights = newYearWeights;
      this.validateYearWeights();
    },
    validateYearWeights() {
      if (!this.settings.academic.yearWeights) return;

      // Validate individual weights (cap at 100)
      this.settings.academic.yearWeights.forEach(year => {
        if (year.weight > 100) year.weight = 100;
        if (year.weight < 0) year.weight = 0;
      });

      // If only one active year, force it to 100%
      const activeYears = this.settings.academic.yearWeights.filter(y => y.active);
      if (activeYears.length === 1) {
        activeYears[0].weight = 100;
      }
    },
    getEffectiveCreditsPerYear() {
      // Return the numeric value of credits per year, handling the custom option
      if (this.settings.academic.creditsPerYear === 'custom') {
        return this.settings.academic.customCreditsPerYear || 120;
      } else {
        return parseInt(this.settings.academic.creditsPerYear, 10) || 120;
      }
    },
    addGrade() {
      this.settings.academic.gradingScale.push({
        letter: '',
        minPercentage: 0,
        gpaValue: 0
      });
    },
    removeGrade(index) {
      this.settings.academic.gradingScale.splice(index, 1);
    },
    addHoliday() {
      this.settings.academic.holidays.push({
        name: '',
        startDate: '',
        endDate: ''
      });
    },
    removeHoliday(index) {
      this.settings.academic.holidays.splice(index, 1);
    },
    // Deep merge utility for merging settings objects
    mergeDeep(target, source) {
      const output = Object.assign({}, target);
      if (this.isObject(target) && this.isObject(source)) {
        Object.keys(source).forEach(key => {
          if (this.isObject(source[key])) {
            if (!(key in target)) {
              Object.assign(output, { [key]: source[key] });
            } else {
              output[key] = this.mergeDeep(target[key], source[key]);
            }
          } else {
            Object.assign(output, { [key]: source[key] });
          }
        });
      }
      return output;
    },
    isObject(item) {
      return (item && typeof item === 'object' && !Array.isArray(item));
    }
  }
};
</script>

<style scoped>
/* Basic variables - Update to include RGB versions for transparency */
:root {
  --primary-color: #7b49ff;
  --primary-color-rgb: 123, 73, 255;
  --primary-light: #9b7aff;
  --primary-dark: #5b34cc;
  --error-color: #f44336;
  --error-color-rgb: 244, 67, 54;
  --success-color: #4caf50;
  --success-color-rgb: 76, 175, 80;
  --warning-color: #ff9800;
  --warning-color-rgb: 255, 152, 0;
  --info-color: #2196f3;
  --info-color-rgb: 33, 150, 243;
  --text-primary: #333;
  --text-secondary: #666;
  --text-tertiary: #999;
  --bg-light: #f5f7fa;
  --bg-card: #ffffff;
  --bg-input: #f5f7fa;
  --bg-hover: #f0f0f0;
  --border-color: #e1e4e8;
  --border-color-light: #f0f0f0;
  --border-radius: 8px;
  --border-radius-lg: 12px;
  --border-radius-xl: 20px;
  --shadow-sm: 0 2px 5px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 10px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 10px 20px rgba(0, 0, 0, 0.1);
  --font-size-base: 16px;
  --transition-speed: 0.3s;
  --focus-outline: 2px solid rgba(123, 73, 255, 0.5);
}

/* Dark mode variables */
.dark-mode {
  --text-primary: #e4e6eb;
  --text-secondary: #b0b3b8;
  --text-tertiary: #777;
  --bg-light: #18191a;
  --bg-card: #242526;
  --bg-input: #3a3b3c;
  --bg-hover: #3a3b3c;
  --border-color: #3e4042;
  --border-color-light: #3e4042;
  --shadow-sm: 0 2px 5px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 10px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 20px rgba(0, 0, 0, 0.4);
  --focus-outline: 2px solid rgba(155, 122, 255, 0.6);
}

/* Animation settings */
.disable-animations * {
  transition: none !important;
  animation: none !important;
}

.reduce-motion * {
  transition-duration: 0.001s !important;
  animation-duration: 0.001s !important;
}

/* Base styles */
.settings-page {
  min-height: 100vh;
  background-color: var(--bg-light);
  color: var(--text-primary);
  transition: background-color var(--transition-speed) ease,
  color var(--transition-speed) ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.dashboard-layout {
  display: flex;
  flex-direction: row;
  position: relative;
  padding-top: 70px; /* Space for fixed navbar */
  min-height: calc(100vh - 70px);
}

/* Main Content Styles */
.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all var(--transition-speed) ease;
  margin-bottom: 80px; /* Space for fixed bottom buttons */
}

.dashboard-header {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dashboard-header h1 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
}

.settings-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
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
  border: 4px solid rgba(var(--primary-color-rgb), 0.1);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.auth-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.auth-card svg {
  color: var(--primary-color);
  opacity: 0.9;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.auth-card:hover svg {
  opacity: 1;
  transform: scale(1.05);
}

.auth-card h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
}

.auth-card p {
  margin: 0;
  color: var(--text-secondary);
}

.login-button {
  display: inline-block;
  background: var(--primary-color);
  color: white;
  padding: 0.85rem 1.75rem;
  border-radius: 24px;
  text-decoration: none;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.login-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(var(--primary-color-rgb), 0.3);
}

.login-button:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.login-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.login-button:focus:not(:active)::after {
  animation: ripple 1s ease-out;
}

@keyframes ripple {
  0% {
    transform: scale(0, 0);
    opacity: 0.5;
  }
  20% {
    transform: scale(25, 25);
    opacity: 0.3;
  }
  100% {
    opacity: 0;
    transform: scale(40, 40);
  }
}

/* Settings content */
.settings-content {
  display: flex;
  gap: 2rem;
}

/* Mobile dropdown */
.mobile-settings-dropdown {
  width: 100%;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 10;
}

.dropdown-selector {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--border-color);
}

.dropdown-selector:hover {
  background-color: var(--bg-hover);
  transform: translateY(-1px);
}

.dropdown-selector:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.dropdown-icon {
  transition: transform 0.3s ease;
}

.dropdown-icon.open {
  transform: rotate(180deg);
}

.mobile-nav-menu {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  right: 0;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  overflow: hidden;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.mobile-nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  width: 100%;
  border: none;
  border-bottom: 1px solid var(--border-color);
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: var(--text-primary);
}

.mobile-nav-item:last-child {
  border-bottom: none;
}

.mobile-nav-item:hover {
  background-color: var(--bg-hover);
}

.mobile-nav-item:focus {
  outline: var(--focus-outline);
  z-index: 1;
}

.mobile-nav-item.active {
  background-color: rgba(var(--primary-color-rgb), 0.1);
  color: var(--primary-color);
  font-weight: 500;
}

.mobile-nav-item .icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-nav-item .icon svg {
  stroke-width: 2;
  width: 18px;
  height: 18px;
}

/* Desktop settings navigation */
.settings-navigation {
  width: 220px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1rem;
  box-shadow: var(--shadow-md);
  align-self: flex-start;
  position: sticky;
  top: 85px; /* Stick below navbar */
  height: fit-content;
  transition: box-shadow 0.3s ease;
}

.settings-navigation:hover {
  box-shadow: var(--shadow-lg);
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-size: 0.95rem;
  position: relative;
  overflow: hidden;
}

.nav-button .icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: color 0.2s ease;
}

.nav-button:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
  transform: translateX(2px);
}

.nav-button:focus {
  outline: var(--focus-outline);
  outline-offset: -2px;
}

.nav-button.active {
  background-color: var(--primary-color);
  color: white;
  font-weight: 500;
  box-shadow: 0 4px 8px rgba(var(--primary-color-rgb), 0.3);
}

.nav-button.active .icon {
  color: white;
}

.nav-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(var(--primary-color-rgb), 0.3);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.nav-button:active::after {
  animation: ripple 0.8s ease-out;
}

/* Settings panel */
.settings-panel {
  flex: 1;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: 2rem;
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.settings-panel:hover {
  box-shadow: var(--shadow-lg);
}

.settings-section {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.settings-section h2 {
  margin: 0 0 1.5rem;
  font-size: 1.35rem;
  font-weight: 600;
  color: var(--primary-color);
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-color);
  position: relative;
}

.settings-section h2::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: var(--primary-color);
  border-radius: 3px;
}

.setting-group {
  margin-bottom: 2.5rem;
  background-color: var(--bg-light);
  padding: 1.5rem;
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
  border: 1px solid var(--border-color-light);
}

.setting-group:hover {
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.setting-group:last-child {
  margin-bottom: 0;
}

.setting-group h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.setting-description {
  color: var(--text-secondary);
  margin-bottom: 1.25rem;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Theme selection */
.theme-selector {
  display: flex;
  gap: 1rem;
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1.25rem;
  border-radius: var(--border-radius);
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.25s ease;
  flex: 1;
  justify-content: center;
  font-weight: 500;
}

.theme-option:hover {
  background-color: var(--bg-hover);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.theme-option:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.theme-option.active {
  border-color: var(--primary-color);
  background-color: rgba(var(--primary-color-rgb), 0.08);
  box-shadow: 0 4px 10px rgba(var(--primary-color-rgb), 0.15);
  transform: translateY(-3px);
}

.theme-option svg {
  transition: transform 0.3s ease;
}

.theme-option:hover svg {
  transform: rotate(15deg);
}

.dark-mode .theme-option.active {
  background-color: rgba(var(--primary-color-rgb), 0.15);
}

/* Color options */
.color-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  justify-content: center;
  padding: 0.5rem;
}

.dark-mode .color-options {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 1.25rem;
  border-radius: var(--border-radius);
}

.color-option {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: var(--shadow-sm);
}

.color-option:hover {
  transform: scale(1.15) translateY(-2px);
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.15);
}

.color-option:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.color-option.active {
  border-color: var(--text-primary);
  transform: scale(1.15);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.color-option.active::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 18px;
  height: 18px;
  background-color: white;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.dark-mode .color-option.active {
  border-color: white;
}

.dark-mode .color-option.active::after {
  background-color: rgba(255, 255, 255, 0.7);
}

/* Toggle switch */
.toggle-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 0;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 52px;
  height: 26px;
  flex-shrink: 0;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 26px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

.dark-mode input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

input:focus + .toggle-slider {
  outline: var(--focus-outline);
  outline-offset: 1px;
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

/* Radio options */
.radio-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem 0;
}

.radio-option input[type="radio"] {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid var(--border-color);
  margin: 0;
  cursor: pointer;
  position: relative;
  transition: border-color 0.2s ease;
}

.radio-option input[type="radio"]:checked {
  border-color: var(--primary-color);
}

.radio-option input[type="radio"]:focus {
  outline: var(--focus-outline);
  outline-offset: 1px;
}

.radio-option input[type="radio"]:checked::after {
  content: "";
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--primary-color);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0);
  animation: radioScale 0.2s forwards;
}

@keyframes radioScale {
  to {
    transform: translate(-50%, -50%) scale(1);
  }
}

.dark-mode .radio-option input[type="radio"]:checked {
  border-color: var(--primary-color);
}

.dark-mode .radio-option input[type="radio"]:checked::after {
  background: var(--primary-color);
}

.radio-option span {
  font-size: 0.95rem;
}

/* Academic Profile Styles */
.academic-profile-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-item {
  background-color: var(--bg-card);
  padding: 1.25rem;
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.profile-item h4 {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 500;
  color: var(--primary-color);
}

.select-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  justify-content: flex-start;
}

.select-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 2px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-secondary);
  padding: 0.85rem 1.35rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.25s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.select-btn:hover {
  border-color: var(--primary-color);
  background: rgba(var(--primary-color-rgb), 0.05);
  color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(var(--primary-color-rgb), 0.1);
}

.select-btn:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.select-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(var(--primary-color-rgb), 0.3);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.select-btn:active::after {
  animation: ripple 0.8s ease-out;
}

.select-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(var(--primary-color-rgb), 0.2);
}

.btn-icon {
  font-size: 1.15rem;
  transition: transform 0.2s ease;
}

.select-btn:hover .btn-icon {
  transform: scale(1.15);
}

.btn-text {
  font-weight: 500;
}

/* Degree Config Styles */
.degree-config-section {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  flex: 1;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.form-group select,
.form-group input[type="text"],
.form-group input[type="number"],
.form-group input[type="date"],
.form-group input[type="email"] {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.2s ease;
}

.form-group select:focus,
.form-group input[type="text"]:focus,
.form-group input[type="number"]:focus,
.form-group input[type="date"]:focus,
.form-group input[type="email"]:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
}

.dark-mode .form-group select:focus,
.dark-mode .form-group input[type="text"]:focus,
.dark-mode .form-group input[type="number"]:focus,
.dark-mode .form-group input[type="date"]:focus,
.dark-mode .form-group input[type="email"]:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.3);
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Custom Value Inputs */
.custom-value-input {
  margin-top: 0.85rem;
  background-color: var(--bg-input);
  padding: 0.85rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-primary);
  width: 100%;
  font-size: 0.95rem;
}

.custom-value-input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
}

/* Target Grade Section */
.target-grade-section {
  margin-top: 0.5rem;
}

.target-grade-btn {
  padding: 0.75rem 1rem;
  flex: 1;
  min-width: 150px;
}

/* Year Weights styles */
.year-weights-container {
  margin-bottom: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  background-color: var(--bg-card);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.year-weights-header {
  display: flex;
  background-color: var(--bg-input);
  padding: 0.85rem;
  font-weight: 600;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
}

.year-weight-row {
  display: flex;
  padding: 0.85rem;
  border-bottom: 1px solid var(--border-color-light);
  transition: background-color 0.2s ease;
}

.year-weight-row:hover {
  background-color: rgba(var(--primary-color-rgb), 0.03);
}

.year-weight-row:last-child {
  border-bottom: none;
}

.year-column {
  flex: 1;
  display: flex;
  align-items: center;
  font-weight: 500;
}

.weight-column {
  flex: 1;
  display: flex;
  align-items: center;
}

.weight-column input {
  width: 80px;
  padding: 0.6rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
  font-size: 0.95rem;
}

.weight-column input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(var(--primary-color-rgb), 0.15);
}

.weight-column input:disabled {
  background-color: var(--bg-light);
  color: var(--text-tertiary);
  cursor: not-allowed;
}

.active-column {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-container {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
  cursor: pointer;
}

.toggle-container input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-switch {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 26px;
  transition: .4s;
}

.toggle-switch:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  border-radius: 50%;
  transition: .4s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

input:checked + .toggle-switch {
  background-color: var(--primary-color);
}

input:checked + .toggle-switch:before {
  transform: translateX(24px);
}

.total-weight {
  padding: 0.85rem;
  text-align: right;
  font-weight: 600;
  background-color: var(--bg-input);
  border-top: 1px solid var(--border-color);
  color: var(--success-color);
}

.weight-error {
  color: var(--warning-color);
}

/* Password input */
.password-input-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.toggle-password:hover {
  color: var(--primary-color);
}

.toggle-password:focus {
  outline: var(--focus-outline);
  outline-offset: 1px;
}

.select-wrapper {
  position: relative;
}

.select-wrapper::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid var(--text-secondary);
  pointer-events: none;
}

.select-wrapper select {
  appearance: none;
  padding-right: 30px;
  cursor: pointer;
}

/* Grading scale */
.grading-scale {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  background-color: var(--bg-card);
}

.grade-row {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  align-items: center;
}

.grade-row:last-child {
  border-bottom: none;
}

.grade-row.header {
  background-color: var(--bg-hover);
  font-weight: 500;
  color: var(--text-primary);
  padding: 0.75rem 0;
}

.grade-letter,
.grade-min,
.grade-gpa {
  padding: 0.75rem;
  flex: 1;
  text-align: center;
}

.grade-action {
  width: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.grade-row input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid transparent;
  border-radius: var(--border-radius);
  text-align: center;
  background-color: transparent;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}

.grade-row input:focus {
  border-color: var(--primary-color);
  background-color: var(--bg-input);
  outline: none;
}

.remove-grade,
.remove-holiday {
  background: transparent;
  border: none;
  color: var(--error-color);
  cursor: pointer;
  padding: 0.5rem;
  opacity: 0.7;
  transition: opacity 0.2s ease, background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.remove-grade:hover,
.remove-holiday:hover {
  opacity: 1;
  background-color: rgba(var(--error-color-rgb), 0.1);
}

.remove-grade:focus,
.remove-holiday:focus {
  outline: var(--focus-outline);
  outline-offset: 1px;
}

.add-grade-btn,
.add-holiday-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background-color: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: var(--border-radius);
  color: var(--primary-color);
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.2s ease;
  font-weight: 500;
}

.add-grade-btn:hover,
.add-holiday-btn:hover {
  background-color: rgba(var(--primary-color-rgb), 0.05);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.add-grade-btn:focus,
.add-holiday-btn:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.dark-mode .add-grade-btn:hover,
.dark-mode .add-holiday-btn:hover {
  background-color: rgba(var(--primary-color-rgb), 0.1);
  border-color: var(--primary-color);
}

/* Holiday items */
.holiday-item {
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  position: relative;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.holiday-item:hover {
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.holiday-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.holiday-name {
  font-weight: 500;
  flex: 1;
}

.holiday-dates {
  display: flex;
  gap: 1rem;
}

/* Password form */
.password-form {
  max-width: 500px;
}

/* Keyboard shortcuts */
.shortcuts-list {
  margin-top: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  background-color: var(--bg-card);
}

.shortcut-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-color);
}

.shortcut-item:last-child {
  border-bottom: none;
}

.shortcut-keys {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.key {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background-color: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 0.8rem;
  font-family: monospace;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Fixed bottom actions */
.settings-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-color);
  padding: 1rem 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  z-index: 100;
  box-shadow: var(--shadow-md);
}

.reset-button,
.save-button,
.verify-code-btn,
.reset-tfa-btn,
.test-tts-btn {
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-xl);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}

.reset-button {
  background-color: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.reset-button:hover {
  background-color: var(--bg-hover);
  border-color: var(--text-secondary);
  transform: translateY(-2px);
}

.reset-button:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.save-button {
  background-color: var(--primary-color);
  border: none;
  color: white;
  min-width: 120px;
  box-shadow: 0 3px 6px rgba(var(--primary-color-rgb), 0.2);
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 12px rgba(var(--primary-color-rgb), 0.3);
}

.save-button:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

.dark-mode .save-button {
  background-color: var(--primary-color);
}

.dark-mode .save-button:hover {
  background-color: var(--primary-dark);
}

.save-button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.verify-code-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  margin-top: 0.5rem;
}

.verify-code-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

.reset-tfa-btn {
  background-color: var(--warning-color);
  color: white;
  border: none;
  margin-top: 0.5rem;
}

.reset-tfa-btn:hover {
  background-color: darkorange;
  transform: translateY(-2px);
}

.test-tts-btn {
  background-color: var(--info-color);
  color: white;
  border: none;
  margin-top: 0.5rem;
}

.test-tts-btn:hover {
  background-color: #0b7dda;
  transform: translateY(-2px);
}

/* Center content for auth prompt */
.center-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* Button ripple effect */
.reset-button::after,
.save-button::after,
.verify-code-btn::after,
.reset-tfa-btn::after,
.test-tts-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.reset-button:active::after,
.save-button:active::after,
.verify-code-btn:active::after,
.reset-tfa-btn:active::after,
.test-tts-btn:active::after {
  animation: ripple 0.8s ease-out;
}

/* High contrast mode styles */
:root.high-contrast {
  --primary-color: #0050c8;
  --primary-dark: #003b94;
  --primary-light: #4d89f0;
  --error-color: #d50000;
  --success-color: #008a00;
  --warning-color: #e65100;
  --text-primary: #000000;
  --text-secondary: #333333;
  --bg-light: #ffffff;
  --bg-card: #f8f8f8;
  --bg-input: #ffffff;
  --bg-hover: #e6e6e6;
  --border-color: #000000;
  --focus-outline: 3px solid #000000;
}

:root.high-contrast.dark-mode {
  --primary-color: #82b1ff;
  --primary-dark: #448aff;
  --primary-light: #bbdefb;
  --text-primary: #ffffff;
  --text-secondary: #dddddd;
  --bg-light: #000000;
  --bg-card: #121212;
  --bg-input: #1e1e1e;
  --bg-hover: #2a2a2a;
  --border-color: #ffffff;
  --focus-outline: 3px solid #ffffff;
}

/* Focus mode styles */
:root.focus-mode .settings-navigation,
:root.focus-mode .mobile-settings-dropdown {
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

:root.focus-mode .settings-navigation:hover,
:root.focus-mode .mobile-settings-dropdown:hover {
  opacity: 1;
}

:root.focus-mode .settings-panel {
  box-shadow: 0 0 0 4px rgba(var(--primary-color-rgb), 0.2);
}

:root.focus-mode .setting-group:not(:hover) {
  opacity: 0.85;
}

/* New styles for TFA Setup */
.tfa-setup-section {
  margin-top: 1.5rem;
  background-color: var(--bg-card);
  padding: 1.5rem;
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.setup-steps {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.setup-steps li {
  margin-bottom: 0.75rem;
}

.qr-code-container {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0;
}

.qr-code-placeholder {
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-light);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-weight: bold;
}

.verification-code-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 200px;
  margin: 0 auto;
}

/* Color Blind Preview Styles */
.color-blind-preview {
  margin-top: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 1rem;
}

.preview-title {
  font-weight: 500;
  margin-bottom: 1rem;
}

.color-samples {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.color-sample {
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  color: white;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
  min-width: 80px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

/* Screen Reader Verbosity Settings */
.indented-option {
  margin-top: 1rem;
  margin-left: 2.5rem;
  padding: 1rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

/* Motion Settings */
.motion-level {
  margin-top: 1rem;
  margin-left: 2.5rem;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.25rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

input[type="range"] {
  width: 100%;
  height: 5px;
  -webkit-appearance: none;
  appearance: none;
  background: linear-gradient(to right, var(--text-tertiary), var(--primary-color));
  outline: none;
  border-radius: 5px;
  margin: 1rem 0 0.5rem;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: var(--primary-color);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.1s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

input[type="range"]:focus {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

/* TTS Options */
.tts-options {
  margin-top: 1rem;
  padding: 1rem;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.tts-options .form-group {
  margin-bottom: 1.5rem;
}

.tts-options .range-labels {
  display: flex;
  justify-content: space-between;
}

/* Responsive styles */
@media (max-width: 768px) {
  .dashboard-main-content {
    padding: 1rem;
  }

  .settings-content {
    flex-direction: column;
  }

  .settings-panel {
    padding: 1.25rem;
  }

  .setting-group {
    padding: 1.25rem;
  }

  .theme-selector,
  .color-options,
  .radio-options {
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .theme-option {
    flex: none;
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .form-row {
    flex-direction: column;
  }

  /* Adjust profile section for mobile */
  .select-group {
    flex-direction: column;
  }

  .select-btn {
    width: 100%;
  }

  /* Adjust grading scale for mobile */
  .grade-row {
    font-size: 0.85rem;
  }

  .grade-letter,
  .grade-min,
  .grade-gpa {
    padding: 0.5rem;
  }

  .holiday-dates {
    flex-direction: column;
  }

  .settings-actions {
    padding: 1rem;
    flex-direction: column-reverse;
    gap: 0.5rem;
  }

  .reset-button,
  .save-button {
    width: 100%;
    justify-content: center;
    padding: 1rem;
  }

  /* Make radio options stack on mobile */
  .radio-options {
    flex-direction: column;
    gap: 0.5rem;
  }

  /* Adjust keyboard shortcuts for mobile */
  .shortcut-item {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  /* Adjust color samples for mobile */
  .color-samples {
    flex-direction: column;
    align-items: center;
  }

  .color-sample {
    width: 100%;
  }
}

/* Medium size devices */
@media (min-width: 769px) and (max-width: 1024px) {
  .settings-content {
    gap: 1.5rem;
  }

  .settings-navigation {
    width: 180px;
  }

  .nav-button {
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
  }
}

/* Accessibility focus indicators */
button:focus-visible,
input:focus-visible,
select:focus-visible,
a:focus-visible {
  outline: var(--focus-outline);
  outline-offset: 2px;
  position: relative;
  z-index: 1;
}

/* Skip to main content - accessibility feature */
.skip-to-content {
  position: absolute;
  left: -9999px;
  z-index: 999;
  padding: 1rem;
  background-color: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 0 0 var(--border-radius) var(--border-radius);
}

.skip-to-content:focus {
  left: 50%;
  transform: translateX(-50%);
  top: 0;
}
</style>