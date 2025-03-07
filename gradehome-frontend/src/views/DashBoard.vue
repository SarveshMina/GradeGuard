<template>
  <div class="dashboard" :class="{ 'dark-mode': darkMode }">
    <!-- Dashboard NavBar at the top -->
    <DashboardNavBar
        :userName="userProfile.firstName || 'User'"
        :userEmail="userProfile.email || 'user@example.com'"
        :userAvatar="userProfile.avatar"
        :isMobile="isMobile"
        @logout="handleLogout"
    />

    <!-- Layout container: main content and sidebar -->
    <div class="dashboard-layout">
      <!-- Move the toggle button outside of the main content area -->
      <button
          v-if="!sidebarVisible"
          @click="toggleSidebar"
          class="sidebar-toggle sidebar-show-button"
          aria-label="Show sidebar"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6" />
        </svg>
        <span class="toggle-text">Calendar</span>
      </button>

      <!-- Main Content Area -->
      <div class="dashboard-main-content" :class="{ 'expanded': !sidebarVisible }">
        <div class="dashboard-header">
          <h1>My Dashboard</h1>
          <div class="view-controls">
            <button :class="{ active: activeView === 'overview' }" @click="activeView = 'overview'">Overview</button>
            <button :class="{ active: activeView === 'yearly' }" @click="activeView = 'yearly'">Yearly View</button>
            <button :class="{ active: activeView === 'insights' }" @click="activeView = 'insights'">Insights</button>
          </div>
        </div>

        <!-- If not logged in -->
        <div v-if="notLoggedIn" class="center-content auth-prompt">
          <div class="auth-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <h2>Welcome to GradeGuard</h2>
            <p>Please sign in to access your personalized dashboard.</p>
            <a href="/login" class="login-button">Go to Login</a>
          </div>
        </div>

        <!-- Otherwise, show the wizards or the main dashboard if already set up -->
        <div v-else-if="showSetupWizard" class="center-content">
          <!-- Wizard Step 1: Basic User Preferences -->
          <div class="setup-wizard">
            <div class="wizard-card">
              <div class="wizard-header">
                <div class="step-indicator">Step 1 of 3</div>
                <h2>Welcome! Let's set up your preferences</h2>
                <p>Please select an option for each question to personalize your experience.</p>
              </div>

              <!-- Academic Level -->
              <div class="form-group">
                <label>What is your current academic level?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: userConfig.academicLevel === 'Undergraduate' }"
                          @click="userConfig.academicLevel = 'Undergraduate'">
                    <span class="btn-icon">🎓</span>
                    <span class="btn-text">Undergraduate</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.academicLevel === 'Postgraduate (Masters)' }"
                          @click="userConfig.academicLevel = 'Postgraduate (Masters)'">
                    <span class="btn-icon">🧑‍🎓</span>
                    <span class="btn-text">Masters</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.academicLevel === 'Postgraduate (PhD)' }"
                          @click="userConfig.academicLevel = 'Postgraduate (PhD)'">
                    <span class="btn-icon">👨‍🎓</span>
                    <span class="btn-text">PhD</span>
                  </button>
                </div>
              </div>

              <!-- Enrollment Type -->
              <div class="form-group">
                <label>Are you full-time or part-time?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: userConfig.enrollmentType === 'Full time' }"
                          @click="userConfig.enrollmentType = 'Full time'">
                    <span class="btn-icon">✅</span>
                    <span class="btn-text">Full time</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.enrollmentType === 'Part time' }"
                          @click="userConfig.enrollmentType = 'Part time'">
                    <span class="btn-icon">⏳</span>
                    <span class="btn-text">Part time</span>
                  </button>
                </div>
              </div>

              <!-- Study Preference -->
              <div class="form-group">
                <label>What describes your study preferences best?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Mornings are best' }"
                          @click="userConfig.studyPreference = 'Mornings are best'">
                    <span class="btn-icon">🌅</span>
                    <span class="btn-text">Mornings</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Afternoons are best' }"
                          @click="userConfig.studyPreference = 'Afternoons are best'">
                    <span class="btn-icon">☀️</span>
                    <span class="btn-text">Afternoons</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Evenings are best' }"
                          @click="userConfig.studyPreference = 'Evenings are best'">
                    <span class="btn-icon">🌆</span>
                    <span class="btn-text">Evenings</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: userConfig.studyPreference === 'Late night' }"
                          @click="userConfig.studyPreference = 'Late night'">
                    <span class="btn-icon">🌙</span>
                    <span class="btn-text">Late Night</span>
                  </button>
                </div>
              </div>

              <!-- Save Preferences -->
              <button @click="saveUserConfig" class="save-button">
                <span>Continue to Step 2</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 12h14"></path>
                  <path d="M12 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Wizard Step 2: Degree Configuration (shown if showNextConfig is true) -->
        <div v-else-if="showNextConfig" class="center-content">
          <div class="next-config">
            <div class="wizard-card">
              <div class="wizard-header">
                <div class="step-indicator">Step 2 of 3</div>
                <h2>Degree Configuration</h2>
                <p>Please provide the details for your degree program.</p>
              </div>

              <!-- Current Year -->
              <div class="form-group">
                <label>What year are you currently in?</label>
                <div class="select-group">
                  <button class="select-btn"
                          v-for="n in 5"
                          :key="n"
                          :class="{ active: nextConfig.currentYear === n }"
                          @click="nextConfig.currentYear = n">
                    Year {{ n }}
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.currentYear === 'other' }"
                          @click="nextConfig.currentYear = 'other'">
                    Other
                  </button>
                </div>
                <input v-if="nextConfig.currentYear === 'other'"
                       type="number"
                       min="1"
                       placeholder="Enter your current year"
                       v-model.number="nextConfig.customCurrentYear" />
              </div>

              <!-- (A) How many years? -->
              <div class="form-group">
                <label>How many years in your degree program?</label>
                <div class="select-group">
                  <button class="select-btn"
                          v-for="n in 5"
                          :key="`years-${n}`"
                          :class="{ active: nextConfig.numYears === n }"
                          @click="nextConfig.numYears = n">
                    {{ n }}
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.numYears === 'other' }"
                          @click="nextConfig.numYears = 'other'">
                    Other
                  </button>
                </div>
                <input v-if="nextConfig.numYears === 'other'"
                       type="number"
                       min="1"
                       placeholder="Enter number of years"
                       v-model.number="nextConfig.customYears" />
              </div>

              <!-- (B) Semesters per year -->
              <div class="form-group">
                <label>How many semesters in one academic year?</label>
                <div class="select-group">
                  <button class="select-btn"
                          v-for="n in 4"
                          :key="`semesters-${n}`"
                          :class="{ active: nextConfig.semesters === n }"
                          @click="nextConfig.semesters = n">
                    {{ n }}
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.semesters === 'other' }"
                          @click="nextConfig.semesters = 'other'">
                    Other
                  </button>
                </div>
                <input v-if="nextConfig.semesters === 'other'"
                       type="number"
                       min="1"
                       placeholder="Enter number of semesters"
                       v-model.number="nextConfig.customSemesters" />
              </div>

              <!-- (C) Credits per year -->
              <div class="form-group">
                <label>How many credits per academic year?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 30 }"
                          @click="nextConfig.credits = 30">
                    30
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 60 }"
                          @click="nextConfig.credits = 60">
                    60
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 90 }"
                          @click="nextConfig.credits = 90">
                    90
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 120 }"
                          @click="nextConfig.credits = 120">
                    120
                  </button>
                  <button class="select-btn"
                          :class="{ active: nextConfig.credits === 'other' }"
                          @click="nextConfig.credits = 'other'">
                    Other
                  </button>
                </div>
                <input v-if="nextConfig.credits === 'other'"
                       type="number"
                       min="1"
                       placeholder="Enter number of credits"
                       v-model.number="nextConfig.customCredits" />
              </div>

              <div class="button-group">
                <button class="back-button" @click="goBackToStep1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 12H5"></path>
                    <path d="M12 19l-7-7 7-7"></path>
                  </svg>
                  <span>Back</span>
                </button>
                <button class="save-button" @click="goToYearWeights">
                  <span>Continue to Year Weights</span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14"></path>
                    <path d="M12 5l7 7-7 7"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Wizard Step 3: Year Weights Configuration -->
        <div v-else-if="showYearWeights" class="center-content">
          <div class="next-config">
            <div class="wizard-card">
              <div class="wizard-header">
                <div class="step-indicator">Step 3 of 3</div>
                <h2>Year Weightings</h2>
                <p>Please specify how much each year contributes to your final grade.</p>
              </div>

              <div class="year-weights-container">
                <div class="year-weights-header">
                  <div class="year-column">Year</div>
                  <div class="weight-column">Weight (%)</div>
                  <div class="active-column">Active</div>
                </div>

                <div v-for="(year, index) in yearWeights" :key="index" class="year-weight-row">
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

              <!-- Target Grade -->
              <div class="form-group">
                <label>What is your target grade at the end of your degree?</label>
                <div class="select-group">
                  <button class="select-btn"
                          :class="{ active: targetGrade === 70 }"
                          @click="targetGrade = 70">
                    <span class="btn-text">First Class (70%+)</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: targetGrade === 60 }"
                          @click="targetGrade = 60">
                    <span class="btn-text">2:1 (60-69%)</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: targetGrade === 50 }"
                          @click="targetGrade = 50">
                    <span class="btn-text">2:2 (50-59%)</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: targetGrade === 40 }"
                          @click="targetGrade = 40">
                    <span class="btn-text">Third (40-49%)</span>
                  </button>
                  <button class="select-btn"
                          :class="{ active: targetGrade === 'custom' }"
                          @click="targetGrade = 'custom'">
                    <span class="btn-text">Custom</span>
                  </button>
                </div>
                <input v-if="targetGrade === 'custom'"
                       type="number"
                       min="0"
                       max="100"
                       placeholder="Enter your target percentage"
                       v-model.number="customTargetGrade" />
              </div>

              <div class="button-group">
                <button class="back-button" @click="goBackToDegreeConfig">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 12H5"></path>
                    <path d="M12 19l-7-7 7-7"></path>
                  </svg>
                  <span>Back</span>
                </button>
                <button class="save-button" @click="completeSetup" :disabled="totalWeight !== 100 && hasActiveYears">
                  <span>Complete Setup</span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 6L9 17l-5-5"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Dashboard Content (shown after setup) -->
        <div v-else class="dashboard-content">
          <!-- OVERVIEW TAB -->
          <div v-if="activeView === 'overview'" class="dashboard-overview">
            <!-- Overall Summary Card -->
            <div class="overview-card summary-card">
              <div class="overview-header">
                <h2>Overall Performance</h2>
                <div class="time-filters">
                  <button :class="{ active: selectedTimeframe === 'all' }" @click="selectedTimeframe = 'all'">All Years</button>
                  <button v-for="year in yearsCompleted" :key="year"
                          :class="{ active: selectedTimeframe === year }"
                          @click="selectedTimeframe = year">Year {{ year }}</button>
                </div>
              </div>

              <div class="overview-body">
                <div class="grade-summary">
                  <div class="grade-circle" :style="{ '--percent': overallAverage / 100 }">
                    <div class="grade-value">{{ overallAverage }}%</div>
                    <div class="grade-label">Average</div>
                  </div>

                  <div class="grade-stats">
                    <div class="stats-item">
                      <div class="stats-label">Year Average</div>
                      <div class="stats-value">{{ yearlyAverage }}%</div>
                    </div>
                    <div class="stats-item">
                      <div class="stats-label">Completed</div>
                      <div class="stats-value">{{ completedCredits }}/{{ totalCredits }} Credits</div>
                    </div>
                    <div class="stats-item">
                      <div class="stats-label">Top Module</div>
                      <div class="stats-value">{{ topModule.name }} ({{ topModule.score }}%)</div>
                    </div>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="progress-section">
                  <div class="progress-header">
                    <h3>Progress Breakdown</h3>
                    <div class="progress-legend">
                      <div class="legend-item">
                        <div class="legend-color" style="background-color: #2ecc71;"></div>
                        <div>Achieved</div>
                      </div>
                      <div class="legend-item">
                        <div class="legend-color" style="background-color: #3498db;"></div>
                        <div>Lost</div>
                      </div>
                      <div class="legend-item">
                        <div class="legend-color" style="background-color: #ecf0f1;"></div>
                        <div>Remaining</div>
                      </div>
                    </div>
                  </div>

                  <div class="progress-bar">
                    <div class="progress-segment achieved" :style="{ width: achievedPercentage + '%' }">
                      {{ achievedPercentage }}%
                    </div>
                    <div class="progress-segment lost" :style="{ width: lostPercentage + '%' }">
                      {{ lostPercentage }}%
                    </div>
                    <div class="progress-segment remaining" :style="{ width: remainingPercentage + '%' }">
                      {{ remainingPercentage }}%
                    </div>
                  </div>

                  <div class="progress-targets">
                    <div class="target-item">
                      <div class="target-value">{{ targetHighGrade }}%</div>
                      <div class="target-label">Needed for First Class</div>
                    </div>
                    <div class="target-item">
                      <div class="target-value">{{ targetMediumGrade }}%</div>
                      <div class="target-label">Needed for 2:1</div>
                    </div>
                    <div class="target-item">
                      <div class="target-value">{{ targetLowGrade }}%</div>
                      <div class="target-label">Needed for 2:2</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Visualizations Row -->
            <div class="visualization-row">
              <!-- Grade Distribution Chart -->
              <div class="chart-card">
                <h3>Grade Distribution</h3>
                <div class="chart-container grade-chart">
                  <GradeDistributionChart :moduleData="moduleData" />
                </div>
              </div>

              <!-- Year Comparison Chart -->
              <div class="chart-card">
                <h3>Year Comparison</h3>
                <div class="chart-container year-chart">
                  <YearComparisonChart :yearData="yearData" />
                </div>
              </div>
            </div>

            <!-- Recent Activity and Goals -->
            <div class="bottom-row">
              <!-- Recent Activity -->
              <div class="activity-card">
                <h3>Recent Activity</h3>
                <div class="activity-list">
                  <div v-for="(activity, index) in recentActivities" :key="index" class="activity-item">
                    <div class="activity-icon" :class="activity.type">
                      <svg v-if="activity.type === 'grade'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                      </svg>
                      <svg v-else-if="activity.type === 'submission'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <path d="M12 18v-6"></path>
                        <path d="M8 15h8"></path>
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                      </svg>
                    </div>
                    <div class="activity-content">
                      <div class="activity-title">{{ activity.title }}</div>
                      <div class="activity-description">{{ activity.description }}</div>
                    </div>
                    <div class="activity-time">{{ activity.time }}</div>
                  </div>
                </div>
              </div>

              <!-- Goals Card -->
              <div class="goals-card">
                <h3>Target Goals</h3>
                <div class="goals-list">
                  <div v-for="(goal, index) in goals" :key="index" class="goal-item">
                    <div class="goal-progress">
                      <svg viewBox="0 0 36 36" class="goal-circle">
                        <path class="goal-circle-bg"
                              d="M18 2.0845
                            a 15.9155 15.9155 0 0 1 0 31.831
                            a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <path class="goal-circle-progress"
                              :stroke-dasharray="`${goal.progress}, 100`"
                              d="M18 2.0845
                            a 15.9155 15.9155 0 0 1 0 31.831
                            a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <text x="18" y="20.35" class="goal-percentage">{{ goal.progress }}%</text>
                      </svg>
                    </div>
                    <div class="goal-details">
                      <div class="goal-title">{{ goal.title }}</div>
                      <div class="goal-description">{{ goal.description }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- YEARLY VIEW TAB -->
          <div v-else-if="activeView === 'yearly'" class="yearly-view">
            <!-- Filter and Sort Controls -->
            <div class="filters-row">
              <div class="filter-group">
                <label for="yearFilter">Year:</label>
                <select id="yearFilter" v-model="selectedYear">
                  <option value="all">All Years</option>
                  <option v-for="year in calculatorConfig.years" :key="year.year" :value="year.year">{{ year.year }}</option>
                </select>
              </div>

              <div class="filter-group">
                <label for="sortBy">Sort By:</label>
                <select id="sortBy" v-model="sortMethod">
                  <option value="name">Module Name</option>
                  <option value="semester">Semester</option>
                  <option value="score-asc">Score (Low to High)</option>
                  <option value="score-desc">Score (High to Low)</option>
                  <option value="credits">Credits</option>
                </select>
              </div>

              <div class="filter-group">
                <button @click="exportGrades" class="export-button">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  Export Grades
                </button>
              </div>
            </div>

            <!-- Year Cards -->
            <div v-for="(year, yearIndex) in filteredYears" :key="year.year" class="year-card">
              <div class="year-header">
                <h2>{{ year.year }}</h2>
                <div class="year-stats">
                  <div class="year-stat">
                    <div class="stat-value">{{ year.average }}%</div>
                    <div class="stat-label">Average</div>
                  </div>
                  <div class="year-stat">
                    <div class="stat-value">{{ year.completedCredits }}/{{ year.totalCredits }}</div>
                    <div class="stat-label">Credits</div>
                  </div>
                  <div class="year-stat">
                    <div class="stat-value">{{ year.weight }}%</div>
                    <div class="stat-label">Weight</div>
                  </div>
                </div>
              </div>

              <!-- Year Progress -->
              <div class="year-progress">
                <div class="progress-bar year-progress-bar">
                  <div class="progress-value" :style="{ width: year.average + '%' }">
                    {{ year.average }}%
                  </div>
                </div>
              </div>

              <!-- Modules Grid -->
              <div class="modules-grid">
                <div v-for="(module, moduleIndex) in year.modules" :key="moduleIndex" class="module-card" @click="viewModuleDetails(module)">
                  <div class="module-icon" :class="getModuleIconClass(module.score)">{{ module.code ? module.code.charAt(0) : module.name.charAt(0) }}</div>
                  <div class="module-details">
                    <div class="module-name">{{ module.name }}</div>
                    <div class="module-info">{{ module.credits }} credits | Semester {{ module.semester || 1 }}</div>
                  </div>
                  <div class="module-score" :class="getScoreClass(module.score)">
                    {{ module.score }}%
                  </div>
                </div>
              </div>

              <!-- Add Module Button -->
              <button @click="showAddModuleForm(year)" class="add-module-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Add Module
              </button>
            </div>
          </div>

          <!-- INSIGHTS TAB -->
          <div v-else-if="activeView === 'insights'" class="insights-view">
            <!-- Performance Insights -->
            <div class="insights-card">
              <h2>Performance Insights</h2>

              <div class="insight-metrics">
                <div class="metric-item">
                  <div class="metric-value" :class="getComparisonClass(averageVsTarget)">{{ overallAverage }}%</div>
                  <div class="metric-label">Current Average</div>
                  <div class="metric-comparison">
                    <span :class="getComparisonClass(averageVsTarget)">
                      <svg v-if="averageVsTarget > 0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="18 15 12 9 6 15"></polyline>
                      </svg>
                      <svg v-else-if="averageVsTarget < 0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                      {{ Math.abs(averageVsTarget) }}% {{ averageVsTarget >= 0 ? 'above' : 'below' }} target
                    </span>
                  </div>
                </div>

                <div class="metric-item">
                  <div class="metric-value">{{ predictionAccuracy }}%</div>
                  <div class="metric-label">Prediction Accuracy</div>
                  <div class="metric-comparison">
                    Based on past performance patterns
                  </div>
                </div>

                <div class="metric-item">
                  <div class="metric-value">{{ consistencyScore }}%</div>
                  <div class="metric-label">Consistency Score</div>
                  <div class="metric-comparison">
                    Variance: {{ performanceVariance }}%
                  </div>
                </div>

                <div class="metric-item">
                  <div class="metric-value">{{ improvementRate }}%</div>
                  <div class="metric-label">Improvement Rate</div>
                  <div class="metric-comparison">
                    Over the last semester
                  </div>
                </div>
              </div>
            </div>

            <!-- Visualization Insights -->
            <div class="insights-charts">
              <!-- Performance Trend Chart -->
              <div class="chart-card large-chart">
                <h3>Performance Trends</h3>
                <div class="chart-container performance-chart">
                  <PerformanceChart :performanceData="performanceData" />
                </div>
              </div>

              <div class="small-charts">
                <!-- Subject Strength Chart -->
                <div class="chart-card">
                  <h3>Subject Strengths</h3>
                  <div class="chart-container strengths-chart">
                    <StrengthsRadarChart :strengthsData="strengthsData" />
                  </div>
                </div>

                <!-- Grade Distribution -->
                <div class="chart-card">
                  <h3>Grade Distribution</h3>
                  <div class="chart-container distribution-chart">
                    <GradeDistributionChart :scoreDistribution="scoreDistribution" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Personalized Tips -->
            <div class="insights-tips">
              <h2>Personalized Tips</h2>

              <div class="tips-container">
                <div v-for="(tip, index) in personalizedTips" :key="index" class="tip-card">
                  <div class="tip-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <path d="M12 8v4"></path>
                      <path d="M12 16h.01"></path>
                    </svg>
                  </div>
                  <div class="tip-content">
                    <h4>{{ tip.title }}</h4>
                    <p>{{ tip.description }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Predictive Analysis -->
            <div class="insights-prediction">
              <h2>Predictive Analysis</h2>

              <div class="prediction-scenarios">
                <div class="scenario-card best">
                  <h3>Best Case</h3>
                  <div class="scenario-grade">{{ bestCaseGrade }}%</div>
                  <p>Based on your top performance in similar modules</p>
                </div>

                <div class="scenario-card expected">
                  <h3>Expected</h3>
                  <div class="scenario-grade">{{ expectedGrade }}%</div>
                  <p>Based on your average performance pattern</p>
                </div>

                <div class="scenario-card minimum">
                  <h3>Minimum Target</h3>
                  <div class="scenario-grade">{{ minimumGrade }}%</div>
                  <p>To maintain your current classification</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Module Detail Dialog (appears when a module is clicked) -->
          <div v-if="showModuleDetail" class="module-detail-dialog">
            <div class="dialog-content">
              <div class="dialog-header">
                <h2>{{ selectedModule.name }}</h2>
                <button class="close-dialog" @click="showModuleDetail = false">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>

              <div class="module-info-grid">
                <div class="info-item">
                  <div class="info-label">Module Code</div>
                  <div class="info-value">{{ selectedModule.code || 'N/A' }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">Credits</div>
                  <div class="info-value">{{ selectedModule.credits }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">Year</div>
                  <div class="info-value">{{ selectedModule.year }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">Semester</div>
                  <div class="info-value">{{ selectedModule.semester || 1 }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">Overall Score</div>
                  <div class="info-value score" :class="getScoreClass(selectedModule.score)">{{ selectedModule.score }}%</div>
                </div>
              </div>

              <h3>Assessment Breakdown</h3>
              <div class="assessments-table">
                <div class="table-header">
                  <div class="table-cell">Assessment</div>
                  <div class="table-cell">Weight</div>
                  <div class="table-cell">Your Score</div>
                  <div class="table-cell">Contribution</div>
                </div>
                <div v-for="(assessment, index) in selectedModule.assessments" :key="index" class="table-row">
                  <div class="table-cell">{{ assessment.name }}</div>
                  <div class="table-cell">{{ assessment.weight }}%</div>
                  <div class="table-cell" :class="getScoreClass(assessment.score)">{{ assessment.score }}%</div>
                  <div class="table-cell">{{ (assessment.score * assessment.weight / 100).toFixed(1) }}%</div>
                </div>
              </div>

              <div class="module-charts">
                <div class="module-chart">
                  <h4>Performance vs Class Average</h4>
                  <ModuleComparisonChart :moduleData="selectedModule" />
                </div>
              </div>

              <div class="dialog-actions">
                <button class="edit-button" @click="editModule(selectedModule)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                  Edit Module
                </button>
                <button class="delete-button" @click="deleteModule(selectedModule)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                  </svg>
                  Delete Module
                </button>
              </div>
            </div>
          </div>

          <!-- Add/Edit Module Form Dialog -->
          <div v-if="showModuleForm" class="module-form-dialog">
            <div class="dialog-content">
              <div class="dialog-header">
                <h2>{{ editingModule ? 'Edit Module' : 'Add New Module' }}</h2>
                <button class="close-dialog" @click="showModuleForm = false">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label for="moduleName">Module Name <span class="required">*</span></label>
                  <input type="text" id="moduleName" v-model="moduleForm.name" placeholder="e.g. Introduction to Programming">
                </div>

                <div class="form-group">
                  <label for="moduleCode">Module Code</label>
                  <input type="text" id="moduleCode" v-model="moduleForm.code" placeholder="e.g. CS101">
                </div>

                <div class="form-group">
                  <label for="moduleCredits">Credits <span class="required">*</span></label>
                  <input type="number" id="moduleCredits" v-model.number="moduleForm.credits" min="0">
                </div>

                <div class="form-group">
                  <label for="moduleYear">Year <span class="required">*</span></label>
                  <select id="moduleYear" v-model="moduleForm.year">
                    <option v-for="year in calculatorConfig.years" :key="year.year" :value="year.year">{{ year.year }}</option>
                  </select>
                </div>

                <!-- Add the new semester field here -->
                <div class="form-group">
                  <label for="moduleSemester">Semester <span class="required">*</span></label>
                  <select id="moduleSemester" v-model="moduleForm.semester">
                    <option v-for="option in semesterOptions" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>
              </div>

              <h3>Assessments</h3>
              <div class="assessments-form">
                <div v-for="(assessment, index) in moduleForm.assessments" :key="index" class="assessment-row">
                  <div class="assessment-inputs">
                    <input type="text" v-model="assessment.name" placeholder="Assessment name">
                    <div class="assessment-numbers">
                      <input type="number" v-model.number="assessment.weight" min="0" max="100" placeholder="Weight %">
                      <input type="number" v-model.number="assessment.score" min="0" max="100" placeholder="Score %">
                    </div>
                  </div>
                  <button class="remove-assessment" @click="removeAssessment(index)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </div>

                <button class="add-assessment" @click="addAssessment">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  Add Assessment
                </button>
              </div>

              <div class="total-weight-indicator" :class="{ 'weight-error': totalAssessmentWeight !== 100 }">
                Total Weight: {{ totalAssessmentWeight }}% {{ totalAssessmentWeight !== 100 ? '(Should be 100%)' : '' }}
              </div>

              <div class="dialog-actions">
                <button class="cancel-button" @click="showModuleForm = false">Cancel</button>
                <button class="save-button" @click="saveModule" :disabled="!isModuleFormValid">
                  {{ editingModule ? 'Update Module' : 'Add Module' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar with Calendar -->
      <transition name="slide">
        <aside v-if="sidebarVisible" class="dashboard-sidebar">
          <!-- Hide sidebar button -->
          <button
              @click="toggleSidebar"
              class="sidebar-toggle sidebar-hide-button"
              aria-label="Hide sidebar"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18l6-6-6-6" />
            </svg>
            <span class="toggle-text">Hide</span>
          </button>
          <CalendarSidebar />
        </aside>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { notify } from "@/services/toastService.js";
import DashboardNavBar from "@/components/DashboardNavBar.vue";
import CalendarSidebar from "@/components/CalendarSidebar.vue";
import { getDarkModePreference } from "@/services/darkModeService.js";
import { API_URL } from "@/config.js";

// Import chart components
import GradeDistributionChart from "@/components/charts/GradeDistributionChart.vue";
import YearComparisonChart from "@/components/charts/YearComparisonChart.vue";
import PerformanceChart from "@/components/charts/PerformanceChart.vue";
import StrengthsRadarChart from "@/components/charts/StrengthsRadarChart.vue";
import ModuleComparisonChart from "@/components/charts/ModuleComparisonChart.vue";

export default {
  name: "Dashboard",
  components: {
    DashboardNavBar,
    CalendarSidebar,
    GradeDistributionChart,
    YearComparisonChart,
    PerformanceChart,
    StrengthsRadarChart,
    ModuleComparisonChart
  },
  data() {
    return {
      // Interface control
      darkMode: false,
      notLoggedIn: false,
      sidebarVisible: true,
      isMobile: false,
      activeView: 'overview', // 'overview', 'yearly', or 'insights'
      selectedTimeframe: 'all',
      selectedYear: 'all',
      sortMethod: 'name',
      loading: false,

      // User data
      userProfile: {
        firstName: "",
        email: "",
        avatar: ""
      },

      // Wizard states
      showSetupWizard: false,
      showNextConfig: false,
      showYearWeights: false,

      // Basic user preferences
      userConfig: {
        academicLevel: "",
        enrollmentType: "",
        studyPreference: "",
      },

      // Calculator config
      calculatorConfig: {
        years: [],
      },

      // Next wizard step (degree config)
      nextConfig: {
        currentYear: 1,
        customCurrentYear: 0,
        numYears: 0,
        semesters: 0,
        credits: 0,
        customYears: 0,
        customSemesters: 0,
        customCredits: 0,
      },

      // Year weights config
      yearWeights: [],

      // Target grade
      targetGrade: 70,
      customTargetGrade: 0,

      // Module data
      moduleData: [],

      // Module detail dialog
      showModuleDetail: false,
      selectedModule: null,

      // Module form dialog
      showModuleForm: false,
      editingModule: false,
      moduleForm: {
        name: '',
        code: '',
        credits: 15,
        year: '',
        semester: 1, // Default to semester 1
        score: 0,
        assessments: []
      },

      // Dashboard data
      dashboardStats: {},
      dashboardConfig: {},

      // Recent activities data
      recentActivities: [],

      // Goals data
      goals: [],

      // Year data for comparisons
      yearData: [],

      // Performance data for charts
      performanceData: [],

      // Strengths data for radar chart
      strengthsData: [],

      // Score distribution data
      scoreDistribution: [],

      // Personalized tips
      personalizedTips: []
    };
  },
  computed: {
    // Total weight of all years in calculator config
    totalWeight() {
      if (!this.yearWeights.length) return 0;

      return this.yearWeights.reduce((sum, year) => {
        return sum + (year.active ? year.weight : 0);
      }, 0);
    },

    // Check if any years are active
    hasActiveYears() {
      return this.yearWeights.some(year => year.active);
    },

    // Total assessment weight in module form
    totalAssessmentWeight() {
      return this.moduleForm.assessments.reduce((sum, assessment) => {
        return sum + (assessment.weight || 0);
      }, 0);
    },

    // Check if module form is valid
    isModuleFormValid() {
      return this.moduleForm.name &&
          this.moduleForm.credits > 0 &&
          this.moduleForm.year &&
          this.moduleForm.assessments.length > 0 &&
          this.totalAssessmentWeight === 100;
    },

    // Get overall average across all years
    overallAverage() {
      return this.dashboardStats?.overallAverage || 0;
    },

    // Get current yearly average
    yearlyAverage() {
      const yearlyAvgs = this.dashboardStats?.yearlyAverages || {};
      const latest = Object.keys(yearlyAvgs).sort().pop();
      return latest ? yearlyAvgs[latest] : 0;
    },

    // Get completed and total credits
    completedCredits() {
      return this.dashboardStats?.completedCredits || 0;
    },

    totalCredits() {
      return this.dashboardStats?.totalCredits || 0;
    },

    // Get top module
    topModule() {
      return this.dashboardStats?.topModule || { name: 'N/A', score: 0 };
    },

    // Get progress percentages
    achievedPercentage() {
      const totalPossible = this.completedCredits * 100;
      const achieved = this.moduleData.reduce((sum, module) => sum + (module.score * module.credits), 0);

      return totalPossible > 0 ? Math.round((achieved / totalPossible) * 100) : 0;
    },

    lostPercentage() {
      return Math.round(this.completedCredits / this.totalCredits * 100) - this.achievedPercentage;
    },

    remainingPercentage() {
      return 100 - (this.achievedPercentage + this.lostPercentage);
    },

    // Get target grades needed for different classifications
    targetHighGrade() {
      return this.dashboardStats?.targetHighGrade || 0;
    },

    targetMediumGrade() {
      return this.dashboardStats?.targetMediumGrade || 0;
    },

    targetLowGrade() {
      return this.dashboardStats?.targetLowGrade || 0;
    },

    // Insights tab calculations
    averageVsTarget() {
      // Comparing current average to personal target
      const targetGradeValue = this.targetGrade === 'custom' ? this.customTargetGrade : this.targetGrade;
      return Math.round((this.overallAverage - targetGradeValue) * 10) / 10;
    },

    predictionAccuracy() {
      return 87; // Could be calculated from actual data in the future
    },

    consistencyScore() {
      // Calculate consistency based on standard deviation of scores
      if (this.moduleData.length < 2) return 100;

      const scores = this.moduleData.map(m => m.score);
      const mean = scores.reduce((sum, score) => sum + score, 0) / scores.length;
      const squaredDiffs = scores.map(score => Math.pow(score - mean, 2));
      const variance = squaredDiffs.reduce((sum, sqrDiff) => sum + sqrDiff, 0) / scores.length;
      const stdDev = Math.sqrt(variance);

      // Convert std deviation to a consistency score (lower std dev = higher consistency)
      // Scale so that 0 std dev = 100% consistency, 30+ std dev = 0% consistency
      return Math.max(0, Math.round(100 - (stdDev * 3.33)));
    },

    performanceVariance() {
      // Calculate variance between highest and lowest scores
      if (this.moduleData.length < 2) return 0;

      const scores = this.moduleData.map(m => m.score);
      const highest = Math.max(...scores);
      const lowest = Math.min(...scores);

      return Math.round((highest - lowest) * 10) / 10;
    },

    improvementRate() {
      // Calculate improvement rate between earliest and latest modules
      if (this.moduleData.length < 2) return 0;

      // Sort modules by year (assuming format "Year X")
      const sortedModules = [...this.moduleData].sort((a, b) => {
        const yearA = parseInt(a.year.replace('Year ', ''));
        const yearB = parseInt(b.year.replace('Year ', ''));
        return yearA - yearB;
      });

      // Calculate average for early modules (first year) and latest modules (last year)
      const firstYearModules = sortedModules.filter(m => m.year === sortedModules[0].year);
      const lastYearModules = sortedModules.filter(m => m.year === sortedModules[sortedModules.length - 1].year);

      if (firstYearModules.length === 0 || lastYearModules.length === 0 || firstYearModules[0].year === lastYearModules[0].year) {
        return 0;
      }

      const firstYearAvg = firstYearModules.reduce((sum, m) => sum + m.score, 0) / firstYearModules.length;
      const lastYearAvg = lastYearModules.reduce((sum, m) => sum + m.score, 0) / lastYearModules.length;

      return Math.round(((lastYearAvg - firstYearAvg) / firstYearAvg * 100) * 10) / 10;
    },

    // Predictive grades
    bestCaseGrade() {
      // Based on current average and assuming best possible performance for remaining modules
      const remainingWeight = 100 - Math.round(this.completedCredits / this.totalCredits * 100);
      const bestRemainingScore = 95; // Assuming 95% is reasonable "best case"

      return Math.min(100, Math.round((this.overallAverage * (100 - remainingWeight) / 100) +
          (bestRemainingScore * remainingWeight / 100)));
    },

    expectedGrade() {
      // Based on current trend
      return Math.min(100, Math.round(this.overallAverage + (this.improvementRate > 0 ? this.improvementRate / 10 : 0)));
    },

    minimumGrade() {
      // Minimum needed to maintain classification
      const classificationThresholds = [40, 50, 60, 70];
      const currentClassification = classificationThresholds.filter(t => this.overallAverage >= t).pop() || 40;

      return currentClassification;
    },

    // Filtered years for the yearly view
    filteredYears() {
      if (!this.calculatorConfig.years.length) return [];

      let years = [];

      this.calculatorConfig.years.forEach(yearConfig => {
        if (!yearConfig.active) return;

        if (this.selectedYear !== 'all' && yearConfig.year !== this.selectedYear) return;

        const yearModules = this.moduleData.filter(m => m.year === yearConfig.year);

        // Sort modules based on selected sort method
        let sortedModules = [...yearModules];

        switch (this.sortMethod) {
          case 'name':
            sortedModules.sort((a, b) => a.name.localeCompare(b.name));
            break;
          case 'semester':
            sortedModules.sort((a, b) => (a.semester || 1) - (b.semester || 1));
            break;
          case 'score-asc':
            sortedModules.sort((a, b) => a.score - b.score);
            break;
          case 'score-desc':
            sortedModules.sort((a, b) => b.score - a.score);
            break;
          case 'credits':
            sortedModules.sort((a, b) => b.credits - a.credits);
            break;
        }

        const totalCredits = yearConfig.credits;
        const completedCredits = yearModules.reduce((sum, m) => sum + m.credits, 0);
        const average = yearModules.length ?
            Math.round(yearModules.reduce((sum, m) => sum + (m.score * m.credits), 0) /
                completedCredits * 10) / 10 : 0;

        years.push({
          year: yearConfig.year,
          average: average,
          completedCredits: completedCredits,
          totalCredits: totalCredits,
          weight: yearConfig.weight,
          modules: sortedModules
        });
      });

      return years;
    },

    // Get completed years count
    yearsCompleted() {
      return this.dashboardStats?.yearData?.length || 0;
    },

    // Generate semester options based on calculator config
    semesterOptions() {
      // Get the maximum number of semesters from calculator config
      let maxSemesters = 2; // Default to 2 semesters if not specified

      if (this.calculatorConfig && this.calculatorConfig.years && this.calculatorConfig.years.length > 0) {
        // Find maximum semesters in configuration
        const semestersArray = this.calculatorConfig.years
            .map(year => year.semesters || 0)
            .filter(s => s > 0);

        if (semestersArray.length > 0) {
          maxSemesters = Math.max(...semestersArray);
        }
      }

      // Generate options with label and value
      const options = [];
      for (let i = 1; i <= maxSemesters; i++) {
        options.push({
          label: `Semester ${i}`,
          value: i
        });
      }

      return options;
    }
  },
  watch: {
    // Watch for changes to the active view to update any necessary data
    activeView(newValue) {
      if (newValue === 'insights') {
        // Prepare data for insight charts when switching to insights tab
        this.prepareInsightsData();
      }
    },

    // Watch for numYears changes to update year weights
    'nextConfig.numYears': function(newValue) {
      if (newValue !== 'other' && newValue > 0) {
        this.initializeYearWeights(newValue);
      }
    },

    'nextConfig.customYears': function(newValue) {
      if (this.nextConfig.numYears === 'other' && newValue > 0) {
        this.initializeYearWeights(newValue);
      }
    }
  },
  async mounted() {
    await this.checkLoginAndFetchConfig();

    // Load modules and dashboard data
    await this.fetchModules();
    await this.fetchDashboardData();

    // Handle dark mode
    this.darkMode = getDarkModePreference();

    // Check for mobile
    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);

    // Try to load sidebar preference from localStorage
    const storedSidebarState = localStorage.getItem('sidebarVisible');
    if (storedSidebarState !== null) {
      this.sidebarVisible = storedSidebarState === 'true';
    }

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', this.onDarkModeChange);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
  },
  methods: {
    // API methods
    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_URL}/user/profile`, { withCredentials: true });
        this.userProfile = response.data;
        return response.data;
      } catch (error) {
        console.error("Error fetching user profile:", error);
        if (error.response && error.response.status === 401) {
          this.notLoggedIn = true;
        }
        return null;
      }
    },

    async fetchCalculatorConfig() {
      try {
        const response = await axios.get(`${API_URL}/calculator`, { withCredentials: true });
        this.calculatorConfig = response.data;
        return response.data;
      } catch (error) {
        console.error("Error fetching calculator config:", error);
        return null;
      }
    },

    async fetchModules() {
      try {
        this.loading = true;
        const response = await axios.get(`${API_URL}/modules`, { withCredentials: true });
        this.moduleData = response.data;
        this.prepareChartData();
        return response.data;
      } catch (error) {
        console.error("Error fetching modules:", error);
        return [];
      } finally {
        this.loading = false;
      }
    },

    async fetchDashboardData() {
      try {
        this.loading = true;
        const response = await axios.get(`${API_URL}/dashboard`, { withCredentials: true });
        const { stats, config } = response.data;

        this.dashboardStats = stats;
        this.dashboardConfig = config;

        // Load recent activities and goals from dashboard config
        this.recentActivities = config.recentActivities || [];
        this.goals = config.goals || [];

        // Prepare chart data
        this.yearData = stats.yearData || [];
        this.scoreDistribution = stats.gradeDistribution || [];

        return response.data;
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        return null;
      } finally {
        this.loading = false;
      }
    },

    async saveModule() {
      if (!this.isModuleFormValid) {
        notify({ type: "warning", message: "Please complete all required fields and ensure assessment weights total 100%." });
        return;
      }

      try {
        this.loading = true;

        // Calculate overall score based on assessments
        const totalScore = this.moduleForm.assessments.reduce((sum, assessment) => {
          return sum + (assessment.score * assessment.weight / 100);
        }, 0);

        this.moduleForm.score = Math.round(totalScore * 10) / 10;

        let response;
        if (this.editingModule) {
          // Update existing module
          response = await axios.put(
              `${API_URL}/modules/${this.moduleForm.id}`,
              this.moduleForm,
              { withCredentials: true }
          );
        } else {
          // Create new module
          response = await axios.post(
              `${API_URL}/modules`,
              this.moduleForm,
              { withCredentials: true }
          );
        }

        await this.fetchModules(); // Refresh module data
        await this.fetchDashboardData(); // Refresh dashboard stats

        notify({
          type: "success",
          message: `Module ${this.editingModule ? 'updated' : 'added'} successfully!`
        });

        this.showModuleForm = false;

        // Add activity to recent activities
        this.addActivity({
          type: 'grade',
          title: this.editingModule ? 'Module Updated' : 'Module Added',
          description: `${this.moduleForm.name}: ${this.moduleForm.score}%`,
          time: 'Just now'
        });
      } catch (error) {
        console.error("Error saving module:", error);
        notify({
          type: "error",
          message: `Failed to ${this.editingModule ? 'update' : 'add'} module: ${error.response?.data?.error || error.message}`
        });
      } finally {
        this.loading = false;
      }
    },

    async deleteModule(module) {
      if (confirm(`Are you sure you want to delete "${module.name}"?`)) {
        try {
          this.loading = true;
          await axios.delete(`${API_URL}/modules/${module.id}`, { withCredentials: true });

          await this.fetchModules(); // Refresh module data
          await this.fetchDashboardData(); // Refresh dashboard stats

          notify({ type: "success", message: "Module deleted successfully!" });
          this.showModuleDetail = false;

          // Add activity to recent activities
          this.addActivity({
            type: 'grade',
            title: 'Module Deleted',
            description: `${module.name}`,
            time: 'Just now'
          });
        } catch (error) {
          console.error("Error deleting module:", error);
          notify({
            type: "error",
            message: `Failed to delete module: ${error.response?.data?.error || error.message}`
          });
        } finally {
          this.loading = false;
        }
      }
    },

    async addActivity(activityData) {
      try {
        await axios.post(
            `${API_URL}/dashboard/activity`,
            activityData,
            { withCredentials: true }
        );

        // Update local activities
        if (!Array.isArray(this.recentActivities)) {
          this.recentActivities = [];
        }

        this.recentActivities.unshift(activityData);

        // Limit to 10 activities
        if (this.recentActivities.length > 10) {
          this.recentActivities = this.recentActivities.slice(0, 10);
        }
      } catch (error) {
        console.error("Error adding activity:", error);
      }
    },

    async updateGoals() {
      try {
        await axios.put(
            `${API_URL}/dashboard/goals`,
            this.goals,
            { withCredentials: true }
        );
      } catch (error) {
        console.error("Error updating goals:", error);
      }
    },

    async updateDashboardConfig(config) {
      try {
        await axios.put(
            `${API_URL}/dashboard`,
            config,
            { withCredentials: true }
        );
      } catch (error) {
        console.error("Error updating dashboard config:", error);
      }
    },

    async completeSetup() {
      // Validate weights before proceeding
      if (this.totalWeight !== 100 && this.hasActiveYears) {
        notify({
          type: "warning",
          message: "The total weight of active years should equal 100%.",
        });
        return;
      }

      try {
        this.loading = true;

        const yearsCount =
            this.nextConfig.numYears === "other" ? this.nextConfig.customYears : this.nextConfig.numYears;
        const semCount =
            this.nextConfig.semesters === "other"
                ? this.nextConfig.customSemesters
                : this.nextConfig.semesters;
        const credCount =
            this.nextConfig.credits === "other" ? this.nextConfig.customCredits : this.nextConfig.credits;

        // Create request payload for calculator config
        const configData = {
          numYears: yearsCount,
          semesters: semCount,
          credits: credCount,
          years: this.yearWeights.map((year, index) => ({
            year: `Year ${index + 1}`,
            active: year.active,
            credits: credCount,
            weight: year.weight,
            semesters: semCount
          }))
        };

        // Save calculator config
        await axios.put(
            `${API_URL}/calculator/update`,
            configData,
            { withCredentials: true }
        );

        // Save target grade in goals
        const targetValue = this.targetGrade === 'custom' ? this.customTargetGrade : this.targetGrade;
        const goals = [{
          title: 'First Class Degree',
          description: `Achieve overall average of ${targetValue}% or higher`,
          progress: 0,
          target_score: targetValue
        }];

        // Update goals
        await axios.put(
            `${API_URL}/dashboard/goals`,
            goals,
            { withCredentials: true }
        );

        // Save user configuration
        if (this.userConfig.academicLevel || this.userConfig.enrollmentType || this.userConfig.studyPreference) {
          await axios.put(
              `${API_URL}/user/config`,
              { studyPreferences: this.userConfig },
              { withCredentials: true }
          );
        }

        this.showYearWeights = false;
        this.showSetupWizard = false;
        this.showNextConfig = false;

        // Refresh data
        await this.fetchCalculatorConfig();
        await this.fetchModules();
        await this.fetchDashboardData();

        notify({ type: "success", message: "Setup completed successfully!" });
      } catch (error) {
        console.error("Error completing setup:", error);
        notify({
          type: "error",
          message: `Setup failed: ${error.response?.data?.error || error.message}`
        });
      } finally {
        this.loading = false;
      }
    },

    // Initialize year weights based on number of years
    initializeYearWeights(numYears) {
      // Create default distribution (equal weights for now)
      const defaultWeight = Math.floor(100 / numYears);
      const remainder = 100 - (defaultWeight * numYears);

      this.yearWeights = [];

      for (let i = 0; i < numYears; i++) {
        // Add remainder to last year if needed
        const weight = i === numYears - 1 ? defaultWeight + remainder : defaultWeight;
        this.yearWeights.push({
          year: i + 1,
          weight: weight,
          active: true
        });
      }
    },

    // Validate year weights to ensure they sum to 100%
    validateYearWeights() {
      // Cap individual weight values at 100
      this.yearWeights.forEach(year => {
        if (year.weight > 100) year.weight = 100;
        if (year.weight < 0) year.weight = 0;
      });

      // If only one active year, force it to 100%
      const activeYears = this.yearWeights.filter(y => y.active);
      if (activeYears.length === 1) {
        activeYears[0].weight = 100;
      }
    },

    // Check if user is logged in and fetch configuration
    async checkLoginAndFetchConfig() {
      try {
        // First try to get user profile to check if logged in
        const profile = await this.fetchUserProfile();

        if (!profile) {
          this.notLoggedIn = true;
          return;
        }

        // Fetch calculator config
        const calcConfig = await this.fetchCalculatorConfig();

        // Check if needs setup
        if (!calcConfig || !calcConfig.years || calcConfig.years.length === 0) {
          this.showSetupWizard = true;
        }
      } catch (error) {
        console.error("Error checking login and config:", error);
        this.notLoggedIn = true;
      }
    },

    // Save user config from wizard step 1
    saveUserConfig() {
      if (!this.userConfig.academicLevel || !this.userConfig.enrollmentType || !this.userConfig.studyPreference) {
        notify({ type: "warning", message: "Please complete all preference fields." });
        return;
      }

      // Move to next step
      this.showSetupWizard = false;
      this.showNextConfig = true;
    },

    // Go back to wizard step 1
    goBackToStep1() {
      this.showNextConfig = false;
      this.showSetupWizard = true;
    },

    // Go to year weights config
    goToYearWeights() {
      const yearsCount =
          this.nextConfig.numYears === "other" ? this.nextConfig.customYears : this.nextConfig.numYears;
      const semCount =
          this.nextConfig.semesters === "other"
              ? this.nextConfig.customSemesters
              : this.nextConfig.semesters;
      const credCount =
          this.nextConfig.credits === "other" ? this.nextConfig.customCredits : this.nextConfig.credits;

      if (!yearsCount || !semCount || !credCount) {
        notify({
          type: "warning",
          message: "Please fill all degree details (years, semesters, credits).",
        });
        return;
      }

      // Move to year weights step
      this.showNextConfig = false;
      this.showYearWeights = true;

      // Initialize year weights if not already done
      if (this.yearWeights.length === 0) {
        this.initializeYearWeights(yearsCount);
      }
    },

    // Go back to degree config
    goBackToDegreeConfig() {
      this.showYearWeights = false;
      this.showNextConfig = true;
    },

    // Toggle sidebar visibility
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
      // Save preference to localStorage
      localStorage.setItem('sidebarVisible', this.sidebarVisible);
    },

    // Handle dark mode change
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },

    // Handle logout event from navbar
    async handleLogout() {
      try {
        // Your logout API call here
        // await axios.post(`${API_URL}/logout`, {}, { withCredentials: true });
        this.notLoggedIn = true;
        this.$router.push('/login');
      } catch (error) {
        console.error("Error during logout:", error);
      }
    },

    // Check if device is mobile
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
      if (this.isMobile && this.sidebarVisible) {
        this.sidebarVisible = false;
        localStorage.setItem('sidebarVisible', 'false');
      }
    },

    // Get module icon class based on score
    getModuleIconClass(score) {
      if (score >= 70) return 'excellent';
      if (score >= 60) return 'good';
      if (score >= 50) return 'average';
      if (score >= 40) return 'pass';
      return 'fail';
    },

    // Get score class based on value
    getScoreClass(score) {
      if (score >= 70) return 'excellent-score';
      if (score >= 60) return 'good-score';
      if (score >= 50) return 'average-score';
      if (score >= 40) return 'pass-score';
      return 'fail-score';
    },

    // Get comparison class for difference values
    getComparisonClass(value) {
      if (value > 5) return 'positive-large';
      if (value > 0) return 'positive-small';
      if (value < -5) return 'negative-large';
      if (value < 0) return 'negative-small';
      return 'neutral';
    },

    // View module details
    viewModuleDetails(module) {
      this.selectedModule = module;
      this.showModuleDetail = true;
    },

    // Show add module form
    showAddModuleForm(year) {
      this.editingModule = false;
      this.moduleForm = {
        name: '',
        code: '',
        credits: 15,
        year: year.year,
        semester: 1, // Default to semester 1
        score: 0,
        assessments: [
          { name: 'Exam', weight: 100, score: 0 }
        ]
      };
      this.showModuleForm = true;
    },

    // Edit module
    editModule(module) {
      this.editingModule = true;
      this.moduleForm = JSON.parse(JSON.stringify(module));

      // If the module doesn't have a semester field yet, default to 1
      if (this.moduleForm.semester === undefined) {
        this.moduleForm.semester = 1;
      }

      // Ensure assessments array exists
      if (!this.moduleForm.assessments || !this.moduleForm.assessments.length) {
        this.moduleForm.assessments = [
          { name: 'Exam', weight: 100, score: module.score }
        ];
      }

      this.showModuleDetail = false;
      this.showModuleForm = true;
    },

    // Add assessment to module form
    addAssessment() {
      this.moduleForm.assessments.push({
        name: `Assessment ${this.moduleForm.assessments.length + 1}`,
        weight: 0,
        score: 0
      });
    },

    // Remove assessment from module form
    removeAssessment(index) {
      this.moduleForm.assessments.splice(index, 1);
    },

    // Export grades to CSV
    exportGrades() {
      // Create CSV content
      let csv = 'Year,Module,Code,Credits,Semester,Score\n';

      this.moduleData.forEach(module => {
        csv += `${module.year},${module.name},${module.code || ''},${module.credits},${module.semester || 1},${module.score}\n`;
      });

      // Create download link
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', 'GradeGuard_Export.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      notify({ type: "success", message: "Grades exported successfully!" });
    },

    // Prepare data for charts
    prepareChartData() {
      // Year data for year comparison chart will be from API

      // Score distribution for charts
      const scores = this.moduleData.map(m => m.score);
      const ranges = [
        { name: '0-39%', range: [0, 39] },
        { name: '40-49%', range: [40, 49] },
        { name: '50-59%', range: [50, 59] },
        { name: '60-69%', range: [60, 69] },
        { name: '70-100%', range: [70, 100] }
      ];

      this.scoreDistribution = ranges.map(range => {
        return {
          name: range.name,
          count: scores.filter(score => score >= range.range[0] && score <= range.range[1]).length
        };
      });
    },

    // Prepare data for insights charts
    prepareInsightsData() {
      // Performance data for line chart
      const modulesByYear = {};

      this.moduleData.forEach(module => {
        if (!modulesByYear[module.year]) {
          modulesByYear[module.year] = [];
        }
        modulesByYear[module.year].push(module);
      });

      this.performanceData = Object.keys(modulesByYear).map(year => {
        const modules = modulesByYear[year];
        return {
          name: year,
          average: Math.round(modules.reduce((sum, m) => sum + m.score, 0) / modules.length * 10) / 10,
          highest: Math.max(...modules.map(m => m.score)),
          lowest: Math.min(...modules.map(m => m.score)),
          count: modules.length
        };
      }).sort((a, b) => {
        return parseInt(a.name.replace('Year ', '')) - parseInt(b.name.replace('Year ', ''));
      });

      // Strengths data for radar chart
      const subjectCategories = [
        { name: 'Programming', pattern: /(programming|coding|development|software)/i },
        { name: 'Theory', pattern: /(theory|concepts|foundations)/i },
        { name: 'Mathematics', pattern: /(math|mathematics|calculation|statistics)/i },
        { name: 'Design', pattern: /(design|architecture|interface)/i },
        { name: 'Research', pattern: /(research|analysis|thesis)/i },
        { name: 'Security', pattern: /(security|cyber|protection)/i }
      ];

      this.strengthsData = subjectCategories.map(category => {
        const matchingModules = this.moduleData.filter(m =>
            category.pattern.test(m.name) || category.pattern.test(m.code)
        );

        return {
          subject: category.name,
          score: matchingModules.length ?
              Math.round(matchingModules.reduce((sum, m) => sum + m.score, 0) / matchingModules.length) :
              50 // Default value if no matching modules
        };
      });

      // Generate personalized tips
      this.generatePersonalizedTips();
    },

    // Generate personalized tips based on module data
    generatePersonalizedTips() {
      const tips = [];

      // Find lowest scoring module
      if (this.moduleData.length > 0) {
        const sortedByScore = [...this.moduleData].sort((a, b) => a.score - b.score);
        const lowestModule = sortedByScore[0];

        if (lowestModule.score < 50) {
          tips.push({
            title: `Focus on ${lowestModule.name}`,
            description: `This is your lowest scoring module (${lowestModule.score}%). Consider allocating more study time to improve your understanding of key concepts.`
          });
        }
      }

      // Find strongest subject area
      if (this.strengthsData.length > 0) {
        const sortedStrengths = [...this.strengthsData].sort((a, b) => b.score - a.score);
        const topStrength = sortedStrengths[0];

        tips.push({
          title: `Maintain Strong Performance`,
          description: `You're excelling in ${topStrength.subject} modules. Keep up the good work and consider peer tutoring to reinforce your knowledge.`
        });
      }

      // Add general tip
      tips.push({
        title: 'Balance Your Workload',
        description: 'Try spacing out your work to reduce stress and improve quality. Setting regular study periods can help maintain consistent progress.'
      });

      this.personalizedTips = tips;
    }
  }
};
</script>

<style scoped>
/* ========== Base Dashboard Styles ========== */
.dashboard {
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

/* ========== Main Content Styles ========== */
.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all var(--transition-speed) ease;
}

.dashboard-main-content.expanded {
  margin-right: 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-dark);
  margin: 0;
}

body.dark-mode .dashboard-header h1 {
  color: var(--primary-light);
}

/* ========== View Controls ========== */
.view-controls {
  display: flex;
  gap: 0.5rem;
  background: var(--bg-card);
  border-radius: 24px;
  padding: 0.25rem;
  box-shadow: var(--shadow-sm);
}

.view-controls button {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.view-controls button.active {
  background: var(--primary-color);
  color: white;
}

.view-controls button:hover:not(.active) {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

/* ========== Sidebar Toggle Buttons ========== */
.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  z-index: 50; /* Increased z-index to ensure button is above other elements */
}

.toggle-text {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-toggle:hover {
  background-color: var(--primary-dark);
  transform: scale(1.05);
}

.sidebar-show-button {
  position: fixed;
  right: 2rem;
  top: 6rem;
  box-shadow: 0 2px 10px rgba(123, 73, 255, 0.3);
  z-index: 100; /* Higher z-index to ensure it's visible */
}

.sidebar-hide-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 20;
}

/* ========== Sidebar Styles ========== */
.dashboard-sidebar {
  width: 320px;
  background-color: var(--bg-card);
  border-left: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
}

/* Slide transition for sidebar */
.slide-enter-active,
.slide-leave-active {
  transition: transform var(--transition-speed) ease,
  opacity var(--transition-speed) ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* ========== Center Content Container ========== */
.center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

/* ========== Authentication Prompt ========== */
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

/* ========== Wizard Styles ========== */
.wizard-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-md);
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
  transition: all var(--transition-speed) ease;
}

.wizard-header {
  text-align: center;
  margin-bottom: 2rem;
}

.step-indicator {
  display: inline-block;
  background-color: var(--primary-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.wizard-header h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.wizard-header p {
  margin: 0;
  color: var(--text-secondary);
}

/* ========== Form Styling ========== */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

.required {
  color: #e74c3c;
}

.form-group input[type="number"],
.form-group input[type="text"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  transition: border-color var(--transition-speed) ease;
}

.form-group input[type="number"]:focus,
.form-group input[type="text"]:focus {
  border-color: var(--primary-color);
  outline: none;
}

.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px;
}

.form-group select:focus {
  border-color: var(--primary-color);
  outline: none;
}

.select-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 1rem;
}

.select-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 2px solid var(--primary-color);
  background: transparent;
  color: var(--primary-color);
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.select-btn:hover {
  background: rgba(123, 73, 255, 0.1);
}

.select-btn.active {
  background: var(--primary-color);
  color: white;
}

.btn-icon {
  font-size: 1.1rem;
}

/* ========== Year Weights Styles ========== */
.year-weights-container {
  margin-bottom: 2rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.year-weights-header {
  display: flex;
  background-color: var(--bg-accent);
  padding: 0.75rem;
  font-weight: 600;
  border-bottom: 1px solid var(--border-color);
}

.year-weight-row {
  display: flex;
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color-light);
}

.year-weight-row:last-child {
  border-bottom: none;
}

.year-column {
  flex: 1;
  display: flex;
  align-items: center;
}

.weight-column {
  flex: 1;
  display: flex;
  align-items: center;
}

.weight-column input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-input);
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
  height: 24px;
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
  border-radius: 24px;
  transition: .4s;
}

