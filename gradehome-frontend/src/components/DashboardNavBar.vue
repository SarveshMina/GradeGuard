<template>
  <div>
    <!-- Desktop Navbar -->
    <header 
      v-if="!isMobile" 
      class="desktop-navbar"
      :class="{ 'navbar-scrolled': isScrolled }"
    >
      <div class="navbar-container">
        <div class="navbar-left">
          <router-link to="/dashboard" class="brand-logo">
            <div class="logo-inner">
              <span class="logo-icon">
                <svg viewBox="0 0 24 24" class="shield-icon" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span class="logo-text">GradeGuard</span>
            </div>
          </router-link>

          <nav class="desktop-nav-links">
            <router-link 
              v-for="(link, index) in navLinks" 
              :key="index"
              :to="link.path" 
              class="nav-link-item"
              :class="{ 'active': $route.path === link.path }"
              v-slot="{ isActive, href, navigate }"
            >
              <a 
                :href="href" 
                @click="navigate"
                class="nav-link-inner"
              >
                <span class="link-icon" :class="{ 'active': isActive }">
                  <!-- Home Icon -->
                  <svg v-if="link.icon === 'home'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                  </svg>
                  
                  <!-- Study Icon -->
                  <svg v-if="link.icon === 'study'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                  </svg>
                  
                  <!-- Calendar Icon -->
                  <svg v-if="link.icon === 'calendar'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  
                  <!-- Settings Icon -->
                  <svg v-if="link.icon === 'settings'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                  </svg>
                </span>
                <span class="link-text">{{ link.name }}</span>
                <span class="link-indicator" :class="{ 'active': isActive }"></span>
              </a>
            </router-link>
          </nav>
        </div>

        <div class="navbar-right">
          <div class="notification-bell" @click="toggleNotifications">
            <div class="notification-indicator" :class="{ 'has-notifications': hasNotifications }"></div>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div>
          
          <div class="theme-toggle-wrapper">
            <button 
              @click="toggleDarkMode" 
              class="theme-toggle-button"
              :class="{ 'is-dark': darkMode }"
              aria-label="Toggle dark mode"
            >
              <div class="toggle-track">
                <div class="toggle-icon">
                  <svg v-if="darkMode" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                  </svg>
                </div>
              </div>
            </button>
          </div>

          <div class="user-profile" ref="userProfileDropdown">
            <button 
              @click="toggleUserMenu" 
              class="user-profile-button"
              :class="{ 'menu-open': showUserMenu }"
            >
              <div class="user-avatar">
                <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
                <div v-else class="avatar-placeholder">{{ userInitials }}</div>
              </div>
              <div class="user-info">
                <span class="user-name">{{ userName }}</span>
                <span class="user-role">Student</span>
              </div>
              <div class="dropdown-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
            </button>

            <transition name="dropdown-fade">
              <div v-if="showUserMenu" class="user-dropdown">
                <div class="user-dropdown-header">
                  <div class="dropdown-user-info">
                    <div class="dropdown-avatar">
                      <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
                      <div v-else class="avatar-placeholder">{{ userInitials }}</div>
                    </div>
                    <div class="dropdown-user-details">
                      <span class="dropdown-user-name">{{ userName }}</span>
                      <span class="dropdown-user-email">{{ userEmail }}</span>
                    </div>
                  </div>
                </div>

                <div class="user-dropdown-body">
                  <router-link @click="showUserMenu = false" to="/profile" class="dropdown-menu-item">
                    <div class="dropdown-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                      </svg>
                    </div>
                    <span class="dropdown-text">My Profile</span>
                  </router-link>

                  <router-link @click="showUserMenu = false" to="/settings" class="dropdown-menu-item">
                    <div class="dropdown-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="3"></circle>
                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                      </svg>
                    </div>
                    <span class="dropdown-text">Account Settings</span>
                  </router-link>

                  <router-link @click="showUserMenu = false" to="/grades" class="dropdown-menu-item">
                    <div class="dropdown-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                      </svg>
                    </div>
                    <span class="dropdown-text">My Grades</span>
                  </router-link>

                  <div class="dropdown-divider"></div>

                  <button @click="handleLogout" class="dropdown-menu-item logout-btn">
                    <div class="dropdown-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                      </svg>
                    </div>
                    <span class="dropdown-text">Logout</span>
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Layout -->
    <div v-if="isMobile" class="mobile-layout">
      <!-- Mobile Top Bar -->
      <div class="mobile-top-bar" :class="{ 'scrolled': isScrolled }">
        <div class="mobile-top-container">
          <router-link to="/dashboard" class="mobile-logo">
            <div class="mobile-logo-inner">
              <span class="mobile-logo-icon">
                <svg viewBox="0 0 24 24" class="shield-icon" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span class="mobile-logo-text">GradeGuard</span>
            </div>
          </router-link>
          
          <div class="mobile-controls">
            <div class="mobile-notification-bell" @click="toggleNotifications">
              <div class="notification-indicator" :class="{ 'has-notifications': hasNotifications }"></div>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
              </svg>
            </div>
            
            <button @click="toggleDarkMode" class="mobile-theme-toggle" :class="{ 'is-dark': darkMode }" aria-label="Toggle dark mode">
              <div class="mobile-toggle-icon">
                <svg v-if="darkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
              </div>
            </button>
            
            <div class="mobile-profile-button" @click="toggleUserMenu">
              <div class="mobile-avatar">
                <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
                <div v-else class="avatar-placeholder">{{ userInitials }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Mobile User Dropdown -->
        <transition name="mobile-dropdown">
          <div v-if="showUserMenu" class="mobile-user-dropdown">
            <div class="mobile-dropdown-header">
              <div class="mobile-dropdown-user">
                <div class="mobile-dropdown-avatar">
                  <img v-if="userAvatar" :src="userAvatar" alt="User avatar" />
                  <div v-else class="avatar-placeholder large">{{ userInitials }}</div>
                </div>
                <div class="mobile-dropdown-details">
                  <span class="mobile-dropdown-name">{{ userName }}</span>
                  <span class="mobile-dropdown-email">{{ userEmail }}</span>
                </div>
              </div>
            </div>
            
            <div class="mobile-dropdown-menu">
              <router-link @click="showUserMenu = false" to="/profile" class="mobile-menu-item">
                <div class="mobile-menu-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <span class="mobile-menu-text">My Profile</span>
              </router-link>
              
              <router-link @click="showUserMenu = false" to="/settings" class="mobile-menu-item">
                <div class="mobile-menu-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                  </svg>
                </div>
                <span class="mobile-menu-text">Account Settings</span>
              </router-link>
              
              <router-link @click="showUserMenu = false" to="/grades" class="mobile-menu-item">
                <div class="mobile-menu-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                </div>
                <span class="mobile-menu-text">My Grades</span>
              </router-link>
              
              <div class="mobile-dropdown-divider"></div>
              
              <button @click="handleLogout" class="mobile-menu-item logout-btn">
                <div class="mobile-menu-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                    <polyline points="16 17 21 12 16 7"></polyline>
                    <line x1="21" y1="12" x2="9" y2="12"></line>
                  </svg>
                </div>
                <span class="mobile-menu-text">Logout</span>
              </button>
            </div>
          </div>
        </transition>
      </div>

      <!-- Mobile Bottom Navigation -->
      <div :class="['mobile-bottom-nav', { 'nav-collapsed': isNavCollapsed }]">
        <div class="mobile-nav-content">
          <router-link 
            v-for="(link, index) in navLinks" 
            :key="index"
            :to="link.path" 
            class="mobile-nav-item"
            :class="{ 'active': $route.path === link.path }"
            v-slot="{ isActive, href, navigate }"
          >
            <a 
              :href="href" 
              @click="navigate"
              class="mobile-nav-link"
            >
              <div class="mobile-nav-icon" :class="{ 'active': isActive }">
                <!-- Home Icon -->
                <svg v-if="link.icon === 'home'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                  <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
                
                <!-- Study Icon -->
                <svg v-if="link.icon === 'study'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                
                <!-- Calendar Icon -->
                <svg v-if="link.icon === 'calendar'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                
                <!-- Settings Icon -->
                <svg v-if="link.icon === 'settings'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                </svg>
              </div>
              <div class="mobile-nav-text" :class="{ 'hidden': isNavCollapsed }">
                {{ link.name }}
              </div>
            </a>
          </router-link>
          
          <div class="float-action-button">
            <button @click="handleFloatAction" class="fab-button">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="16"></line>
                <line x1="8" y1="12" x2="16" y2="12"></line>
              </svg>
            </button>
          </div>
        </div>
        
        <button class="collapse-toggle" @click="toggleNavCollapse">
          <svg v-if="isNavCollapsed" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="13 17 18 12 13 7"></polyline>
            <polyline points="6 17 11 12 6 7"></polyline>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="11 17 6 12 11 7"></polyline>
            <polyline points="18 17 13 12 18 7"></polyline>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Notification Panel - Shown when notifications are toggled -->
    <transition name="panel-slide">
      <div v-if="showNotifications" class="notification-panel">
        <div class="notification-panel-header">
          <h3 class="notification-title">Notifications</h3>
          <button @click="showNotifications = false" class="close-panel-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="notification-list">
          <div v-if="notifications.length === 0" class="empty-notifications">
            <div class="empty-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
              </svg>
            </div>
            <p class="empty-text">You have no new notifications</p>
          </div>
          
          <div v-else class="notification-items">
            <div 
              v-for="(notification, index) in notifications" 
              :key="index"
              class="notification-item"
              :class="{ 'unread': !notification.read }"
            >
              <div class="notification-dot" v-if="!notification.read"></div>
              <div class="notification-icon" :class="notification.type">
                <svg v-if="notification.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <svg v-else-if="notification.type === 'warning'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <div class="notification-content">
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-time">{{ notification.time }}</div>
              </div>
              <button @click="markAsRead(index)" class="mark-read-button" v-if="!notification.read">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <div class="notification-panel-footer">
          <button @click="clearAllNotifications" class="clear-all-button">
            Clear All
          </button>
          <button @click="markAllAsRead" class="mark-all-button">
            Mark All as Read
          </button>
        </div>
      </div>
    </transition>
    
    <!-- Backdrop for mobile dropdown -->
    <transition name="backdrop-fade">
      <div v-if="showUserMenu && isMobile" class="mobile-backdrop" @click="showUserMenu = false"></div>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { getDarkModePreference, toggleDarkMode } from '@/services/darkModeService.js';

export default {
  name: "DashboardNavBar",
  props: {
    userName: {
      type: String,
      default: 'Student Name',
    },
    userEmail: {
      type: String,
      default: 'student@example.com',
    },
    userAvatar: {
      type: String,
      default: '',
    },
    isMobile: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      darkMode: getDarkModePreference(),
      showUserMenu: false,
      showNotifications: false,
      isNavCollapsed: localStorage.getItem('navCollapsed') === 'true' || false,
      isScrolled: false,
      hasNotifications: true,
      notifications: [
        {
          type: 'success',
          message: 'You scored an A+ in Mathematics',
          time: '2 hours ago',
          read: false
        },
        {
          type: 'info',
          message: 'New assignment posted in Chemistry',
          time: '1 day ago',
          read: false
        },
        {
          type: 'warning',
          message: 'Quiz reminder: Biology quiz tomorrow',
          time: '2 days ago',
          read: true
        }
      ],
      navLinks: [
        { name: 'Dashboard', path: '/dashboard', icon: 'home' },
        { name: 'Study Hub', path: '/study', icon: 'study' },
        { name: 'Calendar', path: '/calendar', icon: 'calendar' },
        { name: 'Settings', path: '/settings', icon: 'settings' }
      ]
    }
  },
  computed: {
    userInitials() {
      if (!this.userName) return 'S';

      const names = this.userName.split(' ');
      if (names.length === 1) return names[0].charAt(0).toUpperCase();

      return (names[0].charAt(0) + names[names.length - 1].charAt(0)).toUpperCase();
    }
  },
  mounted() {
    // Initialize dark mode state
    this.darkMode = getDarkModePreference();

    // Set up scroll listener
    window.addEventListener('scroll', this.handleScroll);
    
    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', this.onDarkModeChange);

    // Add click outside listener for user dropdown
    document.addEventListener('click', this.handleClickOutside);

    // Add keyboard listener for accessibility
    document.addEventListener('keydown', this.handleKeyDown);

    // Add iOS safe area padding for mobile
    if (this.isMobile) {
      document.body.classList.add('has-mobile-nav');
      this.checkSafeAreaSupport();
    }
  },
  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('scroll', this.handleScroll);
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    document.removeEventListener('click', this.handleClickOutside);
    document.removeEventListener('keydown', this.handleKeyDown);
    
    document.body.classList.remove('has-mobile-nav');
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = toggleDarkMode();
    },
    onDarkModeChange(event) {
      this.darkMode = event.detail.isDark;
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
      if (this.showUserMenu) {
        this.showNotifications = false;
      }
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
      if (this.showNotifications) {
        this.showUserMenu = false;
      }
      this.hasNotifications = false;
    },
    handleLogout() {
      // Clear local storage or cookies used for authentication
      localStorage.removeItem("user");
      localStorage.removeItem("token");

      // Close menus
      this.showUserMenu = false;
      this.showNotifications = false;

      // Emit event so parent components can react
      this.$emit('logout');
    },
    toggleNavCollapse() {
      this.isNavCollapsed = !this.isNavCollapsed;
      localStorage.setItem('navCollapsed', this.isNavCollapsed);
    },
    handleFloatAction() {
      // Handle floating action button click
      // Can be customized based on your app's needs
      this.$emit('fabClick');
    },
    markAsRead(index) {
      this.notifications[index].read = true;
    },
    markAllAsRead() {
      this.notifications.forEach(notification => {
        notification.read = true;
      });
    },
    clearAllNotifications() {
      this.notifications = [];
      this.showNotifications = false;
    },
    // Event handling for scroll detection
    handleScroll() {
      this.isScrolled = window.scrollY > 10;
    },
    // Click outside handlers
    handleClickOutside(event) {
      // For desktop dropdown
      if (this.$refs.userProfileDropdown && !this.$refs.userProfileDropdown.contains(event.target) && !event.target.closest('.notification-panel')) {
        this.showUserMenu = false;
      }

      // Close notification panel if clicking outside
      if (this.showNotifications && !event.target.closest('.notification-bell') && !event.target.closest('.notification-panel') && !event.target.closest('.mobile-notification-bell')) {
        this.showNotifications = false;
      }
    },
    // Keyboard event handling for accessibility
    handleKeyDown(event) {
      if (event.key === 'Escape') {
        this.showUserMenu = false;
        this.showNotifications = false;
      }
    },
    // Utility function to check for iOS safe area support
    checkSafeAreaSupport() {
      const div = document.createElement('div');
      div.style.paddingBottom = 'env(safe-area-inset-bottom)';
      document.body.appendChild(div);

      const supportsSafeArea = window.getComputedStyle(div).paddingBottom !== 'env(safe-area-inset-bottom)';
      if (supportsSafeArea) {
        document.body.classList.add('supports-safe-area');
      }

      document.body.removeChild(div);
    }
  },
  watch: {
    // Watch for mobile changes to update body class
    isMobile(newVal) {
      if (newVal) {
        document.body.classList.add('has-mobile-nav');
        this.checkSafeAreaSupport();
      } else {
        document.body.classList.remove('has-mobile-nav');
        document.body.classList.remove('supports-safe-area');
      }
    }
  }
};
</script>

