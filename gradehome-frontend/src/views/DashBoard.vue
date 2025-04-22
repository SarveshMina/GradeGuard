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
      <!-- Floating collapse button that appears when sidebar is hidden -->
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
          <!-- Prominent Add Module Button -->

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
                  <GradeDistributionChart :moduleData="completedModuleData" />
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
                  <option value="status">Enrollment Status</option>
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
                    <div class="module-name">
                      {{ module.name }}
                      <span v-if="module.isCurrentlyEnrolled" class="enrolled-badge">Current</span>
                    </div>
                    <div class="module-info">{{ module.credits }} credits | {{ module.semester === 0 ? 'Full Year' : `Semester ${module.semester || 1}` }}</div>
                  </div>
                  <div class="module-score" :class="getScoreClass(module.score)">
                    {{ module.isCurrentlyEnrolled ? 'In Progress' : `${module.score}%` }}
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
                <div class="metric-item" v-tooltip="'This compares your current average (excluding ongoing modules) with your target grade'">
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

                <div class="metric-item" v-tooltip="'Calculated based on how accurately your previous performance predicted your next results. Higher accuracy means more reliable future predictions.'">
                  <div class="metric-value">{{ predictionAccuracy }}%</div>
                  <div class="metric-label">Prediction Accuracy</div>
                  <div class="metric-comparison">
                    Based on past performance patterns
                  </div>
                </div>

                <div class="metric-item" v-tooltip="'Measures how consistent your scores are across all modules. Higher consistency (closer to 100%) means your performance is stable, while lower scores indicate variability. Variance shows the difference between your highest and lowest scores.'">
                  <div class="metric-value">{{ consistencyScore }}%</div>
                  <div class="metric-label">Consistency Score</div>
                  <div class="metric-comparison">
                    Variance: {{ performanceVariance }}%
                  </div>
                </div>

                <div class="metric-item" v-tooltip="'Shows how much your performance has improved over time. Calculated as the percentage change between your earliest and latest completed modules.'">
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
                <div class="scenario-card best" v-tooltip="'This scenario represents the best possible outcome based on your top performances in previous modules.'">
                  <h3>Best Case</h3>
                  <div class="scenario-grade">{{ bestCaseGrade }}%</div>
                  <p>Based on your top performance in similar modules</p>
                </div>

                <div class="scenario-card expected" v-tooltip="'This represents the most likely outcome based on your average performance and current trend.'">
                  <h3>Expected</h3>
                  <div class="scenario-grade">{{ expectedGrade }}%</div>
                  <p>Based on your average performance pattern</p>
                </div>

                <div class="scenario-card minimum" v-tooltip="'This is the minimum grade needed to maintain your current degree classification.'">
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
                  <div class="info-value">{{ selectedModule.semester === 0 ? 'Full Academic Year' : `Semester ${selectedModule.semester || 1}` }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">Overall Score</div>
                  <div class="info-value score" :class="getScoreClass(selectedModule.score)">
                    {{ selectedModule.isCurrentlyEnrolled ? 'In Progress' : `${selectedModule.score}%` }}
                  </div>
                </div>
                <!-- New enrollment status display -->
                <div class="info-item">
                  <div class="info-label">Status</div>
                  <div class="info-value">
                    <span class="enrollment-status" :class="{ 'active': selectedModule.isCurrentlyEnrolled }">
                      {{ selectedModule.isCurrentlyEnrolled ? 'Currently Enrolled' : 'Completed' }}
                    </span>
                  </div>
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

                <!-- Semester field -->
                <div class="form-group">
                  <label for="moduleSemester">Semester <span class="required">*</span></label>
                  <select id="moduleSemester" v-model="moduleForm.semester">
                    <option v-for="option in semesterOptions" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>

                <!-- New Currently Enrolled field -->
                <div class="form-group enrollment-checkbox">
                  <label class="checkbox-container">
                    <input type="checkbox" id="moduleEnrolled" v-model="moduleForm.isCurrentlyEnrolled">
                    <span class="checkbox-label">Currently Enrolled</span>
                  </label>
                  <div class="field-hint">Check this if you are taking this module this semester</div>
                </div>
              </div>

              <h3>Assessments</h3>
              <div class="assessments-form">
                <div v-for="(assessment, index) in moduleForm.assessments" :key="index" class="assessment-row">
                  <div class="assessment-inputs">
                    <input type="text" v-model="assessment.name" placeholder="Assessment name">
                    <div class="assessment-numbers">
                      <input type="number" v-model.number="assessment.weight" min="0" max="100" placeholder="Weight %">
                      <input type="number"
                             v-model.number="assessment.score"
                             min="0"
                             max="100"
                             placeholder="Score %"
                             :disabled="moduleForm.isCurrentlyEnrolled && !assessment.completed">
                    </div>
                  </div>
                  <div v-if="moduleForm.isCurrentlyEnrolled" class="assessment-status">
                    <label class="checkbox-container">
                      <input type="checkbox" v-model="assessment.completed">
                      <span class="checkbox-label">Completed</span>
                    </label>
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
import { userSettingsService } from "@/services/userSettingsService.js"; // Import userSettingsService
import { API_URL } from "@/config.js";

// Import chart components
import GradeDistributionChart from "@/components/charts/GradeDistributionChart.vue";
import YearComparisonChart from "@/components/charts/YearComparisonChart.vue";
import PerformanceChart from "@/components/charts/PerformanceChart.vue";
import StrengthsRadarChart from "@/components/charts/StrengthsRadarChart.vue";
import ModuleComparisonChart from "@/components/charts/ModuleComparisonChart.vue";

// Import tooltip directive
import VTooltip from 'v-tooltip';

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
  directives: {
    tooltip: VTooltip.VTooltip
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
        isCurrentlyEnrolled: false, // New property for enrollment status
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
      personalizedTips: [],

      // Settings-related data from userSettingsService
      settings: {
        appearance: {
          accentColor: 'purple',
          fontSize: 'medium',
          highContrast: false,
          enableAnimations: true
        },
        academic: {
          academicLevel: 'Undergraduate',
          enrollmentType: 'Full time',
          studyPreferences: ['Mornings'],
          currentYear: 1,
          totalYears: 3,
          semestersPerYear: 2,
          creditsPerYear: 120,
          targetGrade: 70,
          gradingScale: [
            {letter: 'A', minPercentage: 70, gpaValue: 4.0},
            {letter: 'B', minPercentage: 60, gpaValue: 3.0},
            {letter: 'C', minPercentage: 50, gpaValue: 2.0},
            {letter: 'D', minPercentage: 40, gpaValue: 1.0},
            {letter: 'F', minPercentage: 0, gpaValue: 0.0}
          ],
          yearWeights: []
        },
        accessibility: {
          colorBlindMode: 'none',
          screenReaderOptimized: false,
          reduceMotion: false,
          motionIntensity: 75,
          keyboardShortcuts: true,
          focusMode: false,
          textToSpeech: false
        },
        calendar: {
          firstDayOfWeek: 'sunday',
          defaultEventDuration: 60,
          defaultEventType: 'general',
          timeFormat: '12h',
          dateFormat: 'MM/DD/YYYY',
          showWeekNumbers: false,
          showCompleted: true,
          highlightToday: true,
          defaultView: 'month'
        }
      }
    };
  },
  computed: {
    // Get completed and in-progress modules
    completedModuleData() {
      return this.moduleData.filter(m => !m.isCurrentlyEnrolled);
    },

    currentModuleData() {
      return this.moduleData.filter(m => m.isCurrentlyEnrolled);
    },

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

    // Get overall average across all years (excluding currently enrolled modules)
    overallAverage() {
      // Always calculate manually excluding currently enrolled modules
      // Don't rely on the backend stats as they might include currently enrolled modules
      const completedModules = this.completedModuleData;
      if (!completedModules || completedModules.length === 0) return 0;

      const totalCredits = completedModules.reduce((sum, m) => sum + m.credits, 0);
      const weightedSum = completedModules.reduce((sum, m) => sum + (m.score * m.credits), 0);

      return totalCredits > 0 ? Math.round((weightedSum / totalCredits) * 10) / 10 : 0;
    },

    // Get current yearly average (excluding currently enrolled modules)
    yearlyAverage() {
      // Always calculate manually for the latest year to ensure in-progress modules are excluded
      // First get the latest year from completed modules
      const latestYear = [...this.completedModuleData]
          .sort((a, b) => {
            const yearA = parseInt(a.year.replace('Year ', ''));
            const yearB = parseInt(b.year.replace('Year ', ''));
            return yearB - yearA;
          })[0];

      if (!latestYear) return 0;

      const latestYearModules = this.completedModuleData.filter(m => m.year === latestYear.year);
      const totalCredits = latestYearModules.reduce((sum, m) => sum + m.credits, 0);
      const weightedSum = latestYearModules.reduce((sum, m) => sum + (m.score * m.credits), 0);

      return totalCredits > 0 ? Math.round((weightedSum / totalCredits) * 10) / 10 : 0;
    },

    // Get completed and total credits
    completedCredits() {
      return this.completedModuleData.reduce((sum, m) => sum + m.credits, 0);
    },

    totalCredits() {
      return this.dashboardStats?.totalCredits ||
          this.moduleData.reduce((sum, m) => sum + m.credits, 0);
    },

    // Get top module (only from completed modules)
    topModule() {
      if (this.dashboardStats?.topModule) {
        return this.dashboardStats.topModule;
      }

      if (this.completedModuleData.length === 0) return {name: 'N/A', score: 0};

      return this.completedModuleData.reduce((top, module) => {
        return (module.score > top.score) ? module : top;
      }, {name: 'N/A', score: 0});
    },

    // Get progress percentages
    achievedPercentage() {
      const completedModules = this.completedModuleData;
      const totalPossible = completedModules.reduce((sum, m) => sum + (m.credits * 100), 0);
      const achieved = completedModules.reduce((sum, m) => sum + (m.score * m.credits), 0);

      return totalPossible > 0 ? Math.round((achieved / totalPossible) * 100) : 0;
    },

    lostPercentage() {
      const completedCredits = this.completedCredits;
      const totalCredits = this.totalCredits;

      if (totalCredits === 0) return 0;

      return Math.round((completedCredits / totalCredits * 100) - this.achievedPercentage);
    },

    remainingPercentage() {
      const completedCredits = this.completedCredits;
      const totalCredits = this.totalCredits;

      if (totalCredits === 0) return 100;

      return Math.round(100 - (completedCredits / totalCredits * 100));
    },

    // Get target grades needed for different classifications based on settings or defaults
    targetHighGrade() {
      if (this.dashboardStats?.targetHighGrade) return this.dashboardStats.targetHighGrade;

      // Calculate based on academic settings if available
      const gradingScale = this.settings.academic.gradingScale || [];
      const firstClass = gradingScale.find(g => g.letter === 'A') || {minPercentage: 70};
      return firstClass.minPercentage;
    },

    targetMediumGrade() {
      if (this.dashboardStats?.targetMediumGrade) return this.dashboardStats.targetMediumGrade;

      // Calculate based on academic settings if available
      const gradingScale = this.settings.academic.gradingScale || [];
      const upperSecond = gradingScale.find(g => g.letter === 'B') || {minPercentage: 60};
      return upperSecond.minPercentage;
    },

    targetLowGrade() {
      if (this.dashboardStats?.targetLowGrade) return this.dashboardStats.targetLowGrade;

      // Calculate based on academic settings if available
      const gradingScale = this.settings.academic.gradingScale || [];
      const lowerSecond = gradingScale.find(g => g.letter === 'C') || {minPercentage: 50};
      return lowerSecond.minPercentage;
    },

    // Insights tab calculations
    averageVsTarget() {
      // Comparing current average to personal target from settings
      const targetGradeValue = this.settings.academic.targetGrade === 'custom' ?
          this.settings.academic.customTargetGrade :
          this.settings.academic.targetGrade || 70;

      return Math.round((this.overallAverage - targetGradeValue) * 10) / 10;
    },

    predictionAccuracy() {
      return 87; // Could be calculated from actual data in the future
    },

    consistencyScore() {
      // Calculate consistency based on standard deviation of scores
      const completedModules = this.completedModuleData;
      if (completedModules.length < 2) return 100;

      const scores = completedModules.map(m => m.score);
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
      const completedModules = this.completedModuleData;
      if (completedModules.length < 2) return 0;

      const scores = completedModules.map(m => m.score);
      const highest = Math.max(...scores);
      const lowest = Math.min(...scores);

      return Math.round((highest - lowest) * 10) / 10;
    },

    improvementRate() {
      // Calculate improvement rate between earliest and latest modules
      const completedModules = this.completedModuleData;
      if (completedModules.length < 2) return 0;

      // Sort modules by year (assuming format "Year X")
      const sortedModules = [...completedModules].sort((a, b) => {
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
      const completedCredits = this.completedCredits;
      const totalCredits = this.totalCredits;

      if (totalCredits === 0) return 0;

      const remainingWeight = 100 - Math.round(completedCredits / totalCredits * 100);
      const bestRemainingScore = 95; // Assuming 95% is reasonable "best case"

      return Math.min(100, Math.round((this.overallAverage * (100 - remainingWeight) / 100) +
          (bestRemainingScore * remainingWeight / 100)));
    },

    expectedGrade() {
      // Based on current trend
      return Math.min(100, Math.round(this.overallAverage + (this.improvementRate > 0 ? this.improvementRate / 10 : 0)));
    },

    minimumGrade() {
      // Use grading scale from settings to determine minimum needed grade
      const gradingScale = this.settings.academic.gradingScale || [];
      const passGrade = gradingScale.find(g => g.letter === 'D')?.minPercentage || 40;

      // Minimum needed to maintain classification
      const currentAverage = this.overallAverage;
      const potentialThresholds = gradingScale
          .map(g => g.minPercentage)
          .filter(threshold => threshold <= currentAverage)
          .sort((a, b) => b - a);

      return potentialThresholds[0] || passGrade;
    },

    // Filtered years for the yearly view
    filteredYears() {
      if (!this.calculatorConfig || !this.calculatorConfig.years || !this.calculatorConfig.years.length) {
        console.log("No years configured in calculator config");
        return [];
      }

      console.log("Calculator config years:", this.calculatorConfig.years);
      console.log("Selected year:", this.selectedYear);
      console.log("Module data count:", this.moduleData?.length || 0);

      let years = [];

      this.calculatorConfig.years.forEach(yearConfig => {
        if (!yearConfig.active) {
          console.log(`Skipping inactive year: ${yearConfig.year}`);
          return;
        }

        if (this.selectedYear !== 'all' && yearConfig.year !== this.selectedYear) {
          console.log(`Skipping year ${yearConfig.year} - not matching selected year ${this.selectedYear}`);
          return;
        }

        const yearModules = this.moduleData.filter(m => m.year === yearConfig.year);
        const completedYearModules = yearModules.filter(m => !m.isCurrentlyEnrolled);

        console.log(`Found ${yearModules.length} modules for ${yearConfig.year}, ${completedYearModules.length} completed`);

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
            sortedModules.sort((a, b) => {
              // Handle currently enrolled modules (place them at the end)
              if (a.isCurrentlyEnrolled && !b.isCurrentlyEnrolled) return 1;
              if (!a.isCurrentlyEnrolled && b.isCurrentlyEnrolled) return -1;
              return a.score - b.score;
            });
            break;
          case 'score-desc':
            sortedModules.sort((a, b) => {
              // Handle currently enrolled modules (place them at the end)
              if (a.isCurrentlyEnrolled && !b.isCurrentlyEnrolled) return 1;
              if (!a.isCurrentlyEnrolled && b.isCurrentlyEnrolled) return -1;
              return b.score - a.score;
            });
            break;
          case 'credits':
            sortedModules.sort((a, b) => b.credits - a.credits);
            break;
          case 'status':
            sortedModules.sort((a, b) => {
              // Sort by enrollment status (current modules first)
              if (a.isCurrentlyEnrolled && !b.isCurrentlyEnrolled) return -1;
              if (!a.isCurrentlyEnrolled && b.isCurrentlyEnrolled) return 1;
              // Then by name
              return a.name.localeCompare(b.name);
            });
            break;
        }

        const totalCredits = yearConfig.credits;
        const completedCredits = completedYearModules.reduce((sum, m) => sum + m.credits, 0);

        // Calculate year averages using only completed modules
        const average = completedYearModules.length ?
            Math.round(completedYearModules.reduce((sum, m) => sum + (m.score * m.credits), 0) /
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

      console.log(`Filtered to ${years.length} visible years`);
      if (years.length === 0 && this.moduleData.length > 0) {
        console.log("WARNING: No years are visible even though modules exist!");
        console.log("Module years:", [...new Set(this.moduleData.map(m => m.year))]);
        console.log("Active years in config:", this.calculatorConfig.years.filter(y => y.active).map(y => y.year));
      }

      return years;
    },

    // Get completed years count
    yearsCompleted() {
      return this.dashboardStats?.yearData?.length || 0;
    },

    // Generate semester options based on calculator config
    semesterOptions() {
      // Get the maximum number of semesters from calculator config or settings
      let maxSemesters = this.settings.academic.semestersPerYear || 2; // Default to settings value

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

      // Add semester options
      for (let i = 1; i <= maxSemesters; i++) {
        options.push({
          label: `Semester ${i}`,
          value: i
        });
      }

      // Add Full Academic Year option with a special value (0)
      options.push({
        label: "Full Academic Year",
        value: 0
      });

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
    'nextConfig.numYears': function (newValue) {
      if (newValue !== 'other' && newValue > 0) {
        this.initializeYearWeights(newValue);
      }
    },

    'nextConfig.customYears': function (newValue) {
      if (this.nextConfig.numYears === 'other' && newValue > 0) {
        this.initializeYearWeights(newValue);
      }
    },

    // Watch for changes in module enrollment status
    'moduleForm.isCurrentlyEnrolled': function (newValue) {
      if (newValue) {
        // Add completed flag to assessments when isCurrentlyEnrolled becomes true
        this.moduleForm.assessments = this.moduleForm.assessments.map(assessment => {
          if (!assessment.hasOwnProperty('completed')) {
            return {...assessment, completed: false};
          }
          return assessment;
        });
      }
    },

    // Watch for settings changes that affect the UI
    'settings.appearance.fontSize': function (newValue) {
      this.applyFontSize(newValue);
    },

    'settings.appearance.highContrast': function (newValue) {
      this.applyHighContrast(newValue);
    },

    'settings.accessibility.reduceMotion': function (newValue) {
      this.applyReduceMotion(newValue);
    },

    'settings.accessibility.focusMode': function (newValue) {
      this.applyFocusMode(newValue);
    }
  },
  async mounted() {
    // Load dark mode preference
    this.darkMode = getDarkModePreference();

    // Check mobile first
    this.checkMobile();
    window.addEventListener("resize", this.checkMobile);

    // Try to load sidebar preference from localStorage
    const storedSidebarState = localStorage.getItem('sidebarVisible');
    console.log(`Loading sidebar state from localStorage: ${storedSidebarState}`);

    if (storedSidebarState !== null) {
      // Parse string 'true'/'false' to boolean with explicit comparison
      this.sidebarVisible = storedSidebarState === 'true';
      console.log(`Set sidebar visibility to: ${this.sidebarVisible}`);
    }

    // Listen for dark mode changes
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // New Capacitor-specific setups
    if (this.isCapacitorApp()) {
      this.setupHardwareBackButton();
      this.handleOrientationChange();
      this.setupKeyboardListeners();
      this.setupPullToRefresh();

      // Add status bar color for Capacitor
      if (window.Capacitor.Plugins.StatusBar) {
        if (this.darkMode) {
          window.Capacitor.Plugins.StatusBar.setBackgroundColor({color: '#111827'});
          window.Capacitor.Plugins.StatusBar.setStyle({style: 'DARK'});
        } else {
          window.Capacitor.Plugins.StatusBar.setBackgroundColor({color: '#f8f9fa'});
          window.Capacitor.Plugins.StatusBar.setStyle({style: 'LIGHT'});
        }
      }
    }

    // Load settings from userSettingsService
    try {
      const userSettings = await userSettingsService.fetchSettings();
      if (userSettings) {
        this.settings = this.mergeDeep(this.settings, userSettings);
        console.log("Settings loaded from userSettingsService:", this.settings);

        // Apply settings immediately
        this.applyAllSettings();
      }
    } catch (error) {
      console.error("Error loading settings:", error);
    }

    // Add event listeners for settings changes
    this.setupSettingsEventListeners();

    // Fetch data after UI is initialized
    await this.checkLoginAndFetchConfig();
    await this.fetchModules();
    await this.fetchDashboardData();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkMobile);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);

    // Remove settings event listeners
    this.removeSettingsEventListeners();
  },
  methods: {
    // Setup settings event listeners
    setupSettingsEventListeners() {
      window.addEventListener('fontSizeChanged', this.onFontSizeChanged);
      window.addEventListener('highContrastChanged', this.onHighContrastChanged);
      window.addEventListener('animationsChanged', this.onAnimationsChanged);
      window.addEventListener('colorBlindModeChanged', this.onColorBlindModeChanged);
      window.addEventListener('reduceMotionChanged', this.onReduceMotionChanged);
      window.addEventListener('settingsChange', this.onSettingsChanged);
      window.addEventListener('calendarSettingsChanged', this.onCalendarSettingsChanged);
      window.addEventListener('yearSettingsUpdated', this.onYearSettingsUpdated);
      window.addEventListener('screenReaderVerbosityChanged', this.onScreenReaderVerbosityChanged);
    },

    // Remove settings event listeners
    removeSettingsEventListeners() {
      window.removeEventListener('fontSizeChanged', this.onFontSizeChanged);
      window.removeEventListener('highContrastChanged', this.onHighContrastChanged);
      window.removeEventListener('animationsChanged', this.onAnimationsChanged);
      window.removeEventListener('colorBlindModeChanged', this.onColorBlindModeChanged);
      window.removeEventListener('reduceMotionChanged', this.onReduceMotionChanged);
      window.removeEventListener('settingsChange', this.onSettingsChanged);
      window.removeEventListener('calendarSettingsChanged', this.onCalendarSettingsChanged);
      window.removeEventListener('yearSettingsUpdated', this.onYearSettingsUpdated);
      window.removeEventListener('screenReaderVerbosityChanged', this.onScreenReaderVerbosityChanged);
    },

    // Apply all settings at once
    applyAllSettings() {
      // Apply appearance settings
      this.applyFontSize(this.settings.appearance.fontSize);
      this.applyHighContrast(this.settings.appearance.highContrast);
      this.applyAnimations(this.settings.appearance.enableAnimations);

      // Apply accessibility settings
      this.applyColorBlindMode(this.settings.accessibility.colorBlindMode);
      this.applyReduceMotion(this.settings.accessibility.reduceMotion);
      this.applyFocusMode(this.settings.accessibility.focusMode);
      this.applyScreenReaderOptimization(this.settings.accessibility.screenReaderOptimized);

      // Apply academic settings
      this.updateAcademicSettings();

      // Apply calendar settings
      this.updateCalendarSettings();
    },

    // Settings event handlers
    onFontSizeChanged(event) {
      const size = event.detail.size;
      this.settings.appearance.fontSize = size;
      this.applyFontSize(size);
    },

    onHighContrastChanged(event) {
      const enabled = event.detail.enabled;
      this.settings.appearance.highContrast = enabled;
      this.applyHighContrast(enabled);
    },

    onAnimationsChanged(event) {
      const enabled = event.detail.enabled;
      this.settings.appearance.enableAnimations = enabled;
      this.applyAnimations(enabled);
    },

    onColorBlindModeChanged(event) {
      const mode = event.detail.mode;
      this.settings.accessibility.colorBlindMode = mode;
      this.applyColorBlindMode(mode);
    },

    onReduceMotionChanged(event) {
      const enabled = event.detail.enabled;
      this.settings.accessibility.reduceMotion = enabled;
      this.applyReduceMotion(enabled);
    },

    onSettingsChanged(event) {
      const {setting, value} = event.detail;

      // Handle various settings
      if (setting === 'keyboardShortcuts') {
        this.settings.accessibility.keyboardShortcuts = value;
      } else if (setting === 'screenReaderOptimized') {
        this.settings.accessibility.screenReaderOptimized = value;
        this.applyScreenReaderOptimization(value);
      } else if (setting === 'focusMode') {
        this.settings.accessibility.focusMode = value;
        this.applyFocusMode(value);
      }
    },

    onCalendarSettingsChanged(event) {
      // Update calendar settings
      const calendarSettings = event.detail;
      this.settings.calendar = {...this.settings.calendar, ...calendarSettings};
      this.updateCalendarSettings();
    },

    onYearSettingsUpdated(event) {
      // Update year weights and academic settings
      const {yearWeights, totalYears, creditsPerYear} = event.detail;

      if (yearWeights) {
        this.settings.academic.yearWeights = yearWeights;
      }

      if (totalYears) {
        this.settings.academic.totalYears = totalYears;
      }

      if (creditsPerYear) {
        this.settings.academic.creditsPerYear = creditsPerYear;
      }

      this.updateAcademicSettings();
    },

    onScreenReaderVerbosityChanged(event) {
      const level = event.detail.level;
      this.settings.accessibility.screenReaderVerbosity = level;
    },

    // Settings application methods
    applyFontSize(size) {
      const sizeMap = {
        'small': '14px',
        'medium': '16px',
        'large': '18px'
      };

      document.documentElement.style.setProperty('--font-size-base', sizeMap[size] || '16px');
    },

    applyHighContrast(enabled) {
      if (enabled) {
        document.documentElement.classList.add('high-contrast');
      } else {
        document.documentElement.classList.remove('high-contrast');
      }
    },

    applyAnimations(enabled) {
      if (!enabled) {
        document.documentElement.classList.add('disable-animations');
      } else {
        document.documentElement.classList.remove('disable-animations');
      }
    },

    applyColorBlindMode(mode) {
      // Remove any existing filters
      const existingFilter = document.getElementById('color-blind-filter');
      if (existingFilter) {
        existingFilter.remove();
      }

      // If no color blind mode selected, we're done
      if (mode === 'none') {
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

      switch (mode) {
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
      document.documentElement.style.filter = `url(#${mode})`;
    },

    applyReduceMotion(enabled) {
      if (enabled) {
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
    },

    applyMotionIntensity() {
      if (!this.settings.accessibility.reduceMotion) {
        // Scale transition duration based on intensity (0-100)
        const intensity = this.settings.accessibility.motionIntensity / 100;
        const transitionDuration = 0.1 + (intensity * 0.4); // Range from 0.1s to 0.5s

        document.documentElement.style.setProperty('--transition-speed', `${transitionDuration}s`);
      }
    },

    applyFocusMode(enabled) {
      if (enabled) {
        document.documentElement.classList.add('focus-mode');
      } else {
        document.documentElement.classList.remove('focus-mode');
      }
    },

    applyScreenReaderOptimization(enabled) {
      if (enabled) {
        document.documentElement.classList.add('screen-reader-optimized');
        // Add ARIA attributes to improve screen reader experience
        this.addScreenReaderAttributes();
      } else {
        document.documentElement.classList.remove('screen-reader-optimized');
      }
    },

    addScreenReaderAttributes() {
      // Add ARIA labels to elements that might need them
      // This would be more comprehensive in a real implementation
      const moduleCards = document.querySelectorAll('.module-card');
      moduleCards.forEach((card, index) => {
        const moduleName = card.querySelector('.module-name')?.textContent || `Module ${index + 1}`;
        const moduleScore = card.querySelector('.module-score')?.textContent || 'No score';
        card.setAttribute('aria-label', `${moduleName}, ${moduleScore}`);
      });
    },

    updateAcademicSettings() {
      // Update calculator config based on academic settings
      const academicSettings = this.settings.academic;

      // Only update if we need to and have valid data
      if (academicSettings.totalYears && academicSettings.creditsPerYear && academicSettings.yearWeights?.length) {
        // Create new calculator config years if needed
        if (!this.calculatorConfig.years || this.calculatorConfig.years.length === 0) {
          this.calculatorConfig.years = academicSettings.yearWeights.map((weight, index) => ({
            year: `Year ${index + 1}`,
            active: weight.active,
            credits: typeof academicSettings.creditsPerYear === 'number' ?
                academicSettings.creditsPerYear :
                parseInt(academicSettings.creditsPerYear) || 120,
            weight: weight.weight,
            semesters: academicSettings.semestersPerYear || 2
          }));
        }

        // Update target grade
        this.targetGrade = academicSettings.targetGrade;
        this.customTargetGrade = academicSettings.customTargetGrade;
      }
    },

    updateCalendarSettings() {
      // Update calendar component with settings
      // Real implementation would update the CalendarSidebar component
      console.log("Updating calendar with settings:", this.settings.calendar);
    },

    // Deep merge utility for merging settings objects
    mergeDeep(target, source) {
      const output = Object.assign({}, target);
      if (this.isObject(target) && this.isObject(source)) {
        Object.keys(source).forEach(key => {
          if (this.isObject(source[key])) {
            if (!(key in target)) {
              Object.assign(output, {[key]: source[key]});
            } else {
              output[key] = this.mergeDeep(target[key], source[key]);
            }
          } else {
            Object.assign(output, {[key]: source[key]});
          }
        });
      }
      return output;
    },

    isObject(item) {
      return (item && typeof item === 'object' && !Array.isArray(item));
    },

    // Capacitor detection and mobile methods
    isCapacitorApp() {
      return window.Capacitor !== undefined && window.Capacitor.isNative === true;
    },

    showGlobalAddModule() {
      // Create default years if none exist
      if (!this.calculatorConfig.years || this.calculatorConfig.years.length === 0) {
        // Create default years configuration based on settings if available
        if (this.settings.academic.totalYears && this.settings.academic.yearWeights?.length) {
          this.calculatorConfig.years = this.settings.academic.yearWeights.map((weight, index) => ({
            year: `Year ${index + 1}`,
            active: weight.active,
            credits: typeof this.settings.academic.creditsPerYear === 'number' ?
                this.settings.academic.creditsPerYear :
                parseInt(this.settings.academic.creditsPerYear) || 120,
            weight: weight.weight,
            semesters: this.settings.academic.semestersPerYear || 2
          }));
        } else {
          // Fallback to default values
          this.calculatorConfig.years = [
            {
              year: 'Year 1',
              active: true,
              credits: 120,
              weight: 33,
              semesters: 2
            },
            {
              year: 'Year 2',
              active: true,
              credits: 120,
              weight: 33,
              semesters: 2
            },
            {
              year: 'Year 3',
              active: true,
              credits: 120,
              weight: 34,
              semesters: 2
            }
          ];
        }
      }

      // Set up the module form
      this.editingModule = false;
      this.moduleForm = {
        name: '',
        code: '',
        credits: 15,
        // Use the first year if available, or 'Year 1' as fallback
        year: this.calculatorConfig.years && this.calculatorConfig.years.length > 0
            ? this.calculatorConfig.years[0].year
            : 'Year 1',
        semester: 1,
        score: 0,
        isCurrentlyEnrolled: true,
        assessments: [
          {name: 'Exam', weight: 100, score: 0, completed: false}
        ]
      };

      // Show the form
      this.showModuleForm = true;
    },

    // Method to handle hardware back button
    setupHardwareBackButton() {
      if (this.isCapacitorApp() && window.Capacitor.Plugins.App) {
        // Add hardware back button handler for Android
        window.Capacitor.Plugins.App.addListener('backButton', () => {
          if (this.showModuleDetail) {
            this.showModuleDetail = false;
            return;
          }

          if (this.showModuleForm) {
            this.showModuleForm = false;
            return;
          }

          if (this.sidebarVisible && this.isMobile) {
            this.sidebarVisible = false;
            return;
          }

          // If on a wizard step, go back to previous step
          if (this.showYearWeights) {
            this.goBackToDegreeConfig();
            return;
          }

          if (this.showNextConfig) {
            this.goBackToStep1();
            return;
          }

          if (this.showSetupWizard) {
            // Just close the app, as we're at the beginning
            window.Capacitor.Plugins.App.exitApp();
            return;
          }

          // If on insights or yearly view, go back to overview
          if (this.activeView !== 'overview') {
            this.activeView = 'overview';
            return;
          }

          // Allow system to handle back button (usually exit app)
          window.Capacitor.Plugins.App.minimizeApp();
        });
      }
    },

    // Method to handle screen orientation changes
    handleOrientationChange() {
      if (this.isCapacitorApp() && window.screen.orientation) {
        window.screen.orientation.addEventListener('change', () => {
          // Force UI update on orientation change
          this.checkMobile();

          // Small timeout to allow UI to adjust
          setTimeout(() => {
            // Force chart redraw if needed
            if (this.$refs.gradeChart) {
              this.$refs.gradeChart.redrawChart();
            }
            if (this.$refs.yearChart) {
              this.$refs.yearChart.redrawChart();
            }
          }, 300);
        });
      }
    },

    // Setup keyboard event listeners for Capacitor
    setupKeyboardListeners() {
      if (this.isCapacitorApp() && window.Capacitor.Plugins.Keyboard) {
        window.Capacitor.Plugins.Keyboard.addListener('keyboardWillShow', () => {
          document.body.classList.add('keyboard-open');
        });

        window.Capacitor.Plugins.Keyboard.addListener('keyboardWillHide', () => {
          document.body.classList.remove('keyboard-open');
        });
      }
    },

    // Pull to refresh functionality
    setupPullToRefresh() {
      if (this.isCapacitorApp()) {
        let startY = 0;
        let currentY = 0;
        const threshold = 100;
        let isPulling = false;
        let refreshIndicator = null;

        // Create refresh indicator
        const createIndicator = () => {
          refreshIndicator = document.createElement('div');
          refreshIndicator.className = 'pull-to-refresh-indicator';
          refreshIndicator.textContent = 'Pull down to refresh';
          document.querySelector('.dashboard-main-content').prepend(refreshIndicator);
          return refreshIndicator;
        };

        // Handle touch start
        document.addEventListener('touchstart', (e) => {
          // Only activate at top of page
          if (window.scrollY === 0) {
            startY = e.touches[0].clientY;
            isPulling = true;

            if (!refreshIndicator) {
              refreshIndicator = createIndicator();
            }
          }
        });

        // Handle touch move
        document.addEventListener('touchmove', (e) => {
          if (!isPulling) return;

          currentY = e.touches[0].clientY;
          const pullDistance = currentY - startY;

          if (pullDistance > 0 && pullDistance < threshold) {
            refreshIndicator.textContent = 'Pull down to refresh';
            refreshIndicator.style.marginTop = `${pullDistance - 40}px`;
          } else if (pullDistance >= threshold) {
            refreshIndicator.textContent = 'Release to refresh';
            refreshIndicator.style.marginTop = `${threshold - 40}px`;
          }
        });

        // Handle touch end
        document.addEventListener('touchend', async () => {
          if (!isPulling) return;

          const pullDistance = currentY - startY;
          isPulling = false;

          if (pullDistance >= threshold) {
            refreshIndicator.textContent = 'Refreshing...';

            // Refresh data
            try {
              await Promise.all([
                this.fetchModules(),
                this.fetchDashboardData()
              ]);

              refreshIndicator.textContent = 'Updated!';
              setTimeout(() => {
                refreshIndicator.style.marginTop = '-40px';
              }, 500);
            } catch (error) {
              refreshIndicator.textContent = 'Failed to refresh';
              setTimeout(() => {
                refreshIndicator.style.marginTop = '-40px';
              }, 500);
            }
          } else {
            refreshIndicator.style.marginTop = '-40px';
          }
        });
      }
    },

    // Show loading overlay
    showLoading() {
      if (document.querySelector('.loading-overlay')) return;

      const overlay = document.createElement('div');
      overlay.className = 'loading-overlay';

      const spinner = document.createElement('div');
      spinner.className = 'loading-spinner';
      overlay.appendChild(spinner);

      document.body.appendChild(overlay);
    },

    // Hide loading overlay
    hideLoading() {
      const overlay = document.querySelector('.loading-overlay');
      if (overlay) {
        overlay.remove();
      }
    },

    // Show native toast notification (Capacitor)
    showNativeToast(message) {
      if (this.isCapacitorApp() && window.Capacitor.Plugins.Toast) {
        window.Capacitor.Plugins.Toast.show({
          text: message,
          duration: 'short',
          position: 'bottom'
        });
      } else {
        // Fallback to notify service
        notify({type: "info", message: message});
      }
    },

    // Enhanced checkMobile method
    checkMobile() {
      const wasMobile = this.isMobile;

      // Check if we're in a Capacitor app
      if (this.isCapacitorApp()) {
        // Always treat Capacitor as mobile
        this.isMobile = true;
      } else {
        // Regular browser check
        this.isMobile = window.innerWidth <= 768;
      }

      // Add appropriate class to body
      if (this.isMobile) {
        document.body.classList.add('is-mobile');

        // Add platform-specific class
        if (this.isCapacitorApp()) {
          if (window.Capacitor.getPlatform() === 'ios') {
            document.body.classList.add('capacitor-ios');
          } else if (window.Capacitor.getPlatform() === 'android') {
            document.body.classList.add('capacitor-android');
          }
        }
      } else {
        document.body.classList.remove('is-mobile');
        document.body.classList.remove('capacitor-ios');
        document.body.classList.remove('capacitor-android');
      }

      // Only force hiding of sidebar when switching to mobile
      if (!wasMobile && this.isMobile && this.sidebarVisible) {
        console.log("Switching to mobile - hiding sidebar");
        this.sidebarVisible = false;
        localStorage.setItem('sidebarVisible', 'false');
      }
    },

    // API methods
    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_URL}/user/profile`, {withCredentials: true});
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
        const response = await axios.get(`${API_URL}/calculator`, {withCredentials: true});
        this.calculatorConfig = response.data;

        // Synchronize with settings if needed
        this.syncCalculatorConfigWithSettings();

        return response.data;
      } catch (error) {
        console.error("Error fetching calculator config:", error);
        return null;
      }
    },

    syncCalculatorConfigWithSettings() {
      if (!this.calculatorConfig || !this.calculatorConfig.years || !this.settings.academic.yearWeights) {
        return;
      }

      // Update calculator config with settings values where appropriate
      // (This method could be expanded based on your specific needs)
    },

    async fetchModules() {
      if (this.isMobile) this.showLoading();

      try {
        this.loading = true;
        console.log("Fetching modules from API...");
        const response = await axios.get(`${API_URL}/modules`, {withCredentials: true});
        console.log("Modules from API:", response.data);
        this.moduleData = response.data;
        console.log("Current moduleData after assignment:", this.moduleData);
        console.log("Number of modules loaded:", this.moduleData.length);

        // Log module details for debugging
        if (this.moduleData.length > 0) {
          console.log("First module details:", {
            name: this.moduleData[0].name,
            year: this.moduleData[0].year,
            isCurrentlyEnrolled: this.moduleData[0].isCurrentlyEnrolled
          });
        }

        this.prepareChartData();

        // Check filtered years for debugging
        const yearsWithModules = [...new Set(this.moduleData.map(m => m.year))];
        console.log("Years containing modules:", yearsWithModules);
        console.log("Calculator config years:", this.calculatorConfig.years?.map(y => y.year) || []);

        return response.data;
      } catch (error) {
        console.error("Error fetching modules:", error);
        if (error.response) {
          console.error("Response status:", error.response.status);
          console.error("Response data:", error.response.data);
        }

        // Try to load from local storage as fallback
        try {
          const localModules = JSON.parse(localStorage.getItem('gradeGuardModules') || '[]');
          console.log("Loaded modules from local storage:", localModules);
          if (localModules.length > 0) {
            this.moduleData = localModules;
            console.log("Using local storage modules as fallback");
          }
        } catch (localError) {
          console.error("Error loading from local storage:", localError);
        }

        if (this.isCapacitorApp()) {
          this.showNativeToast("Failed to load modules");
        }
        return [];
      } finally {
        this.loading = false;
        if (this.isMobile) this.hideLoading();
      }
    },

    async fetchDashboardData() {
      if (this.isMobile) this.showLoading();

      try {
        this.loading = true;
        const response = await axios.get(`${API_URL}/dashboard`, {withCredentials: true});
        const {stats, config} = response.data;

        this.dashboardStats = stats;
        this.dashboardConfig = config;

        // Load recent activities and goals from dashboard config
        this.recentActivities = config.recentActivities || [];
        this.goals = config.goals || [];

        // Prepare chart data
        this.yearData = stats.yearData || [];
        this.scoreDistribution = stats.gradeDistribution || [];

        // Generate personalized tips
        this.generatePersonalizedTips();

        return response.data;
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        if (this.isCapacitorApp()) {
          this.showNativeToast("Failed to load dashboard data");
        }
        return null;
      } finally {
        this.loading = false;
        if (this.isMobile) this.hideLoading();
      }
    },

    // Handle dark mode change
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
      this.settings.appearance.darkMode = this.darkMode;

      // Update status bar in Capacitor
      if (this.isCapacitorApp() && window.Capacitor.Plugins.StatusBar) {
        if (this.darkMode) {
          window.Capacitor.Plugins.StatusBar.setBackgroundColor({color: '#111827'});
          window.Capacitor.Plugins.StatusBar.setStyle({style: 'DARK'});
        } else {
          window.Capacitor.Plugins.StatusBar.setBackgroundColor({color: '#f8f9fa'});
          window.Capacitor.Plugins.StatusBar.setStyle({style: 'LIGHT'});
        }
      }

      // Reapply accent color when theme changes
      const accentColor = this.settings.appearance.accentColor || 'purple';
      this.applyAccentColor(accentColor);

      // Reapply color blind mode filter after theme change
      if (this.settings.accessibility.colorBlindMode !== 'none') {
        this.applyColorBlindMode(this.settings.accessibility.colorBlindMode);
      }
    },

    // Apply accent color
    applyAccentColor(colorId) {
      // Map of color IDs to their hex values
      const colorMap = {
        'purple': '#7b49ff',
        'blue': '#2196f3',
        'green': '#4caf50',
        'red': '#f44336',
        'orange': '#ff9800',
        'pink': '#e91e63',
        'teal': '#009688'
      };

      const colorValue = colorMap[colorId] || colorMap['purple']; // Default to purple

      // Set CSS variables for the accent color
      document.documentElement.style.setProperty('--primary-color', colorValue);

      // Calculate darker variant for hover states
      const darkerColor = this.adjustColor(colorValue, -20);
      document.documentElement.style.setProperty('--primary-dark', darkerColor);

      // Calculate lighter variant
      const lighterColor = this.adjustColor(colorValue, 20);
      document.documentElement.style.setProperty('--primary-light', lighterColor);
    },

    // Helper function to adjust colors
    adjustColor(hex, amount) {
      // Convert hex to RGB
      let r = parseInt(hex.slice(1, 3), 16);
      let g = parseInt(hex.slice(3, 5), 16);
      let b = parseInt(hex.slice(5, 7), 16);

      // Adjust RGB values
      r = Math.max(0, Math.min(255, r + amount));
      g = Math.max(0, Math.min(255, g + amount));
      b = Math.max(0, Math.min(255, b + amount));

      // Convert back to hex
      return `#${Math.round(r).toString(16).padStart(2, '0')}${Math.round(g).toString(16).padStart(2, '0')}${Math.round(b).toString(16).padStart(2, '0')}`;
    },

    // Handle logout event from navbar
    async handleLogout() {
      if (this.isMobile) this.showLoading();

      try {
        await axios.post(`${API_URL}/logout`, {}, {withCredentials: true});
        this.notLoggedIn = true;

        // Exit app if on Capacitor
        if (this.isCapacitorApp()) {
          this.showNativeToast("Logged out successfully");
          // Give time for toast to show before exiting
          setTimeout(() => {
            window.Capacitor.Plugins.App.exitApp();
          }, 1000);
        } else {
          // Add the logout=true query parameter here for web
          this.$router.push('/login?logout=true');
        }
      } catch (error) {
        console.error("Error during logout:", error);

        if (this.isCapacitorApp()) {
          this.showNativeToast("Error during logout");
          this.hideLoading();
        } else {
          // Also add it here in case of errors
          this.$router.push('/login?logout=true');
        }
      } finally {
        if (this.isMobile) this.hideLoading();
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
      // Use grading scale from settings if available
      const gradingScale = this.settings.academic.gradingScale || [];

      if (gradingScale.length >= 5) {
        // Find corresponding grade in the scale
        const firstClass = gradingScale.find(g => g.letter === 'A');
        const upperSecond = gradingScale.find(g => g.letter === 'B');
        const lowerSecond = gradingScale.find(g => g.letter === 'C');
        const third = gradingScale.find(g => g.letter === 'D');

        // Use custom thresholds if available
        if (firstClass && score >= firstClass.minPercentage) return 'excellent-score';
        if (upperSecond && score >= upperSecond.minPercentage) return 'good-score';
        if (lowerSecond && score >= lowerSecond.minPercentage) return 'average-score';
        if (third && score >= third.minPercentage) return 'pass-score';
        return 'fail-score';
      }

      // Default behavior if gradingScale is not properly configured
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
        isCurrentlyEnrolled: true, // Default to true for new modules
        assessments: [
          {name: 'Exam', weight: 100, score: 0, completed: false}
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

      // If the module doesn't have the isCurrentlyEnrolled field, default to false
      if (this.moduleForm.isCurrentlyEnrolled === undefined) {
        this.moduleForm.isCurrentlyEnrolled = false;
      }

      // Ensure assessments array exists
      if (!this.moduleForm.assessments || !this.moduleForm.assessments.length) {
        this.moduleForm.assessments = [
          {name: 'Exam', weight: 100, score: module.score, completed: !module.isCurrentlyEnrolled}
        ];
      } else if (this.moduleForm.isCurrentlyEnrolled) {
        // Make sure all assessments have the 'completed' property if the module is currently enrolled
        this.moduleForm.assessments = this.moduleForm.assessments.map(assessment => {
          if (!assessment.hasOwnProperty('completed')) {
            return {...assessment, completed: false};
          }
          return assessment;
        });
      }

      this.showModuleDetail = false;
      this.showModuleForm = true;
    },

    // Add assessment to module form
    addAssessment() {
      this.moduleForm.assessments.push({
        name: `Assessment ${this.moduleForm.assessments.length + 1}`,
        weight: 0,
        score: 0,
        completed: false
      });
    },

    // Remove assessment from module form
    removeAssessment(index) {
      this.moduleForm.assessments.splice(index, 1);
    },

    // Export grades to CSV
    exportGrades() {
      // Create CSV content with proper date formatting based on settings
      let csv = 'Year,Module,Code,Credits,Semester,Score,Currently Enrolled\n';

      // Format date function that respects settings
      const formatDate = (date) => {
        if (!date) return '';

        const dateObj = new Date(date);
        const format = this.settings.calendar.dateFormat || 'MM/DD/YYYY';

        // Simple formatting based on format string
        const day = dateObj.getDate().toString().padStart(2, '0');
        const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
        const year = dateObj.getFullYear();

        if (format === 'MM/DD/YYYY') {
          return `${month}/${day}/${year}`;
        } else if (format === 'DD/MM/YYYY') {
          return `${day}/${month}/${year}`;
        } else {
          return `${year}-${month}-${day}`;
        }
      };

      this.moduleData.forEach(module => {
        const semesterText = module.semester === 0 ? 'Full Year' : `Semester ${module.semester || 1}`;
        const scoreText = module.isCurrentlyEnrolled ? 'In Progress' : `${module.score}`;
        csv += `${module.year},${module.name},${module.code || ''},${module.credits},${semesterText},${scoreText},${module.isCurrentlyEnrolled ? 'Yes' : 'No'}\n`;
      });

      // Handle export based on platform
      if (this.isCapacitorApp() && window.Capacitor.Plugins.Filesystem) {
        // Save file using Capacitor
        const fileName = `GradeGuard_Export_${new Date().toISOString().slice(0, 10)}.csv`;

        window.Capacitor.Plugins.Filesystem.writeFile({
          path: fileName,
          data: csv,
          directory: window.Capacitor.FilesystemDirectory.Documents,
          encoding: window.Capacitor.FilesystemEncoding.UTF8
        }).then(() => {
          this.showNativeToast("Grades exported successfully to Documents folder");

          // Try to share the file
          if (window.Capacitor.Plugins.Share) {
            window.Capacitor.Plugins.Share.share({
              title: 'GradeGuard Export',
              text: 'Your exported grades',
              url: fileName,
              dialogTitle: 'Share your grades'
            }).catch(err => {
              console.error("Error sharing file:", err);
            });
          }
        }).catch(err => {
          console.error("Error saving file:", err);
          this.showNativeToast("Error exporting grades");
        });
      } else {
        // Web browser export
        const blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', 'GradeGuard_Export.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        notify({type: "success", message: "Grades exported successfully!"});
      }
    },

    // Prepare data for charts
    prepareChartData() {
      // Year data for year comparison chart will be from API

      // Score distribution for charts
      const completedModules = this.completedModuleData;
      const scores = completedModules.map(m => m.score);

      // Use grading scale ranges from settings if available
      let ranges;
      const gradingScale = this.settings.academic.gradingScale;

      if (gradingScale && gradingScale.length >= 4) {
        ranges = [];
        // Sort grading scale by minPercentage in descending order
        const sortedScale = [...gradingScale].sort((a, b) => b.minPercentage - a.minPercentage);

        // Create ranges from grading scale
        for (let i = 0; i < sortedScale.length; i++) {
          const min = sortedScale[i].minPercentage;
          const max = i === 0 ? 100 : sortedScale[i - 1].minPercentage - 1;
          ranges.push({
            name: `${sortedScale[i].letter} (${min}-${max}%)`,
            range: [min, max]
          });
        }
      } else {
        // Default ranges
        ranges = [
          {name: '0-39%', range: [0, 39]},
          {name: '40-49%', range: [40, 49]},
          {name: '50-59%', range: [50, 59]},
          {name: '60-69%', range: [60, 69]},
          {name: '70-100%', range: [70, 100]}
        ];
      }

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
      const completedModules = this.completedModuleData;
      const modulesByYear = {};

      completedModules.forEach(module => {
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
        {name: 'Programming', pattern: /(programming|coding|development|software)/i},
        {name: 'Theory', pattern: /(theory|concepts|foundations)/i},
        {name: 'Mathematics', pattern: /(math|mathematics|calculation|statistics)/i},
        {name: 'Design', pattern: /(design|architecture|interface)/i},
        {name: 'Research', pattern: /(research|analysis|thesis)/i},
        {name: 'Security', pattern: /(security|cyber|protection)/i}
      ];

      this.strengthsData = subjectCategories.map(category => {
        const matchingModules = completedModules.filter(m =>
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

    // Generate personalized tips based on module data and settings
    generatePersonalizedTips() {
      const tips = [];

      // Focus on currently enrolled modules
      const currentModules = this.currentModuleData;
      if (currentModules.length > 0) {
        // Group by completion date or urgency
        const upcomingModules = currentModules.slice(0, 3); // Take the first 3 for simplicity

        upcomingModules.forEach(module => {
          tips.push({
            title: `Focus on ${module.name}`,
            description: `You're currently enrolled in this module. Create a study plan and allocate regular time to stay on top of the coursework.`
          });
        });

        // Add general study tip for current modules
        if (currentModules.length > 0) {
          tips.push({
            title: 'Current Modules Strategy',
            description: `You're currently enrolled in ${currentModules.length} module${currentModules.length > 1 ? 's' : ''}. Try to distribute your effort based on credit weighting and assessment schedules.`
          });
        }
      }

      // Add study preference based tip if available
      if (this.settings.academic.studyPreferences && this.settings.academic.studyPreferences.length > 0) {
        const preferredTimes = this.settings.academic.studyPreferences.join(' and ');
        tips.push({
          title: 'Leverage Your Study Preferences',
          description: `You've indicated that ${preferredTimes} are your best study times. Schedule your most difficult work during these periods to maximize productivity.`
        });
      }

      // Add time management tip
      tips.push({
        title: 'Effective Time Management',
        description: 'Break down large assignments into smaller tasks and set deadlines for each part. This makes progress more manageable and reduces last-minute stress.'
      });

      // Add study technique tip
      tips.push({
        title: 'Active Learning Techniques',
        description: 'Instead of passive reading, try active recall by testing yourself on key concepts. Research shows this significantly improves retention compared to re-reading materials.'
      });

      // Add tip based on academic level if available
      if (this.settings.academic.academicLevel) {
        let levelTip = {
          title: `${this.settings.academic.academicLevel} Level Tips`,
          description: ''
        };

        if (this.settings.academic.academicLevel === 'Undergraduate') {
          levelTip.description = 'Focus on building a solid foundation across all your subjects. Make connections between different modules to deepen your understanding.';
        } else if (this.settings.academic.academicLevel.includes('Masters')) {
          levelTip.description = 'Develop your critical analysis skills. Go beyond just learning content to evaluating, critiquing, and applying concepts in new contexts.';
        } else if (this.settings.academic.academicLevel.includes('PhD')) {
          levelTip.description = 'Regular writing is essential. Set aside time each week to document your research progress and ideas, even if they\'re not fully formed yet.';
        }
        if (levelTip.description) {
          tips.push(levelTip);
        }
      }

      // If we have less than 4 tips, add general ones
      if (tips.length < 4) {
        tips.push({
          title: 'Balance Your Workload',
          description: 'Try spacing out your work to reduce stress and improve quality. Setting regular study periods can help maintain consistent progress.'
        });
      }

      this.personalizedTips = tips.slice(0, 4); // Limit to 4 tips
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
      if (!this.yearWeights) return;

      // Validate individual weights (cap at 100)
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
          // Try to use academic settings for setup if available
          if (this.settings.academic.yearWeights?.length) {
            this.calculatorConfig.years = this.settings.academic.yearWeights.map((weight, index) => ({
              year: `Year ${index + 1}`,
              active: weight.active,
              credits: typeof this.settings.academic.creditsPerYear === 'number' ?
                  this.settings.academic.creditsPerYear :
                  parseInt(this.settings.academic.creditsPerYear) || 120,
              weight: weight.weight,
              semesters: this.settings.academic.semestersPerYear || 2
            }));
          } else {
            this.showSetupWizard = true;
          }
        }
      } catch (error) {
        console.error("Error checking login and config:", error);
        this.notLoggedIn = true;
      }
    },

    logSidebarStatus() {
      console.log(
          `[Sidebar Debug] sidebarVisible: ${this.sidebarVisible},
     localStorage value: ${localStorage.getItem('sidebarVisible')},
     isMobile: ${this.isMobile}`
      );
    },

    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
      localStorage.setItem('sidebarVisible', this.sidebarVisible.toString());

      // Add debug logs
      console.log(`Sidebar toggled to: ${this.sidebarVisible}`);

      // Add proper class for mobile
      if (this.sidebarVisible && this.isMobile) {
        document.querySelector('.dashboard-sidebar').classList.add('visible');
      } else if (!this.sidebarVisible && this.isMobile) {
        document.querySelector('.dashboard-sidebar').classList.remove('visible');
      }
    },

    // Save user config from wizard step 1
    saveUserConfig() {
      if (!this.userConfig.academicLevel || !this.userConfig.enrollmentType || !this.userConfig.studyPreference) {
        const message = "Please complete all preference fields.";
        if (this.isCapacitorApp()) {
          this.showNativeToast(message);
        } else {
          notify({type: "warning", message: message});
        }
        return;
      }

      // Update settings with user config
      this.settings.academic.academicLevel = this.userConfig.academicLevel;
      this.settings.academic.enrollmentType = this.userConfig.enrollmentType;
      this.settings.academic.studyPreferences = [this.userConfig.studyPreference];

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
        const message = "Please fill all degree details (years, semesters, credits).";
        if (this.isCapacitorApp()) {
          this.showNativeToast(message);
        } else {
          notify({type: "warning", message: message});
        }
        return;
      }

      // Update settings with degree config
      this.settings.academic.totalYears = yearsCount;
      this.settings.academic.semestersPerYear = semCount;
      this.settings.academic.creditsPerYear = credCount;

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

    async completeSetup() {
      // Validate weights before proceeding
      if (this.totalWeight !== 100 && this.hasActiveYears) {
        const message = "The total weight of active years should equal 100%.";
        if (this.isCapacitorApp()) {
          this.showNativeToast(message);
        } else {
          notify({type: "warning", message: message});
        }
        return;
      }

      if (this.isMobile) this.showLoading();

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

        // Update settings with completed setup data
        this.settings.academic.totalYears = yearsCount;
        this.settings.academic.semestersPerYear = semCount;
        this.settings.academic.creditsPerYear = credCount;
        this.settings.academic.yearWeights = this.yearWeights;
        this.settings.academic.targetGrade = this.targetGrade;
        this.settings.academic.customTargetGrade = this.customTargetGrade;

        // Save calculator config
        await axios.put(
            `${API_URL}/calculator/update`,
            configData,
            {withCredentials: true}
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
            {withCredentials: true}
        );

        // Save user configuration
        if (this.userConfig.academicLevel || this.userConfig.enrollmentType || this.userConfig.studyPreference) {
          await axios.put(
              `${API_URL}/user/config`,
              {studyPreferences: this.userConfig},
              {withCredentials: true}
          );
        }

        // Save settings to userSettingsService
        await userSettingsService.saveSettings(this.settings);

        this.showYearWeights = false;
        this.showSetupWizard = false;
        this.showNextConfig = false;

        // Refresh data
        await this.fetchCalculatorConfig();
        await this.fetchModules();
        await this.fetchDashboardData();

        const message = "Setup completed successfully!";
        if (this.isCapacitorApp()) {
          this.showNativeToast(message);
        } else {
          notify({type: "success", message: message});
        }
      } catch (error) {
        console.error("Error completing setup:", error);
        const errorMsg = `Setup failed: ${error.response?.data?.error || error.message}`;

        if (this.isCapacitorApp()) {
          this.showNativeToast(errorMsg);
        } else {
          notify({type: "error", message: errorMsg});
        }
      } finally {
        this.loading = false;
        if (this.isMobile) this.hideLoading();
      }
    },
    async saveModule() {
      if (!this.isModuleFormValid) {
        notify({
          type: "warning",
          message: "Please complete all required fields and ensure assessment weights total 100%."
        });
        return;
      }

      if (this.isMobile) this.showLoading();

      try {
        this.loading = true;
        console.log("Saving module:", this.moduleForm);

        // Calculate overall score based on completed assessments
        if (this.moduleForm.isCurrentlyEnrolled) {
          // Only calculate score from completed assessments
          const completedAssessments = this.moduleForm.assessments.filter(a => a.completed);

          if (completedAssessments.length > 0) {
            const totalWeight = completedAssessments.reduce((sum, a) => sum + a.weight, 0);
            const weightedScore = completedAssessments.reduce((sum, a) => sum + (a.score * a.weight), 0);

            this.moduleForm.score = totalWeight > 0 ? Math.round((weightedScore / totalWeight) * 10) / 10 : 0;
          } else {
            this.moduleForm.score = 0; // No completed assessments yet
          }

          // Set the status property to 'in_progress' to align with your requirement
          this.moduleForm.status = 'in_progress';
        } else {
          // For completed modules, calculate normally
          const totalScore = this.moduleForm.assessments.reduce((sum, assessment) => {
            return sum + (assessment.score * assessment.weight / 100);
          }, 0);

          this.moduleForm.score = Math.round(totalScore * 10) / 10;
          this.moduleForm.status = 'completed';
        }

        // Try to save to API first
        let response;
        let apiSuccess = false;

        try {
          if (this.editingModule) {
            // Update existing module
            console.log("Updating existing module with ID:", this.moduleForm.id);
            response = await axios.put(
                `${API_URL}/modules/${this.moduleForm.id}`,
                this.moduleForm,
                {withCredentials: true}
            );
            apiSuccess = true;
            console.log("Module updated successfully via API");
          } else {
            // Create new module
            console.log("Creating new module");
            response = await axios.post(
                `${API_URL}/modules`,
                this.moduleForm,
                {withCredentials: true}
            );
            apiSuccess = true;
            console.log("Module created successfully via API");
          }

          if (response && response.data) {
            console.log("API response after save:", response.data);
          }
        } catch (apiError) {
          console.warn("API save failed, will use local storage instead:", apiError);
          if (apiError.response) {
            console.error("Response status:", apiError.response.status);
            console.error("Response data:", apiError.response.data);
          }
          // We'll continue with local storage backup below
        }

        // If API call was successful, refresh data and ensure the year is active
        if (apiSuccess) {
          try {
            console.log("API save successful, updating calculator config if needed...");

            // Get the year of the module we just saved
            const moduleYear = this.moduleForm.year;

            // Fetch the latest calculator config
            const calcResponse = await axios.get(`${API_URL}/calculator`, {withCredentials: true});
            let calculatorConfig = calcResponse.data;

            // Initialize years array if it doesn't exist
            if (!calculatorConfig.years) {
              calculatorConfig.years = [];
            }

            // Check if the year exists in the calculator config
            let yearConfig = calculatorConfig.years.find(y => y.year === moduleYear);
            let configUpdated = false;

            if (yearConfig) {
              // Year exists but might not be active - ensure it's active
              if (!yearConfig.active) {
                console.log(`Activating existing year ${moduleYear} in calculator config`);
                yearConfig.active = true;
                configUpdated = true;
              }
            } else {
              // Year doesn't exist - create it with reasonable defaults
              console.log(`Adding new year ${moduleYear} to calculator config`);

              // Calculate default weight (distribute evenly or use a fixed percentage)
              const newWeight = calculatorConfig.years.length > 0 ?
                  Math.floor(100 / (calculatorConfig.years.length + 1)) : 100;

              calculatorConfig.years.push({
                year: moduleYear,
                active: true,
                credits: 120, // Standard UK credits per year
                weight: newWeight,
                semesters: 2 // Standard semesters per year
              });

              // Adjust weights of other years if needed
              if (calculatorConfig.years.length > 1) {
                const totalWeight = calculatorConfig.years.reduce((sum, year) => sum + year.weight, 0);
                if (totalWeight > 100) {
                  // Normalize weights to sum to 100
                  const factor = 100 / totalWeight;
                  calculatorConfig.years.forEach(year => {
                    year.weight = Math.floor(year.weight * factor);
                  });

                  // Ensure they sum to exactly 100 by adjusting the last year
                  const sumAfterNormalization = calculatorConfig.years.reduce((sum, year) => sum + year.weight, 0);
                  if (sumAfterNormalization !== 100) {
                    const diff = 100 - sumAfterNormalization;
                    calculatorConfig.years[calculatorConfig.years.length - 1].weight += diff;
                  }
                }
              }

              configUpdated = true;
            }

            // Save updated config if changes were made
            if (configUpdated) {
              await axios.put(
                  `${API_URL}/calculator`,
                  calculatorConfig,
                  {withCredentials: true}
              );
              console.log("Calculator config updated with active year:", moduleYear);

              // Update local calculator config to match
              this.calculatorConfig = calculatorConfig;
            }

            // Now refresh all data to ensure consistent state
            console.log("Refreshing modules and dashboard data...");
            await this.fetchCalculatorConfig();
            await this.fetchModules();
            await this.fetchDashboardData();

            // Ensure we're on yearly view and showing all years
            this.activeView = 'yearly';
            this.selectedYear = 'all';

            // Force UI update after a short delay to ensure data is processed
            setTimeout(() => {
              this.$forceUpdate();
              console.log("UI forcefully updated");
            }, 100);

          } catch (configError) {
            console.error("Error updating calculator config:", configError);
            // Still fetch modules even if config update failed
            await this.fetchModules();
            await this.fetchDashboardData();
          }
        } else {
          // If API failed, add the module to the local moduleData array directly
          console.log("Using local storage fallback for module save");
          const moduleToAdd = {...this.moduleForm};

          if (!this.editingModule) {
            // Generate a local ID for new modules
            moduleToAdd.id = 'local-' + Date.now();
            console.log("Generated local ID for new module:", moduleToAdd.id);
          }

          // Update or add to moduleData
          if (this.editingModule) {
            const index = this.moduleData.findIndex(m => m.id === moduleToAdd.id);
            if (index >= 0) {
              console.log("Updating module at index:", index);
              this.moduleData[index] = moduleToAdd;
            } else {
              console.log("Module ID not found, adding as new");
              this.moduleData.push(moduleToAdd);
            }
          } else {
            console.log("Adding new module to moduleData");
            this.moduleData.push(moduleToAdd);
          }

          console.log("Current moduleData after local update:", this.moduleData.length);

          // Check and update calculator config for local storage case too
          try {
            const moduleYear = this.moduleForm.year;
            let yearExists = false;
            let yearActive = false;

            // Check if year exists and is active
            if (this.calculatorConfig && this.calculatorConfig.years) {
              const yearConfig = this.calculatorConfig.years.find(y => y.year === moduleYear);
              if (yearConfig) {
                yearExists = true;
                yearActive = yearConfig.active;

                // Activate the year if it exists but isn't active
                if (!yearActive) {
                  yearConfig.active = true;
                  // No need to update API here as we're in local storage mode
                  console.log(`Activated year ${moduleYear} in local calculator config`);
                }
              }
            }

            // If year doesn't exist, add it
            if (!yearExists && this.calculatorConfig) {
              if (!this.calculatorConfig.years) {
                this.calculatorConfig.years = [];
              }

              this.calculatorConfig.years.push({
                year: moduleYear,
                active: true,
                credits: 120,
                weight: 100 / (this.calculatorConfig.years.length + 1),
                semesters: 2
              });

              console.log(`Added new year ${moduleYear} to local calculator config`);
            }
          } catch (localConfigError) {
            console.error("Error updating local calculator config:", localConfigError);
          }

          // Update the UI
          this.$nextTick(() => {
            this.activeView = 'yearly';
            this.selectedYear = 'all';
            this.$forceUpdate();
            console.log("UI updated after local update");
          });
        }

        // Create or update local storage backup of modules
        try {
          const modules = JSON.parse(localStorage.getItem('gradeGuardModules') || '[]');
          // Add ID if this is a new module
          if (!this.editingModule) {
            this.moduleForm.id = this.moduleForm.id || 'local-' + Date.now();
          }
          // Update or add the module
          const existingIndex = modules.findIndex(m => m.id === this.moduleForm.id);
          if (existingIndex >= 0) {
            modules[existingIndex] = {...this.moduleForm};
            console.log("Updated module in local storage");
          } else {
            modules.push({...this.moduleForm});
            console.log("Added module to local storage");
          }
          localStorage.setItem('gradeGuardModules', JSON.stringify(modules));
          console.log("Local storage updated with modules");
        } catch (storageError) {
          console.error("Error saving to local storage:", storageError);
        }

        const message = `Module ${this.editingModule ? 'updated' : 'added'} successfully!`;

        if (this.isCapacitorApp()) {
          this.showNativeToast(message);
        } else {
          notify({type: "success", message: message});
        }

        this.showModuleForm = false;

        // Add activity to recent activities
        this.addActivity({
          type: 'grade',
          title: this.editingModule ? 'Module Updated' : 'Module Added',
          description: `${this.moduleForm.name}: ${this.moduleForm.isCurrentlyEnrolled ? 'In Progress' : `${this.moduleForm.score}%`}`,
          time: 'Just now'
        });

        console.log("Module save completed successfully");

      } catch (error) {
        console.error("Unhandled error saving module:", error);
        const errorMsg = `Failed to ${this.editingModule ? 'update' : 'add'} module: ${error.response?.data?.error || error.message}`;

        if (this.isCapacitorApp()) {
          this.showNativeToast(errorMsg);
        } else {
          notify({type: "error", message: errorMsg});
        }
      } finally {
        this.loading = false;
        if (this.isMobile) this.hideLoading();
      }
    },
    async deleteModule(module) {
      // Use a confirm dialog appropriate for the platform
      let confirmed = false;

      if (this.isCapacitorApp() && window.Capacitor.Plugins.Dialog) {
        const {value} = await window.Capacitor.Plugins.Dialog.confirm({
          title: 'Confirm Deletion',
          message: `Are you sure you want to delete "${module.name}"?`,
          okButtonTitle: 'Delete',
          cancelButtonTitle: 'Cancel'
        });
        confirmed = value;
      } else {
        confirmed = confirm(`Are you sure you want to delete "${module.name}"?`);
      }

      if (confirmed) {
        if (this.isMobile) this.showLoading();

        try {
          this.loading = true;
          await axios.delete(`${API_URL}/modules/${module.id}`, {withCredentials: true});

          await this.fetchModules(); // Refresh module data
          await this.fetchDashboardData(); // Refresh dashboard stats

          const message = "Module deleted successfully!";
          if (this.isCapacitorApp()) {
            this.showNativeToast(message);
          } else {
            notify({type: "success", message: message});
          }

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
          const errorMsg = `Failed to delete module: ${error.response?.data?.error || error.message}`;

          if (this.isCapacitorApp()) {
            this.showNativeToast(errorMsg);
          } else {
            notify({type: "error", message: errorMsg});
          }
        } finally {
          this.loading = false;
          if (this.isMobile) this.hideLoading();
        }
      }
    },
    async addActivity(activityData) {
      try {
        await axios.post(
            `${API_URL}/dashboard/activity`,
            activityData,
            {withCredentials: true}
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
            {withCredentials: true}
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
            {withCredentials: true}
        );
      } catch (error) {
        console.error("Error updating dashboard config:", error);
      }
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
  --bg-light: #f8f9fa;
  --bg-card: #ffffff;
  --bg-accent: #f1f3f9;
  --bg-input: #ffffff;
  --text-primary: #333333;
  --text-secondary: #667085;
  --text-muted: #94a3b8;
  --primary-color: #7b49ff;
  --primary-dark: #6038cc;
  --primary-light: #9a73ff;
  --success-color: #22c55e;
  --info-color: #3b82f6;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --border-color: #e2e8f0;
  --border-color-light: #f1f5f9;
  --border-radius: 8px;
  --border-radius-lg: 12px;
  --transition-speed: 0.3s;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
  --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.dashboard.dark-mode {
  --bg-light: #111827;
  --bg-card: #1f2937;
  --bg-accent: #2d3748;
  --bg-input: #374151;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --primary-color: #8b5cf6;
  --primary-dark: #7c3aed;
  --primary-light: #a78bfa;
  --border-color: #374151;
  --border-color-light: #4b5563;
}

/* High contrast mode */
.high-contrast {
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

.dark-mode.high-contrast {
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

/* Animation settings */
.disable-animations * {
  transition: none !important;
  animation: none !important;
}

.reduce-motion * {
  transition-duration: 0.001s !important;
  animation-duration: 0.001s !important;
}

/* Focus mode */
.focus-mode .dashboard-content > *:not(:focus-within):not(.overview-card):not(.chart-card):not(.activity-card):not(.goals-card):not(.year-card):not(.insights-card):not(.settings-section) {
  opacity: 0.7;
  filter: grayscale(20%);
  transition: opacity 0.3s ease, filter 0.3s ease;
}

.focus-mode .dashboard-content > *:hover:not(:focus-within) {
  opacity: 0.9;
  filter: grayscale(0%);
}

.focus-mode .dashboard-header {
  opacity: 1 !important;
  filter: none !important;
}

/* Screen reader optimizations */
.screen-reader-optimized .visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.screen-reader-optimized .module-card,
.screen-reader-optimized .chart-card,
.screen-reader-optimized .activity-item,
.screen-reader-optimized .goal-item {
  position: relative;
}

/* Skip to content link for screen readers */
.screen-reader-optimized .skip-to-content {
  position: absolute;
  left: -9999px;
  z-index: 999;
  padding: 1rem;
  background-color: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 0 0 var(--border-radius) var(--border-radius);
}

.screen-reader-optimized .skip-to-content:focus {
  left: 50%;
  transform: translateX(-50%);
  top: 0;
}

/* Accessibility focus indicators */
.screen-reader-optimized button:focus-visible,
.screen-reader-optimized input:focus-visible,
.screen-reader-optimized select:focus-visible,
.screen-reader-optimized a:focus-visible {
  outline: var(--focus-outline);
  outline-offset: 2px;
  position: relative;
  z-index: 1;
}

/* Enhanced focus outlines for keyboard navigation */
.screen-reader-optimized .module-card:focus-within,
.screen-reader-optimized .chart-card:focus-within,
.screen-reader-optimized .activity-item:focus-within,
.screen-reader-optimized .goal-item:focus-within {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

/* Font size adjustments based on setting */
:root {
  --font-size-base: 16px;
}

.dashboard-main-content {
  font-size: var(--font-size-base);
}

/* Small font size */
.dashboard-main-content.font-small {
  --font-size-base: 14px;
}

.dashboard-main-content.font-small h1 {
  font-size: 1.6rem;
}

.dashboard-main-content.font-small h2 {
  font-size: 1.3rem;
}

.dashboard-main-content.font-small h3 {
  font-size: 1.1rem;
}

.dashboard-main-content.font-small .grade-value {
  font-size: 2.25rem;
}

/* Medium font size - default */
.dashboard-main-content.font-medium {
  --font-size-base: 16px;
}

/* Large font size */
.dashboard-main-content.font-large {
  --font-size-base: 18px;
}

.dashboard-main-content.font-large h1 {
  font-size: 2rem;
}

.dashboard-main-content.font-large h2 {
  font-size: 1.7rem;
}

.dashboard-main-content.font-large h3 {
  font-size: 1.4rem;
}

.dashboard-main-content.font-large .grade-value {
  font-size: 3rem;
}

.dashboard-main-content.font-large .module-card,
.dashboard-main-content.font-large .activity-item,
.dashboard-main-content.font-large .goal-item {
  padding: 1.5rem;
}

/* Responsive modifications for increased font sizes */
@media (max-width: 768px) {
  .dashboard-main-content.font-large .visualization-row,
  .dashboard-main-content.font-large .bottom-row {
    grid-template-columns: 1fr;
  }

  .dashboard-main-content.font-large .modules-grid {
    grid-template-columns: 1fr;
  }
}

/* Calendar display based on settings */
.hide-week-numbers .fc-week-number {
  display: none !important;
}

.hide-completed .fc-event.completed {
  display: none !important;
}

.highlight-today .fc-day-today {
  background-color: rgba(var(--primary-color-rgb), 0.1) !important;
  border: 1px solid var(--primary-color) !important;
}

/* Time format adjustments for calendar */
.time-format-24h .fc-event-time {
  /* Styles for 24h time format in calendar */
}

.time-format-12h .fc-event-time {
  /* Styles for 12h time format in calendar */
}

/* Enhanced color coding for grading scale from settings */
.grading-scale-custom .excellent-score {
  color: var(--custom-excellent-color, #2ecc71);
}

.grading-scale-custom .good-score {
  color: var(--custom-good-color, #3498db);
}

.grading-scale-custom .average-score {
  color: var(--custom-average-color, #f1c40f);
}

.grading-scale-custom .pass-score {
  color: var(--custom-pass-color, #e67e22);
}

.grading-scale-custom .fail-score {
  color: var(--custom-fail-color, #e74c3c);
}

/* Custom module icon classes based on grading scale */
.grading-scale-custom .module-icon.excellent {
  background: linear-gradient(135deg, var(--custom-excellent-color, #2ecc71), var(--custom-excellent-dark, #27ae60));
}

.grading-scale-custom .module-icon.good {
  background: linear-gradient(135deg, var(--custom-good-color, #3498db), var(--custom-good-dark, #2980b9));
}

.grading-scale-custom .module-icon.average {
  background: linear-gradient(135deg, var(--custom-average-color, #f1c40f), var(--custom-average-dark, #f39c12));
}

.grading-scale-custom .module-icon.pass {
  background: linear-gradient(135deg, var(--custom-pass-color, #e67e22), var(--custom-pass-dark, #d35400));
}

.grading-scale-custom .module-icon.fail {
  background: linear-gradient(135deg, var(--custom-fail-color, #e74c3c), var(--custom-fail-dark, #c0392b));
}

.dashboard-layout {
  display: flex;
  flex-direction: row;
  position: relative;
  padding-top: 70px; /* Space for fixed navbar */
  min-height: calc(100vh - 70px);
  font-family: var(--font-main);
}

/* ========== Main Content Styles ========== */
.dashboard-main-content {
  flex: 1;
  padding: 2rem;
  transition: all var(--transition-speed) ease;
  background-image: linear-gradient(to bottom, rgba(248, 250, 252, 0.8), rgba(241, 245, 249, 0.4));
}

.dark-mode .dashboard-main-content {
  background-image: linear-gradient(to bottom, rgba(17, 24, 39, 0.8), rgba(31, 41, 55, 0.4));
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
  font-weight: 700;
  color: var(--primary-dark);
  margin: 0;
  letter-spacing: -0.5px;
  position: relative;
}

.dashboard-header h1::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 40px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.dark-mode .dashboard-header h1 {
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
  border: 1px solid var(--border-color-light);
}

.view-controls button {
  padding: 0.5rem 1.25rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.view-controls button.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 2px 8px rgba(123, 73, 255, 0.25);
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
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.3);
  transition: all 0.2s ease;
  z-index: 10;
}

.toggle-text {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-toggle:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(123, 73, 255, 0.4);
}

.sidebar-show-button {
  position: fixed;
  right: 2rem;
  top: 6rem;
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.3);
}

/* Ensure button is visible and clickable */
button.sidebar-show-button:not([disabled]) {
  cursor: pointer;
  pointer-events: auto !important;
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
  border: 1px solid var(--border-color-light);
}

.auth-card svg {
  color: var(--primary-color);
  filter: drop-shadow(0 2px 4px rgba(123, 73, 255, 0.2));
}

.auth-card h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-dark);
  letter-spacing: -0.5px;
}

.auth-card p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.5;
}

.login-button {
  display: inline-block;
  background: var(--primary-color);
  color: white;
  padding: 0.75rem 1.75rem;
  border-radius: 24px;
  text-decoration: none;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(123, 73, 255, 0.25);
  transition: all 0.2s ease;
}

.login-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(123, 73, 255, 0.35);
}

/* ========== Wizard Styles ========== */
.wizard-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 2.5rem;
  box-shadow: var(--shadow-md);
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
  transition: all var(--transition-speed) ease;
  border: 1px solid var(--border-color-light);
}

.wizard-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.step-indicator {
  display: inline-block;
  background-color: var(--primary-color);
  color: white;
  padding: 0.3rem 0.9rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  box-shadow: 0 2px 6px rgba(123, 73, 255, 0.2);
}

.wizard-header h2 {
  margin: 0 0 0.75rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary-dark);
  letter-spacing: -0.5px;
}

.wizard-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1.05rem;
  line-height: 1.5;
}

/* ========== Form Styling ========== */
.form-group {
  margin-bottom: 1.75rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.required {
  color: var(--danger-color);
  margin-left: 3px;
}

.form-group input[type="number"],
.form-group input[type="text"] {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  transition: all var(--transition-speed) ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.form-group input[type="number"]:focus,
.form-group input[type="text"]:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.form-group select {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  background-color: var(--bg-input);
  color: var(--text-primary);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.85rem center;
  background-size: 16px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.form-group select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.select-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  justify-content: center;
  margin-bottom: 1.25rem;
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
}

.select-btn:hover {
  border-color: var(--primary-color);
  background: rgba(123, 73, 255, 0.05);
  color: var(--primary-color);
  transform: translateY(-2px);
}

.select-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.2);
}

.btn-icon {
  font-size: 1.15rem;
}

/* ========== Year Weights Styles ========== */
.year-weights-container {
  margin-bottom: 2.25rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  background-color: var(--bg-card);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.year-weights-header {
  display: flex;
  background-color: var(--bg-accent);
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
  background-color: rgba(123, 73, 255, 0.03);
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
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
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
  background-color: var(--bg-accent);
  border-top: 1px solid var(--border-color);
  color: var(--success-color);
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
  margin-top: 1.75rem;
  padding: 0.85rem 1.75rem;
  font-weight: 600;
  font-size: 0.95rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.25s ease;
  width: 100%;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 12px rgba(123, 73, 255, 0.25);
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(123, 73, 255, 0.35);
}

.save-button:disabled {
  background-color: var(--text-muted);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.button-group {
  display: flex;
  gap: 1.25rem;
  margin-top: 1.75rem;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem 1.75rem;
  font-weight: 600;
  font-size: 0.95rem;
  background-color: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.25s ease;
}

.back-button:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: translateY(-2px);
}

/* ========== Dashboard Overview Tab ========== */
.dashboard-overview {
  display: flex;
  flex-direction: column;
  gap: 2.25rem;
}

.overview-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(to right, var(--bg-card), rgba(123, 73, 255, 0.05));
}

.overview-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-dark);
  letter-spacing: -0.5px;
  position: relative;
}

.overview-header h2::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.time-filters {
  display: flex;
  gap: 0.5rem;
  background: var(--bg-card);
  border-radius: 20px;
  padding: 0.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color-light);
}

.time-filters button {
  padding: 0.4rem 0.85rem;
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
  box-shadow: 0 2px 6px rgba(123, 73, 255, 0.25);
}

.time-filters button:hover:not(.active) {
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
}

.overview-body {
  padding: 1.75rem;
}

.grade-summary {
  display: flex;
  align-items: center;
  gap: 3.5rem;
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
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
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
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--primary-dark);
  line-height: 1;
  letter-spacing: -1px;
}

.grade-label {
  position: relative;
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.35rem;
  font-weight: 500;
}

.grade-stats {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  flex: 1;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1.25rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.25s ease;
  border-left: 3px solid var(--primary-color);
}

.stats-item:hover {
  transform: translateX(5px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.stats-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.stats-value {
  font-weight: 700;
  color: var(--primary-dark);
  font-size: 1.1rem;
}

/* ========== Progress Section ========== */
.progress-section {
  margin-top: 2.5rem;
  background: var(--bg-accent);
  padding: 1.5rem;
  border-radius: var(--border-radius);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.progress-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.progress-legend {
  display: flex;
  gap: 1.25rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.legend-color {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.progress-bar {
  display: flex;
  height: 2.75rem;
  border-radius: var(--border-radius);
  overflow: hidden;
  margin-bottom: 1.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-segment {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
  transition: width 0.5s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.progress-segment.achieved {
  background: linear-gradient(to right, #2ecc71, #27ae60);
}

.progress-segment.lost {
  background: linear-gradient(to right, #3498db, #2980b9);
}

.progress-segment.remaining {
  background: linear-gradient(to right, #ecf0f1, #bdc3c7);
  color: var(--text-secondary);
  text-shadow: none;
}

.progress-targets {
  display: flex;
  justify-content: space-between;
  gap: 1.25rem;
}

.target-item {
  flex: 1;
  text-align: center;
  padding: 1.25rem;
  background: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border-top: 3px solid transparent;
  transition: all 0.25s ease;
}

.target-item:nth-child(1) {
  border-top-color: #2ecc71;
}

.target-item:nth-child(2) {
  border-top-color: #3498db;
}

.target-item:nth-child(3) {
  border-top-color: #f1c40f;
}

.target-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.target-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--primary-dark);
  margin-bottom: 0.5rem;
  letter-spacing: -0.5px;
}

.target-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* ========== Visualization Row ========== */
.visualization-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.25rem;
}

.chart-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin: 0 0 1.25rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  position: relative;
  display: inline-block;
}

.chart-card h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.chart-container {
  height: 320px;
  position: relative;
}

.large-chart .chart-container {
  height: 370px;
}

/* ========== Bottom Row ========== */
.bottom-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2.25rem;
}

/* ========== Activity Card ========== */
.activity-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.activity-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.activity-card h3 {
  margin: 0 0 1.25rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  position: relative;
  display: inline-block;
}

.activity-card h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  padding: 1rem;
  border-radius: var(--border-radius);
  background: var(--bg-accent);
  transition: all 0.25s ease;
  border-left: 3px solid transparent;
}

.activity-item:hover {
  transform: translateX(5px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.activity-item.grade {
  border-left-color: #2ecc71;
}

.activity-item.submission {
  border-left-color: #3498db;
}

.activity-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
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
  margin-bottom: 0.35rem;
}

.activity-description {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.activity-time {
  font-size: 0.75rem;
  color: var(--text-muted);
  white-space: nowrap;
  font-weight: 500;
}

/* ========== Goals Card ========== */
.goals-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.goals-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.goals-card h3 {
  margin: 0 0 1.25rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  position: relative;
  display: inline-block;
}

.goals-card h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 30px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.goals-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1rem;
  border-radius: var(--border-radius);
  background: var(--bg-accent);
  transition: all 0.25s ease;
  border-left: 3px solid var(--primary-color);
}

.goal-item:hover {
  transform: translateX(5px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.goal-progress {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
}

.goal-circle {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.1));
}

.goal-circle-bg {
  fill: none;
  stroke: var(--border-color);
  stroke-width: 2.75;
}

.goal-circle-progress {
  fill: none;
  stroke: var(--primary-color);
  stroke-width: 2.75;
  stroke-linecap: round;
}

.goal-percentage {
  font-size: 10px;
  fill: var(--primary-dark);
  text-anchor: middle;
  dominant-baseline: middle;
  transform: rotate(90deg);
  font-weight: 700;
}

.goal-details {
  flex: 1;
}

.goal-title {
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.35rem;
}

.goal-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

/* ========== Yearly View Tab ========== */
.yearly-view {
  display: flex;
  flex-direction: column;
  gap: 2.25rem;
}

/* ========== Filters Row ========== */
.filters-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.25rem 1.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.filter-group label {
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.25rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.25s ease;
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.2);
}

.export-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(123, 73, 255, 0.3);
}

/* ========== Year Card ========== */
.year-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  margin-bottom: 2.25rem;
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.year-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.year-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.75rem;
  border-bottom: 1px solid var(--border-color-light);
  padding-bottom: 1.25rem;
}

.year-header h2 {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--primary-dark);
  letter-spacing: -0.5px;
}

.year-stats {
  display: flex;
  gap: 1.75rem;
}

.year-stat {
  text-align: center;
  padding: 0.5rem 1rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  min-width: 100px;
}

.stat-value {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--primary-dark);
  letter-spacing: -0.5px;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin-top: 0.2rem;
}

/* ========== Year Progress ========== */
.year-progress {
  margin-bottom: 1.75rem;
}

.year-progress-bar {
  height: 1.75rem;
  background-color: var(--bg-accent);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.progress-value {
  height: 100%;
  background: linear-gradient(to right, var(--primary-color), var(--primary-light));
  color: white;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.85rem;
  font-weight: 700;
  font-size: 0.9rem;
  transition: width 0.5s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* ========== Modules Grid ========== */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.75rem;
}

.module-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.25s ease;
  cursor: pointer;
  border: 1px solid transparent;
}

.module-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.07);
  border-color: var(--border-color);
  background: var(--bg-card);
}

.module-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  font-weight: 700;
  color: white;
  background: var(--primary-color);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  font-size: 1.1rem;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.module-icon.excellent {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.module-icon.good {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.module-icon.average {
  background: linear-gradient(135deg, #f1c40f, #f39c12);
}

.module-icon.pass {
  background: linear-gradient(135deg, #e67e22, #d35400);
}

.module-icon.fail {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.module-details {
  flex: 1;
}

.module-name {
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.35rem;
  font-size: 1.05rem;
  display: flex;
  align-items: center;
}

/* Enrollment badge styles */
.enrolled-badge {
  display: inline-block;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: white;
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 10px;
  vertical-align: middle;
  margin-left: 8px;
  font-weight: 700;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  box-shadow: 0 1px 3px rgba(123, 73, 255, 0.3);
}

.module-info {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.module-score {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.5px;
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
  padding: 0.85rem 1.75rem;
  background: transparent;
  color: var(--primary-color);
  border: 2px dashed var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.25s ease;
  font-size: 0.95rem;
}

.add-module-button:hover {
  background: rgba(123, 73, 255, 0.05);
  transform: scale(1.05);
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.1);
}

/* ========== Insights Tab ========== */
.insights-view {
  display: flex;
  flex-direction: column;
  gap: 2.25rem;
}

/* ========== Insights Card ========== */
.insights-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.insights-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.insights-card h2 {
  margin: 0 0 1.75rem;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--primary-dark);
  letter-spacing: -0.5px;
  position: relative;
  display: inline-block;
}

.insights-card h2::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 40px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 4px;
}

.insight-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.metric-item {
  text-align: center;
  padding: 1.75rem 1.25rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.25s ease;
  border-top: 4px solid var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: help;
}

.metric-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.metric-value {
  font-size: 2.25rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
  letter-spacing: -1px;
  line-height: 1;
}

.metric-label {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  letter-spacing: -0.5px;
}

.metric-comparison {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
  line-height: 1.4;
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

/* ========== Tooltip Styles ========== */
.tooltip {
  display: block;
  z-index: 10000;
  max-width: 300px;
}

.tooltip .tooltip-inner {
  background: var(--bg-card);
  color: var(--text-primary);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  line-height: 1.5;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--border-color);
}

.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: var(--bg-card);
}

.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

/* ========== Insights Charts ========== */
.insights-charts {
  display: flex;
  flex-direction: column;
  gap: 2.25rem;
}

.small-charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.25rem;
}

/* ========== Insights Tips ========== */
.insights-tips {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.insights-tips:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.tips-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-top: 1.75rem;
}

.tip-card {
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  padding: 1.5rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  transition: all 0.25s ease;
  border-left: 4px solid var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.tip-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
  background: linear-gradient(to right, var(--bg-accent), rgba(123, 73, 255, 0.05));
}

.tip-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(123, 73, 255, 0.1);
  color: var(--primary-color);
  flex-shrink: 0;
  box-shadow: 0 3px 8px rgba(123, 73, 255, 0.15);
}

.tip-content h4 {
  margin: 0 0 0.75rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.25px;
}

.tip-content p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ========== Prediction Scenarios ========== */
.insights-prediction {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: 1.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.insights-prediction:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.prediction-scenarios {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.75rem;
}

.scenario-card {
  text-align: center;
  padding: 1.75rem;
  border-radius: var(--border-radius);
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: help;
}

.scenario-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
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
  margin: 0 0 1.25rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.25px;
}

.scenario-grade {
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--primary-dark);
  margin-bottom: 1.25rem;
  letter-spacing: -1px;
  line-height: 1;
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
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
  font-weight: 500;
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
  backdrop-filter: blur(5px);
}

.dialog-content {
  background: var(--bg-card);
  border-radius: var(--border-radius-lg);
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(to right, var(--bg-card), rgba(123, 73, 255, 0.05));
}

.dialog-header h2 {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--primary-dark);
  letter-spacing: -0.5px;
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
  transform: rotate(90deg);
}

.module-info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  padding: 1.75rem;
}

.info-item {
  background: var(--bg-accent);
  padding: 1.25rem;
  border-radius: var(--border-radius);
  text-align: center;
  transition: all 0.2s ease;
  border-top: 3px solid transparent;
}

.info-item:nth-child(1) { border-top-color: #3498db; }
.info-item:nth-child(2) { border-top-color: #2ecc71; }
.info-item:nth-child(3) { border-top-color: #f1c40f; }
.info-item:nth-child(4) { border-top-color: #e67e22; }
.info-item:nth-child(5) { border-top-color: #9b59b6; }
.info-item:nth-child(6) { border-top-color: #1abc9c; }

.info-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.info-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.info-value {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.info-value.score {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.5px;
}

/* Enrollment status indicator */
.enrollment-status {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  background-color: #e0e0e0;
  color: #666;
}

.enrollment-status.active {
  background-color: rgba(46, 204, 113, 0.2);
  color: #27ae60;
  box-shadow: 0 1px 3px rgba(46, 204, 113, 0.2);
}

.dialog-content h3 {
  margin: 0;
  padding: 0 1.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-top: 1.5rem;
  letter-spacing: -0.25px;
}

.assessments-table {
  padding: 1.75rem;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1.25rem;
}

.table-header {
  font-weight: 700;
  color: var(--text-primary);
  padding-bottom: 0.85rem;
  border-bottom: 2px solid var(--border-color);
  margin-bottom: 0.85rem;
}

.table-row {
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--border-color-light);
  align-items: center;
  transition: background-color 0.2s ease;
}

.table-row:hover {
  background-color: rgba(123, 73, 255, 0.03);
}

.table-row:last-child {
  border-bottom: none;
}

.table-cell {
  padding: 0.6rem 0;
}

.module-charts {
  padding: 1.75rem;
}

.module-chart {
  margin-bottom: 1.75rem;
  background: var(--bg-accent);
  padding: 1.25rem;
  border-radius: var(--border-radius);
}

.module-chart h4 {
  margin: 0 0 1.25rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.25px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1.25rem;
  padding: 1.75rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-accent);
}

.edit-button,
.delete-button,
.cancel-button {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.85rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-size: 0.95rem;
}

.edit-button {
  background: var(--primary-color);
  color: white;
  border: none;
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.25);
}

.edit-button:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(123, 73, 255, 0.35);
}

.delete-button {
  background: transparent;
  color: #e74c3c;
  border: 1px solid #e74c3c;
}

.delete-button:hover {
  background: rgba(231, 76, 60, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(231, 76, 60, 0.15);
}

.cancel-button {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.cancel-button:hover {
  background: var(--bg-accent);
  transform: translateY(-2px);
}

/* ========== Module Form ========== */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  padding: 1.75rem;
}

.assessments-form {
  padding: 1.75rem;
  background: var(--bg-accent);
  margin: 0 1.75rem;
  border-radius: var(--border-radius);
}

.assessment-row {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
  padding: 1rem;
  background: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.assessment-row:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.07);
}

.assessment-inputs {
  flex: 1;
  display: flex;
  gap: 1.25rem;
}

.assessment-inputs input[type="text"] {
  flex: 2;
  padding: 0.85rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-input);
  color: var(--text-primary);
  font-size: 0.95rem;
}

.assessment-inputs input[type="text"]:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.assessment-numbers {
  flex: 1;
  display: flex;
  gap: 0.6rem;
}

.assessment-numbers input {
  flex: 1;
  padding: 0.85rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-input);
  color: var(--text-primary);
  font-size: 0.95rem;
}

.assessment-numbers input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.15);
}

.assessment-numbers input:disabled {
  background: var(--bg-accent);
  color: var(--text-muted);
  cursor: not-allowed;
}

.assessment-status {
  display: flex;
  align-items: center;
  padding: 0 0.5rem;
}

.assessment-status .checkbox-container {
  margin: 0;
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
  border-radius: 50%;
}

.remove-assessment:hover {
  background: rgba(231, 76, 60, 0.1);
  transform: scale(1.1);
}

.add-assessment {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  margin-top: 1.25rem;
  padding: 0.85rem 1.5rem;
  background: transparent;
  color: var(--primary-color);
  border: 2px dashed var(--primary-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.25s ease;
  font-size: 0.95rem;
}

.add-assessment:hover {
  background: rgba(123, 73, 255, 0.05);
  transform: scale(1.05);
  box-shadow: 0 3px 10px rgba(123, 73, 255, 0.1);
}

.total-weight-indicator {
  padding: 1rem 1.75rem 1.75rem;
  text-align: right;
  font-weight: 600;
  color: var(--success-color);
}

.total-weight-indicator.weight-error {
  color: var(--warning-color);
}

/* ========== Enrollment Checkbox Styling ========== */
.enrollment-checkbox {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1rem;
  background: var(--bg-accent);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--primary-color);
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

.checkbox-container input[type="checkbox"] {
  margin-right: 8px;
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--primary-color);
}

.checkbox-label {
  font-weight: 600;
  color: var(--text-primary);
}

.field-hint {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  line-height: 1.4;
}

/* ========== Mobile Optimizations ========== */
/* Base adjustments for mobile devices */
@media (max-width: 768px) {
  .dashboard {
    /* Use full viewport space */
    padding: 0;
    overflow-x: hidden;
  }

  .dashboard-layout {
    flex-direction: column;
    padding-top: 60px; /* Smaller navbar height for mobile */
  }

  .dashboard-main-content {
    padding: 0.75rem;
    width: 100%;
    max-width: 100%;
    margin: 0;
  }

  /* Adjust header for mobile */
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
    padding: 0.5rem;
  }

  .dashboard-header h1 {
    font-size: 1.5rem;
    width: 100%;
  }

  .view-controls {
    width: 100%;
    overflow-x: auto;
    justify-content: flex-start;
    padding: 0.25rem 0;
  }

  .view-controls button {
    padding: 0.35rem 0.75rem;
    font-size: 0.8rem;
    white-space: nowrap;
  }

  /* Overview tab adjustments */
  .dashboard-overview {
    gap: 1rem;
  }

  .overview-card {
    margin-bottom: 1rem;
  }

  .overview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
  }

  .time-filters {
    width: 100%;
    overflow-x: auto;
    justify-content: flex-start;
  }

  /* Grade summary adjust for mobile */
  .grade-summary {
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding: 0 0.5rem;
  }

  .grade-circle {
    width: 140px;
    height: 140px;
  }

  .grade-stats {
    width: 100%;
  }

  /* Progress section adjustments */
  .progress-section {
    padding: 1rem;
    margin-top: 1.5rem;
  }

  .progress-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .progress-legend {
    width: 100%;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .progress-targets {
    flex-direction: column;
    gap: 1rem;
  }

  .target-item {
    padding: 1rem;
  }

  /* Visualization adjustments */
  .visualization-row {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .chart-container {
    height: 250px;
  }

  /* Bottom row adjustments */
  .bottom-row {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  /* Yearly view adjustments */
  .filters-row {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    padding: 1rem;
  }

  .filter-group {
    width: 100%;
  }

  .filter-group select {
    width: 100%;
  }

  .export-button {
    width: 100%;
    justify-content: center;
  }

  .modules-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  /* Module detail dialog */
  .module-detail-dialog,
  .module-form-dialog {
    padding: 0.5rem;
  }

  .dialog-content {
    max-height: 95vh;
    width: 95%;
    padding: 0;
  }

  .dialog-header {
    padding: 1rem;
  }

  .dialog-header h2 {
    font-size: 1.3rem;
  }

  .module-info-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    padding: 1rem;
  }

  .dialog-content h3 {
    padding: 0 1rem;
    font-size: 1.1rem;
  }

  .assessments-table {
    padding: 1rem;
  }

  .table-header,
  .table-row {
    grid-template-columns: 2fr 1fr;
  }

  .table-cell:nth-child(3),
  .table-cell:nth-child(4) {
    display: none;
  }

  .dialog-actions {
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
  }

  .dialog-actions button {
    width: 100%;
  }

  /* Module form */
  .form-grid {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .assessment-inputs {
    flex-direction: column;
    gap: 0.75rem;
  }

  .assessment-numbers {
    width: 100%;
  }

  /* Insights tab */
  .insight-metrics {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .small-charts {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .tips-container {
    grid-template-columns: 1fr;
  }

  .prediction-scenarios {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  /* Touch-specific optimizations */
  .module-card,
  .select-btn,
  .save-button,
  .back-button,
  .add-module-button,
  .sidebar-toggle,
  button {
    /* Increase touch targets */
    min-height: 44px;
  }

  /* Fix button and input sizes */
  input, select, button {
    font-size: 16px !important; /* Prevent iOS zoom on focus */
  }

  /* Make sidebar fullscreen on mobile */
  .dashboard-sidebar {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: calc(100vh - 60px);
    z-index: 1000;
    border-left: none;
  }

  /* Sidebar buttons */
  .sidebar-hide-button {
    top: 0.75rem;
    right: 0.75rem;
  }

  .sidebar-show-button {
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    top: auto;
    z-index: 900;
    border-radius: 50%;
    width: 56px;
    height: 56px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  }

  .sidebar-show-button .toggle-text {
    display: none;
  }

  /* Fix for Capacitor status bar */
  .ios .dashboard-layout {
    padding-top: 75px; /* Extra padding for iOS status bar */
  }

  .android .dashboard-layout {
    padding-top: 65px; /* Extra padding for Android status bar */
  }

  /* Ensure proper scroll behavior */
  .dashboard-main-content {
    -webkit-overflow-scrolling: touch;
  }

  /* Hide unnecessary elements on small screens */
  .dashboard-sidebar {
    display: none;
  }

  .dashboard-sidebar.visible {
    display: block;
  }

  /* Improved touch feedback */
  .select-btn:active,
  .module-card:active,
  .activity-item:active,
  .stats-item:active,
  .goal-item:active,
  .target-item:active,
  .tip-card:active {
    opacity: 0.7;
    transform: scale(0.98);
  }

  /* Fix for sticky hover states on mobile */
  @media (hover: none) {
    .select-btn:hover,
    .module-card:hover,
    .activity-item:hover,
    .stats-item:hover,
    .goal-item:hover,
    .target-item:hover,
    .tip-card:hover {
      transform: none;
      box-shadow: none;
    }
  }
}

/* Specific adjustments for very small devices */
@media (max-width: 375px) {
  .dashboard-main-content {
    padding: 0.5rem;
  }

  .grade-circle {
    width: 120px;
    height: 120px;
  }

  .grade-value {
    font-size: 2.25rem;
  }

  .view-controls button {
    padding: 0.3rem 0.6rem;
    font-size: 0.75rem;
  }

  .dashboard-header h1 {
    font-size: 1.35rem;
  }
}

/* Improvements for landscape orientation */
@media (max-width: 900px) and (orientation: landscape) {
  .grade-summary {
    flex-direction: row;
    align-items: center;
  }

  .dialog-content {
    max-height: 85vh;
  }

  .dashboard-layout {
    padding-top: 55px;
  }

  .module-info-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Capacitor-specific adjustments */
.capacitor-ios .dashboard-layout {
  /* Safe area inset for iOS notches and home indicators */
  padding-top: env(safe-area-inset-top, 60px);
  padding-bottom: env(safe-area-inset-bottom, 0);
  padding-left: env(safe-area-inset-left, 0);
  padding-right: env(safe-area-inset-right, 0);
}

.capacitor-ios .sidebar-show-button {
  bottom: calc(1rem + env(safe-area-inset-bottom, 0));
}

/* Fix for keyboard appearing */
.keyboard-open .dashboard-main-content {
  padding-bottom: 300px; /* Add extra space when keyboard is open */
}

/* Loading states for better UX on slower mobile connections */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Optimizations for pull-to-refresh */
.pull-to-refresh-indicator {
  text-align: center;
  height: 40px;
  margin-top: -40px;
  color: var(--text-secondary);
  font-size: 14px;
  padding-top: 10px;
}

/* Navigation bar adjustments for mobile */
@media (max-width: 768px) {
  .dashboard-nav-bar {
    height: 60px;
    padding: 0 1rem;
  }

  .nav-title {
    font-size: 1.1rem;
  }

  .nav-profile {
    gap: 0.5rem;
  }

  .nav-avatar {
    width: 32px;
    height: 32px;
  }

  .nav-user-info {
    display: none; /* Hide user info on mobile, keep only avatar */
  }
}
</style>