.toggle-switch:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  border-radius: 50%;
  transition: .4s;
}

input:checked + .toggle-switch {
  background-color: var(--primary-color);
}

input:checked + .toggle-switch:before {
  transform: translateX(26px);
}

.total-weight {
  padding: 0.75rem;
  text-align: right;
  font-weight: 600;
  background-color: var(--bg-accent);
  border-top: 1px solid var(--border-color);
}

.weight-error {
  color: var(--warning-color);
}

/* ========== Button Styling ========== */
.save-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

.save-button:disabled {
  background-color: var(--text-muted);
  cursor: not-allowed;
  transform: none;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  background-color: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: rgba(123, 73, 255, 0.1);
}

/* ========== Dashboard Overview Tab ========== */
.dashboard-overview {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.overview-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.overview-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.time-filters {
  display: flex;
  gap: 0.5rem;
}

.time-filters button {
  padding: 0.35rem 0.75rem;
  border: none;
  background: transparent;
  color: var(--text-muted);
  border-radius: 16px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.time-filters button.active {
  background: var(--primary-color);
  color: white;
}

.time-filters button:hover:not(.active) {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.overview-body {
  padding: 1.5rem;
}

.grade-summary {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.grade-circle {
  position: relative;
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: conic-gradient(
      var(--primary-color) 0deg,
      var(--primary-color) calc(var(--percent) * 360deg),
      var(--bg-accent) calc(var(--percent) * 360deg),
      var(--bg-accent) 360deg
  );
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.grade-circle::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border-radius: 50%;
  background: var(--bg-card);
  box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.1);
}

.grade-value {
  position: relative;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-dark);
}

.grade-label {
  position: relative;
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.grade-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
}

.stats-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.stats-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.stats-value {
  font-weight: 600;
  color: var(--primary-dark);
}

/* ========== Progress Section ========== */
.progress-section {
  margin-top: 2rem;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.progress-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.progress-legend {
  display: flex;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.progress-bar {
  display: flex;
  height: 2.5rem;
  border-radius: var(--border-radius);
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.progress-segment {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.progress-segment.achieved {
  background-color: #2ecc71;
}

.progress-segment.lost {
  background-color: #3498db;
}

.progress-segment.remaining {
  background-color: #ecf0f1;
  color: var(--text-secondary);
}

.progress-targets {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.target-item {
  flex: 1;
  text-align: center;
  padding: 1rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
}

.target-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 0.5rem;
}

.target-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* ========== Visualization Row ========== */
.visualization-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.chart-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.chart-card h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-container {
  height: 300px;
  position: relative;
}

.large-chart .chart-container {
  height: 350px;
}

/* ========== Bottom Row ========== */
.bottom-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;
}

/* ========== Activity Card ========== */
.activity-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.activity-card h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  background: var(--bg-accent);
  transition: all 0.2s ease;
}

.activity-item:hover {
  transform: translateX(5px);
}

.activity-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.activity-icon.grade {
  background: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
}

.activity-icon.submission {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.activity-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.activity-time {
  font-size: 0.75rem;
  color: var(--text-muted);
  white-space: nowrap;
}

/* ========== Goals Card ========== */
.goals-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.goals-card h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.goals-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  background: var(--bg-accent);
}

.goal-progress {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.goal-circle {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.goal-circle-bg {
  fill: none;
  stroke: var(--border-color);
  stroke-width: 2.5;
}

.goal-circle-progress {
  fill: none;
  stroke: var(--primary-color);
  stroke-width: 2.5;
  stroke-linecap: round;
}

.goal-percentage {
  font-size: 10px;
  fill: var(--primary-dark);
  text-anchor: middle;
  dominant-baseline: middle;
  transform: rotate(90deg);
}

.goal-details {
  flex: 1;
}

.goal-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.goal-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* ========== Yearly View Tab ========== */
.yearly-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========== Filters Row ========== */
.filters-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1rem 1.5rem;
  box-shadow: var(--shadow-md);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-group label {
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
}

.export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.export-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

/* ========== Year Card ========== */
.year-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  margin-bottom: 2rem;
}

.year-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.year-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.year-stats {
  display: flex;
  gap: 1.5rem;
}

.year-stat {
  text-align: center;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary-dark);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

/* ========== Year Progress ========== */
.year-progress {
  margin-bottom: 1.5rem;
}

.year-progress-bar {
  height: 1.5rem;
  background-color: var(--bg-accent);
}

.progress-value {
  height: 100%;
  background: linear-gradient(to right, #3498db, var(--primary-color));
  color: white;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.75rem;
  font-weight: 600;
  font-size: 0.85rem;
  transition: width 0.5s ease;
}

/* ========== Modules Grid ========== */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.module-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
  cursor: pointer;
}

.module-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-sm);
}

.module-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  font-weight: 600;
  color: white;
  background: var(--primary-color);
}

.module-icon.excellent {
  background: #2ecc71;
}

.module-icon.good {
  background: #3498db;
}

.module-icon.average {
  background: #f1c40f;
}

.module-icon.pass {
  background: #e67e22;
}

.module-icon.fail {
  background: #e74c3c;
}

.module-details {
  flex: 1;
}

.module-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.module-info {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.module-score {
  font-size: 1.2rem;
  font-weight: 700;
}

.excellent-score {
  color: #2ecc71;
}

.good-score {
  color: #3498db;
}

.average-score {
  color: #f1c40f;
}

.pass-score {
  color: #e67e22;
}

.fail-score {
  color: #e74c3c;
}

/* ========== Add Module Button ========== */
.add-module-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  background: transparent;
  color: var(--primary-color);
  border: 2px dashed var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.add-module-button:hover {
  background: rgba(123, 73, 255, 0.05);
  transform: scale(1.05);
}

/* ========== Insights Tab ========== */
.insights-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========== Insights Card ========== */
.insights-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.insights-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.insight-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.metric-item {
  text-align: center;
  padding: 1.5rem 1rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
}

.metric-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-sm);
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.metric-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.metric-comparison {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.metric-comparison svg {
  vertical-align: middle;
  margin-right: 0.25rem;
}

.positive-large {
  color: #27ae60;
}

.positive-small {
  color: #2ecc71;
}

.negative-large {
  color: #c0392b;
}

.negative-small {
  color: #e74c3c;
}

.neutral {
  color: var(--text-secondary);
}

/* ========== Insights Charts ========== */
.insights-charts {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.small-charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

/* ========== Insights Tips ========== */
.insights-tips {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.tips-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.tip-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
}

.tip-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-sm);
}

.tip-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
  flex-shrink: 0;
}

.tip-content h4 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.tip-content p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* ========== Prediction Scenarios ========== */
.insights-prediction {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.prediction-scenarios {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.scenario-card {
  text-align: center;
  padding: 1.5rem;
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
}

.scenario-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-sm);
}

.scenario-card.best {
  background: rgba(46, 204, 113, 0.1);
  border: 1px solid rgba(46, 204, 113, 0.3);
}

.scenario-card.expected {
  background: rgba(52, 152, 219, 0.1);
  border: 1px solid rgba(52, 152, 219, 0.3);
}

.scenario-card.minimum {
  background: rgba(241, 196, 15, 0.1);
  border: 1px solid rgba(241, 196, 15, 0.3);
}

.scenario-card h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.scenario-grade {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 1rem;
}

.scenario-card.best .scenario-grade {
  color: #27ae60;
}

.scenario-card.expected .scenario-grade {
  color: #2980b9;
}

.scenario-card.minimum .scenario-grade {
  color: #d35400;
}

.scenario-card p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* ========== Module Detail Dialog ========== */
.module-detail-dialog,
.module-form-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.dialog-content {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.dialog-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-dark);
}