<style scoped>
/* =============== Core Navbar Styles =============== */
/* Variables - these will ensure compatibility with your app */
:root {
  --primary-color: #673ab7;
  --primary-dark: #512da8;
  --primary-light: #9575cd;
  --primary-gradient: linear-gradient(135deg, #673ab7, #9575cd);
  
  --bg-light: #ffffff;
  --bg-card: #ffffff;
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-muted: #888888;
  --divider: #e0e0e0;
  --border-color: #e0e0e0;
  
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  
  --navbar-height: 70px;
  --mobile-navbar-height: 60px;
  --mobile-bottom-nav-height: 68px;
  
  --border-radius: 12px;
  --border-radius-lg: 16px;
  --transition-speed: 0.3s;
}

.dark {
  --bg-light: #1e1e1e;
  --bg-card: #272727;
  --text-primary: #ffffff;
  --text-secondary: #dadada;
  --text-muted: #9e9e9e;
  --divider: #333333;
  --border-color: #333333;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.35);
}

body.has-mobile-nav {
  padding-top: var(--mobile-navbar-height);
  padding-bottom: calc(var(--mobile-bottom-nav-height) + env(safe-area-inset-bottom, 0px));
}

/* Desktop Navbar */
.desktop-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--navbar-height);
  background-color: var(--bg-light);
  border-bottom: 1px solid var(--border-color);
  z-index: 1000;
  transition: all var(--transition-speed) ease;
  box-shadow: var(--shadow-sm);
}

.navbar-scrolled {
  box-shadow: var(--shadow-md);
  height: calc(var(--navbar-height) - 10px);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
}

.navbar-left {
  display: flex;
  align-items: center;
  height: 100%;
}

/* Brand Logo */
.brand-logo {
  text-decoration: none;
  margin-right: 3rem;
}

.logo-inner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: var(--primary-gradient);
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.2);
  color: white;
  transition: all var(--transition-speed) ease;
}

.logo-icon:hover {
  transform: translateY(-2px) rotate(5deg);
}

.shield-icon {
  width: 24px;
  height: 24px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
  transition: all var(--transition-speed) ease;
}

/* Nav Links */
.desktop-nav-links {
  display: flex;
  height: 100%;
  gap: 0.75rem;
}

.nav-link-item {
  position: relative;
  height: 100%;
  text-decoration: none;
}

.nav-link-inner {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 1.25rem;
  gap: 0.75rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--transition-speed) ease;
  position: relative;
  font-weight: 500;
}

.nav-link-inner:hover {
  color: var(--primary-color);
}

.link-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-speed) ease;
}

.nav-link-inner:hover .link-icon {
  transform: translateY(-2px);
  color: var(--primary-color);
}

.link-icon.active {
  color: var(--primary-color);
}

.link-text {
  transition: all var(--transition-speed) ease;
}