.close-dialog {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-dialog:hover {
  background: var(--bg-accent);
  color: var(--text-primary);
}

.module-info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1.5rem;
}

.info-item {
  background: var(--bg-accent);
  padding: 1rem;
  border-radius: var(--border-radius);
  text-align: center;
}

.info-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.info-value {
  font-weight: 600;
  color: var(--text-primary);
}

.info-value.score {
  font-size: 1.25rem;
  font-weight: 700;
}

.dialog-content h3 {
  margin: 0;
  padding: 0 1.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.assessments-table {
  padding: 1.5rem;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
}

.table-header {
  font-weight: 600;
  color: var(--text-primary);
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 0.75rem;
}

.table-row {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color-light);
  align-items: center;
}

.table-row:last-child {
  border-bottom: none;
}

.table-cell {
  padding: 0.5rem 0;
}

.module-charts {
  padding: 1.5rem;
}

.module-chart {
  margin-bottom: 1.5rem;
}

.module-chart h4 {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.edit-button,
.delete-button,
.cancel-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-button {
  background: var(--primary-color);
  color: white;
  border: none;
}

.edit-button:hover {
  background: var(--primary-dark);
}

.delete-button {
  background: transparent;
  color: #e74c3c;
  border: 1px solid #e74c3c;
}

.delete-button:hover {
  background: rgba(231, 76, 60, 0.1);
}

.cancel-button {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-button:hover {
  background: var(--bg-accent);
}

/* ========== Module Form ========== */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
}

.assessments-form {
  padding: 1.5rem;
}

.assessment-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.assessment-inputs {
  flex: 1;
  display: flex;
  gap: 1rem;
}

.assessment-inputs input[type="text"] {
  flex: 2;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-input);
  color: var(--text-primary);
}