.nav-link-inner:hover .link-text {
  transform: translateY(-2px);
}

.link-indicator {
  position: absolute;
  bottom: 0;
  left: 15%;
  width: 70%;
  height: 3px;
  background: var(--primary-gradient);
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  transform: scaleX(0);
  transition: transform var(--transition-speed) ease;
  transform-origin: center;
}

.link-indicator.active {
  transform: scaleX(1);
}

.nav-link-inner:hover .link-indicator:not(.active) {
  transform: scaleX(0.4);
}

/* Navbar Right Section */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

/* Notification Bell */
.notification-bell {
  position: relative;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
  color: var(--text-secondary);
}

.notification-bell:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.notification-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background-color: transparent;
  border-radius: 50%;
  transition: all var(--transition-speed) ease;
}

.notification-indicator.has-notifications {
  background-color: #f44336;
  box-shadow: 0 0 0 3px var(--bg-card);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.4);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(244, 67, 54, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(244, 67, 54, 0);
  }
}

/* Theme Toggle Button */
.theme-toggle-wrapper {
  display: flex;
  align-items: center;
}

.theme-toggle-button {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
}

.theme-toggle-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.theme-toggle-button.is-dark {
  color: var(--primary-light);
}

.toggle-track {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-speed) ease;
}

.theme-toggle-button:hover .toggle-track {
  transform: rotate(30deg);
}

.toggle-icon {
  position: relative;
  z-index: 1;
}

/* User Profile Section */
.user-profile {
  position: relative;
}

.user-profile-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem 0.5rem 0.5rem;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 50px;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
}

.user-profile-button:hover, 
.user-profile-button.menu-open {
  background-color: rgba(103, 58, 183, 0.05);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid transparent;
  transition: all var(--transition-speed) ease;
}

.user-profile-button:hover .user-avatar,
.user-profile-button.menu-open .user-avatar {
  border-color: var(--primary-color);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
  line-height: 1.2;
}

.user-role {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.dropdown-icon {
  display: flex;
  align-items: center;
  margin-left: 0.25rem;
  color: var(--text-muted);
  transition: transform var(--transition-speed) ease;
}

.user-profile-button.menu-open .dropdown-icon {
  transform: rotate(180deg);
}

/* User Dropdown Menu */
.user-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 280px;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  overflow: hidden;
  z-index: 1001;
}

.user-dropdown-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--divider);
  background-color: var(--bg-light);
}

.dropdown-user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.dropdown-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--primary-light);
  border: 2px solid var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.dropdown-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dropdown-user-details {
  display: flex;
  flex-direction: column;
}

.dropdown-user-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.dropdown-user-email {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.user-dropdown-body {
  padding: 0.75rem;
}

.dropdown-menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.9rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: all var(--transition-speed) ease;
  margin-bottom: 0.25rem;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: inherit;
  font-size: 0.9rem;
}