.assessment-numbers {
  flex: 1;
  display: flex;
  gap: 0.5rem;
}

.assessment-numbers input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-input);
  color: var(--text-primary);
}

.remove-assessment {
  background: transparent;
  border: none;
  color: #e74c3c;
  padding: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.remove-assessment:hover {
  transform: scale(1.1);
}

.add-assessment {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem 1.25rem;
  background: transparent;
  color: var(--primary-color);
  border: 1px dashed var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.add-assessment:hover {
  background: rgba(123, 73, 255, 0.05);
}

.total-weight-indicator {
  padding: 0 1.5rem 1.5rem;
  text-align: right;
  font-weight: 500;
  color: var(--success-color);
}

.total-weight-indicator.weight-error {
  color: var(--warning-color);
}

/* ========== Responsive adjustments ========== */
@media (max-width: 1200px) {
  .insight-metrics {
    grid-template-columns: repeat(2, 1fr);
  }

  .visualization-row {
    grid-template-columns: 1fr;
  }

  .small-charts {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 992px) {
  .bottom-row {
    grid-template-columns: 1fr;
  }

  .prediction-scenarios {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-layout {
    flex-direction: column;
    padding-top: 60px; /* Smaller navbar height */
  }

  .dashboard-main-content {
    padding: 1.5rem;
  }

  .dashboard-sidebar {
    width: 100%;
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 100;
    border-radius: 0;
    border-left: none;
  }

  .sidebar-hide-button {
    top: 1rem;
    right: 1rem;
  }

  .sidebar-show-button {
    right: 1rem;
    bottom: 1rem;
    top: auto;
  }

  .grade-summary {
    flex-direction: column;
    align-items: center;
    gap: 2rem;
  }

  .modules-grid {
    grid-template-columns: 1fr;
  }

  .filters-row {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .module-info-grid {
    grid-template-columns: 1fr 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .assessment-inputs {
    flex-direction: column;
  }

  .table-header,
  .table-row {
    grid-template-columns: 2fr 1fr;
  }

  .table-cell:nth-child(3),
  .table-cell:nth-child(4) {
    display: none;
  }

  .slide-enter-from,
  .slide-leave-to {
    transform: translateY(100%);
  }

  .button-group {
    flex-direction: column;
  }

  .year-weights-container {
    font-size: 0.9rem;
  }

  .year-weights-header,
  .year-weight-row {
    padding: 0.5rem;
  }

  .weight-column input {
    width: 60px;
    padding: 0.4rem;
  }
}

/* Small screen adjustments */
@media (max-width: 480px) {
  .dashboard-layout,
  .dashboard-main-content {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .select-group {
    flex-direction: column;
    align-items: stretch;
  }

  .select-btn {
    width: 100%;
    justify-content: center;
  }

  .module-detail-dialog,
  .module-form-dialog {
    padding: 1rem;
  }

  .module-info-grid {
    grid-template-columns: 1fr;
  }

  .progress-targets {
    flex-direction: column;
  }

  .insight-metrics {
    grid-template-columns: 1fr;
  }
}
</style>