.dropdown-menu-item:hover {
  background-color: rgba(103, 58, 183, 0.05);
  transform: translateX(5px);
}

.dropdown-menu-item .dropdown-icon {
  color: var(--text-secondary);
  margin-left: 0;
  transition: all var(--transition-speed) ease;
}

.dropdown-menu-item:hover .dropdown-icon {
  color: var(--primary-color);
  transform: scale(1.1);
}

.dropdown-text {
  font-weight: 500;
}

.dropdown-divider {
  height: 1px;
  background-color: var(--divider);
  margin: 0.5rem 0;
}

.logout-btn {
  color: #f44336;
}

.logout-btn .dropdown-icon {
  color: #f44336;
}

.logout-btn:hover {
  background-color: rgba(244, 67, 54, 0.1);
}

/* Dropdown animations */
.dropdown-fade-enter-active, 
.dropdown-fade-leave-active {
  transition: all var(--transition-speed) ease;
  transform-origin: top right;
}

.dropdown-fade-enter-from, 
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* Notification Panel */
.notification-panel {
  position: fixed;
  top: calc(var(--navbar-height) + 10px);
  right: 20px;
  width: 360px;
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  overflow: hidden;
  z-index: 1002;
  max-height: calc(100vh - var(--navbar-height) - 40px);
  display: flex;
  flex-direction: column;
}

.notification-panel-header {
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--divider);
  background-color: var(--bg-light);
}

.notification-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-panel-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all var(--transition-speed) ease;
}

.close-panel-button:hover {
  background-color: rgba(103, 58, 183, 0.05);
  color: var(--primary-color);
}

.notification-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem;
}

.empty-notifications {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
}

.empty-icon {
  margin-bottom: 1rem;
  opacity: 0.6;
}

.empty-text {
  text-align: center;
  font-size: 0.95rem;
}

.notification-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  background-color: var(--bg-light);
  border: 1px solid var(--border-color);
  position: relative;
  transition: all var(--transition-speed) ease;
}

.notification-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.notification-item.unread {
  border-color: var(--primary-light);
  background-color: rgba(103, 58, 183, 0.05);
}

.notification-dot {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--primary-color);
}

.notification-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon.success {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.notification-icon.warning {
  background-color: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.notification-icon.info {
  background-color: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.notification-content {
  flex: 1;
}

.notification-message {
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-size: 0.9rem;
  line-height: 1.4;
}

.notification-time {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.mark-read-button {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(103, 58, 183, 0.1);
  color: var(--primary-color);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all var(--transition-speed) ease;
}

.mark-read-button:hover {
  background-color: var(--primary-color);
  color: white;
}

.notification-panel-footer {
  display: flex;
  padding: 0.75rem;
  border-top: 1px solid var(--divider);
  gap: 0.75rem;
}

.clear-all-button, .mark-all-button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  transition: all var(--transition-speed) ease;
}

.clear-all-button {
  background-color: var(--bg-light);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.clear-all-button:hover {
  background-color: var(--divider);
}

.mark-all-button {
  background-color: var(--primary-color);
  color: white;
}

.mark-all-button:hover {
  background-color: var(--primary-dark);
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.2);
}

/* Panel animations */
.panel-slide-enter-active,
.panel-slide-leave-active {
  transition: all var(--transition-speed) ease;
  transform-origin: top right;
}

.panel-slide-enter-from,
.panel-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

/* =============== MOBILE STYLES =============== */

/* Mobile Top Bar */
.mobile-top-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--mobile-navbar-height);
  background-color: var(--bg-light);
  z-index: 1000;
  border-bottom: 1px solid var(--border-color);
  transition: all var(--transition-speed) ease;
  padding-top: env(safe-area-inset-top, 0);
  box-shadow: var(--shadow-sm);
}

.mobile-top-bar.scrolled {
  box-shadow: var(--shadow-md);
}

.mobile-top-container {
  height: 100%;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mobile-logo {
  text-decoration: none;
}

.mobile-logo-inner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mobile-logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--primary-gradient);
  border-radius: 10px;
  color: white;
}

.mobile-logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}

.mobile-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.mobile-notification-bell {
  position: relative;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  color: var(--text-secondary);
}

.mobile-notification-bell:active {
  transform: scale(0.95);
  background-color: rgba(103, 58, 183, 0.05);
  color: var(--primary-color);
}

.mobile-theme-toggle {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  color: var(--text-secondary);
}

.mobile-theme-toggle:active {
  transform: scale(0.95);
  background-color: rgba(103, 58, 183, 0.05);
  color: var(--primary-color);
}

.mobile-theme-toggle.is-dark {
  color: var(--primary-light);
}

.mobile-profile-button {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
}

.mobile-profile-button:active {
  transform: scale(0.95);
  border-color: var(--primary-color);
}

.mobile-avatar {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Mobile User Dropdown */
.mobile-user-dropdown {
  position: fixed;
  top: calc(var(--mobile-navbar-height) + env(safe-area-inset-top, 0px));
  right: 0;
  width: 80%;
  max-width: 320px;
  background-color: var(--bg-card);
  box-shadow: var(--shadow-lg);
  border-bottom-left-radius: var(--border-radius-lg);
  z-index: 1001;
  overflow: hidden;
  max-height: calc(100vh - var(--mobile-navbar-height) - var(--mobile-bottom-nav-height));
  overflow-y: auto;
  border-left: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
}

.mobile-dropdown-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--divider);
  background-color: var(--bg-light);
}

.mobile-dropdown-user {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.mobile-dropdown-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--primary-light);
  border: 2px solid var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder.large {
  font-size: 1.2rem;
}

.mobile-dropdown-details {
  display: flex;
  flex-direction: column;
}

.mobile-dropdown-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.mobile-dropdown-email {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.mobile-dropdown-menu {
  padding: 0.75rem;
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: all 0.2s ease;
  margin-bottom: 0.25rem;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-family: inherit;
  font-size: 0.95rem;
}

.mobile-menu-item:active {
  background-color: rgba(103, 58, 183, 0.05);
  transform: scale(0.98);
}

.mobile-menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.mobile-menu-text {
  font-weight: 500;
}

.mobile-dropdown-divider {
  height: 1px;
  background-color: var(--divider);
  margin: 0.5rem 0;
}

.mobile-menu-item.logout-btn {
  color: #f44336;
}

.mobile-menu-item.logout-btn .mobile-menu-icon {
  color: #f44336;
}

/* Mobile dropdown animations */
.mobile-dropdown-enter-active,
.mobile-dropdown-leave-active {
  transition: all var(--transition-speed) ease;
}

.mobile-dropdown-enter-from,
.mobile-dropdown-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Mobile backdrop */
.mobile-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  animation: fadeIn var(--transition-speed) ease;
}

.backdrop-fade-enter-active,
.backdrop-fade-leave-active {
  transition: opacity var(--transition-speed) ease;
}

.backdrop-fade-enter-from,
.backdrop-fade-leave-to {
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Mobile Bottom Navigation */
.mobile-bottom-nav {
  position: fixed;
  bottom: env(safe-area-inset-bottom, 16px);
  left: 16px;
  right: 16px;
  height: var(--mobile-bottom-nav-height);
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  z-index: 999;
  transition: all 0.5s ease;
  display: flex;
  align-items: center;
  transform: translateZ(0); /* Force hardware acceleration */
  will-change: transform, width;
  overflow: hidden;
}

.nav-collapsed {
  width: 70px;
  left: 16px;
  right: auto;
}

.mobile-nav-content {
  display: flex;
  height: 100%;
  width: 100%;
  transition: all 0.5s ease;
  position: relative;
}

.nav-collapsed .mobile-nav-content {
  flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 8px 0;
}

.mobile-nav-item {
  flex: 1;
  height: 100%;
  display: flex;
  text-decoration: none;
  transition: all var(--transition-speed) ease;
}

.nav-collapsed .mobile-nav-item {
  height: auto;
  width: 100%;
  flex: none;
}

.mobile-nav-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: var(--text-secondary);
  text-decoration: none;
  gap: 4px;
  padding: 6px 0;
  transition: all var(--transition-speed) ease;
  position: relative;
}

.mobile-nav-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 25%;
  width: 50%;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 3px 3px 0 0;
  transform: scaleX(0);
  transform-origin: center;
  transition: transform var(--transition-speed) ease;
  opacity: 0;
}

.mobile-nav-item.active .mobile-nav-link::before {
  transform: scaleX(1);
  opacity: 1;
}

.nav-collapsed .mobile-nav-link::before {
  left: 0;
  bottom: 25%;
  width: 3px;
  height: 50%;
  border-radius: 0 3px 3px 0;
}

.mobile-nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-speed) ease;
  position: relative;
  width: 24px;
  height: 24px;
}

.mobile-nav-icon.active {
  color: var(--primary-color);
}

.mobile-nav-item.active .mobile-nav-icon {
  transform: translateY(-2px);
}

.nav-collapsed .mobile-nav-item.active .mobile-nav-icon {
  transform: scale(1.15);
}

.mobile-nav-text {
  font-size: 12px;
  font-weight: 500;
  transition: all var(--transition-speed) ease;
  white-space: nowrap;
}

.mobile-nav-item.active .mobile-nav-text {
  color: var(--primary-color);
  transform: translateY(-2px);
}

.mobile-nav-text.hidden {
  opacity: 0;
  height: 0;
  margin: 0;
  transform: scale(0);
}

/* Floating Action Button */
.float-action-button {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
}

.fab-button {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary-gradient);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.3);
  cursor: pointer;
  transition: all var(--transition-speed) ease;
}

.fab-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(103, 58, 183, 0.3);
}

.fab-button:active {
  transform: scale(0.95);
}

/* Collapse Button */
.collapse-toggle {
  position: absolute;
  right: -24px;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--primary-gradient);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 10px rgba(103, 58, 183, 0.3);
  cursor: pointer;
  z-index: 3;
  transition: all var(--transition-speed) ease;
}

.collapse-toggle:active {
  transform: translateY(-50%) scale(0.95);
}

.nav-collapsed .collapse-toggle svg {
  transform: rotate(180deg);
}

/* Media query adjustments for smaller screens */
@media (max-width: 374px) {
  .mobile-bottom-nav {
    bottom: max(10px, env(safe-area-inset-bottom, 10px));
    left: 10px;
    right: 10px;
    height: 60px;
  }

  .nav-collapsed {
    width: 60px;
  }

  .mobile-nav-icon {
    width: 22px;
    height: 22px;
  }

  .mobile-nav-text {
    font-size: 11px;
  }

  .collapse-toggle {
    width: 42px;
    height: 42px;
    right: -21px;
  }

  .fab-button {
    width: 50px;
    height: 50px;
  }
  
  .mobile-controls {
    gap: 0.5rem;
  }
  
  .mobile-theme-toggle,
  .mobile-notification-bell,
  .mobile-profile-button {
    width: 34px;
    height: 34px;
  }
  
  .mobile-logo-text {
    font-size: 1.1rem;
  }
}
</style>