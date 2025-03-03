<template>
  <div class="landing-container" ref="landingContainer">
    <!-- Fixed Header/Nav with backdrop blur -->
    <header class="landing-header" ref="headerRef" :class="{ 'scrolled': isScrolled }">
      <div class="logo-container">
        <div class="logo visible-logo">GradeGuard</div>
      </div>
      <nav>
        <!-- Arrow buttons for Login & Sign Up -->
        <router-link :to="{ path: '/login', query: { mode: 'login' } }" class="nav-btn">
          <span class="text">Login</span>
          <span class="hover-circle"></span>
        </router-link>

        <router-link :to="{ path: '/login', query: { mode: 'signup' } }" class="nav-btn primary">
          <span class="text">Sign Up</span>
          <svg class="arrow-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12h14"></path>
            <path d="M12 5l7 7-7 7"></path>
          </svg>
        </router-link>

        <!-- Dark mode toggle -->
        <button @click="toggleDarkMode" class="theme-toggle" aria-label="Toggle dark mode">
          <svg v-if="darkMode" class="sun-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
          <svg v-else class="moon-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
      </nav>
    </header>

    <!-- Hero Section with Animated Background -->
    <section class="hero-section" ref="heroRef">
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>

      <div class="hero-content-wrapper">
        <div class="hero-content" data-aos="fade-up">
          <h1 class="hero-title">Track, Analyze, <span class="accent">Excel</span></h1>
          <p class="hero-description">
            Your intelligent academic companion for monitoring grades, predicting outcomes, and optimizing your study journey.
          </p>
          <div class="hero-buttons">
            <router-link :to="{ path: '/login', query: { mode: 'signup' } }" class="btn-primary">
              <span class="text">Get Started</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14"></path>
                <path d="M12 5l7 7-7 7"></path>
              </svg>
            </router-link>
            <button class="btn-secondary" @click="scrollToCalcForm">
              Try Calculator
            </button>
          </div>

          <!-- Features preview -->
          <div class="features-preview">
            <div class="feature-tag">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <span>Grade Tracking</span>
            </div>
            <div class="feature-tag">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
              <span>Performance Analytics</span>
            </div>
            <div class="feature-tag">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polygon points="10 8 16 12 10 16 10 8"></polygon>
              </svg>
              <span>Smart Predictions</span>
            </div>
          </div>
        </div>

        <div class="hero-image" data-aos="fade-left" data-aos-delay="200">
          <div class="dashboard-preview">
            <div class="preview-header">
              <div class="preview-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <div class="preview-title">Student Dashboard</div>
            </div>
            <div class="preview-content">
              <!-- Simplified dashboard preview with animated chart -->
              <div class="chart-container">
                <div class="chart-header">
                  <span>Performance Trend</span>
                  <div class="chart-legend">
                    <span class="legend-dot blue"></span>
                    <span class="legend-text">Grades</span>
                    <span class="legend-dot purple"></span>
                    <span class="legend-text">Target</span>
                  </div>
                </div>
                <div class="chart-visual">
                  <div class="chart-line"></div>
                  <div class="chart-target"></div>
                  <div class="chart-bars">
                    <div class="bar" style="height: 40%"></div>
                    <div class="bar" style="height: 60%"></div>
                    <div class="bar" style="height: 45%"></div>
                    <div class="bar" style="height: 70%"></div>
                    <div class="bar" style="height: 65%"></div>
                    <div class="bar highlight" style="height: 80%"></div>
                  </div>
                </div>
              </div>
              <div class="grades-preview">
                <div class="grade-item">
                  <div class="grade-icon n">N</div>
                  <div class="grade-details">
                    <div class="grade-name">Neural Networks</div>
                    <div class="grade-credits">20 credits</div>
                  </div>
                  <div class="grade-value">84%</div>
                </div>
                <div class="grade-item">
                  <div class="grade-icon p">P</div>
                  <div class="grade-details">
                    <div class="grade-name">Database Systems</div>
                    <div class="grade-credits">10 credits</div>
                  </div>
                  <div class="grade-value">76%</div>
                </div>
                <div class="grade-item">
                  <div class="grade-icon q">Q</div>
                  <div class="grade-details">
                    <div class="grade-name">Quantum Computing</div>
                    <div class="grade-credits">10 credits</div>
                  </div>
                  <div class="grade-value">92%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="scroll-indicator" v-if="showScrollDown" @click="scrollToCalcForm">
        <div class="mouse">
          <div class="wheel"></div>
        </div>
        <div class="scroll-text">Scroll down</div>
      </div>
    </section>

    <!-- Calculator Section -->
    <section class="calculator-section" ref="statsSectionRef" data-aos="fade-up">
      <div class="section-header">
        <h2>Try Our <span class="accent">Calculator</span></h2>
        <p>Get a feel for how our grade calculator works without signing up</p>
      </div>

      <div class="calculator-container">
        <div class="calc-form">
          <h3>Quick Calculate</h3>
          <div class="form-group">
            <label for="university">Your University / College</label>
            <input type="text" id="university" v-model="university" placeholder="e.g. MIT" />
          </div>
          <div class="form-group">
            <label for="degree">Your Degree</label>
            <input type="text" id="degree" v-model="degree" placeholder="e.g. Computer Science" />
          </div>
          <button class="btn-primary" @click="handleQuickCalc">
            <span>Calculate</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"></path>
              <path d="M12 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>

        <div class="stats-card-container">
          <div class="card-tabs">
            <button :class="{ active: statsMode === 'percentage' }" @click="statsMode = 'percentage'">
              Percentage
            </button>
            <button :class="{ active: statsMode === 'gpa' }" @click="statsMode = 'gpa'">
              GPA
            </button>
          </div>

          <transition name="fade-scale" mode="out-in">
            <div class="stats-card" :key="statsMode">
              <div v-if="statsMode === 'percentage'">
                <div class="stats-header">
                  <h3>Module Performance</h3>
                  <div class="overall-grade">72% Average</div>
                </div>

                <div class="progress-container">
                  <div class="progress-label">
                    <span>Overall Progress</span>
                    <span>72%</span>
                  </div>
                  <div class="progress-bar">
                    <div class="progress-segment achieved" style="width: 72%"></div>
                    <div class="progress-segment remaining" style="width: 28%"></div>
                  </div>
                </div>

                <div class="modules-list">
                  <div class="module" v-for="m in modulesPerc" :key="m.name">
                    <div :class="['module-icon', m.colorClass]">{{ m.letter }}</div>
                    <div class="module-info">
                      <div class="module-name">{{ m.name }}</div>
                      <div class="module-credits">{{ m.credits }} credits</div>
                    </div>
                    <div class="module-grade" :class="{'highlight': m.grade !== '-'}">{{ m.grade }}</div>
                  </div>
                </div>
              </div>

              <div v-else-if="statsMode === 'gpa'">
                <div class="stats-header">
                  <h3>GPA Performance</h3>
                  <div class="overall-grade">3.7 GPA</div>
                </div>

                <div class="progress-container">
                  <div class="progress-label">
                    <span>Overall Progress</span>
                    <span>3.7/4.0</span>
                  </div>
                  <div class="progress-bar">
                    <div class="progress-segment achieved" style="width: 92%"></div>
                    <div class="progress-segment remaining" style="width: 8%"></div>
                  </div>
                </div>

                <div class="modules-list">
                  <div class="module" v-for="m in modulesGpa" :key="m.name">
                    <div :class="['module-icon', m.colorClass]">{{ m.letter }}</div>
                    <div class="module-info">
                      <div class="module-name">{{ m.name }}</div>
                      <div class="module-credits">{{ m.credits }} credits</div>
                    </div>
                    <div class="module-grade" :class="{'highlight': m.grade !== '-'}">{{ m.grade }}</div>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section" ref="featuresRef" data-aos="fade-up">
      <div class="section-header">
        <h2>Powerful <span class="accent">Features</span></h2>
        <p>Everything you need to excel in your academic journey</p>
      </div>

      <div class="features-grid">
        <div class="feature-card" data-aos="fade-up" data-aos-delay="100">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
          </div>
          <h3>Track Coursework & Exams</h3>
          <p>Easily record and monitor all your academic assignments, track deadlines, and keep your study schedule organized.</p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="150">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
            </svg>
          </div>
          <h3>Customizable Year Structure</h3>
          <p>Divide your modules into years and customize weights for each year to match your specific program requirements.</p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="200">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="20" x2="12" y2="10"></line>
              <line x1="18" y1="20" x2="18" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="16"></line>
            </svg>
          </div>
          <h3>Grade Targets & Predictions</h3>
          <p>Set academic goals, track your progress, and use our AI-powered prediction engine to forecast your final classification.</p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="250">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
          </div>
          <h3>Time Management Tools</h3>
          <p>Optimize your study time with intelligent scheduling, productivity tracking, and personalized study recommendations.</p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="300">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
          </div>
          <h3>Advanced Analytics</h3>
          <p>Gain deep insights into your academic performance through detailed visualizations, trend analysis, and personalized reports.</p>
        </div>

        <div class="feature-card" data-aos="fade-up" data-aos-delay="350">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <h3>Calendar Integration</h3>
          <p>Seamlessly connect with your university calendar to sync deadlines, classes, and important academic events.</p>
        </div>
      </div>
    </section>

    <!-- Grading Systems Section -->
    <section class="systems-section" ref="systemsRef" data-aos="fade-up">
      <div class="section-header">
        <h2>Supports All <span class="accent">Grading Systems</span></h2>
        <p>No matter where you study, we've got you covered</p>
      </div>

      <div class="systems-container">
        <div class="system-card" data-aos="fade-up" data-aos-delay="100">
          <div class="system-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </div>
          <h3>Universal Support</h3>
          <p>Works with grading systems from universities and colleges worldwide.</p>
        </div>

        <div class="system-card" data-aos="fade-up" data-aos-delay="150">
          <div class="system-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path>
              <line x1="4" y1="22" x2="4" y2="15"></line>
            </svg>
          </div>
          <h3>US GPA Calculator</h3>
          <p>Full support for US grading systems including 4.0, 4.3, and 5.0 GPA scales.</p>
        </div>

        <div class="system-card" data-aos="fade-up" data-aos-delay="200">
          <div class="system-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <h3>UK Percentage System</h3>
          <p>Handles UK-style weighted percentages and honors classifications with ease.</p>
        </div>

        <div class="system-card" data-aos="fade-up" data-aos-delay="250">
          <div class="system-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
              <path d="M2 17l10 5 10-5"></path>
              <path d="M2 12l10 5 10-5"></path>
            </svg>
          </div>
          <h3>European ECTS</h3>
          <p>Compatible with the European Credit Transfer and Accumulation System.</p>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section" data-aos="fade-up">
      <div class="cta-content">
        <h2>Ready to Excel in Your Studies?</h2>
        <p>Join thousands of students using GradeGuard to achieve academic success.</p>
        <router-link :to="{ path: '/login', query: { mode: 'signup' } }" class="btn-cta">
          <span>Get Started for Free</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12h14"></path>
            <path d="M12 5l7 7-7 7"></path>
          </svg>
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
import Footer from '@/components/Footer.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { getDarkModePreference, toggleDarkMode } from '@/services/darkModeService.js'

export default {
  name: 'Landing',
  components: { Footer },
  data() {
    return {
      darkMode: false,
      showScrollDown: true,
      isScrolled: false,
      university: '',
      degree: '',
      statsMode: 'percentage',
      modulesPerc: [
        { letter: 'N', name: 'Neural Networks', credits: 20, grade: '84%', colorClass: 'n' },
        { letter: 'P', name: 'Database Systems', credits: 10, grade: '76%', colorClass: 'p' },
        { letter: 'Q', name: 'Quantum Computing', credits: 10, grade: '-', colorClass: 'q' }
      ],
      modulesGpa: [
        { letter: 'N', name: 'Neural Networks', credits: 20, grade: 'A', colorClass: 'n' },
        { letter: 'P', name: 'Database Systems', credits: 10, grade: 'B+', colorClass: 'p' },
        { letter: 'Q', name: 'Quantum Computing', credits: 10, grade: '-', colorClass: 'q' }
      ]
    }
  },
  methods: {
    handleQuickCalc() {
      alert(`Calculating for ${this.university} - ${this.degree}...`)
    },
    toggleDarkMode() {
      this.darkMode = toggleDarkMode(); // Use the centralized toggle function
    },
    scrollToCalcForm() {
      this.$refs.statsSectionRef.scrollIntoView({ behavior: 'smooth' })
    },
    updateGradient() {
      const container = this.$refs.landingContainer;
      if (!container) return;

      // Set gradient based on dark mode state
      if (this.darkMode) {
        container.style.setProperty('--bg-gradient-from', '#1a1a2e');
        container.style.setProperty('--bg-gradient-to', '#0f0f1a');
      } else {
        container.style.setProperty('--bg-gradient-from', '#f9f9ff');
        container.style.setProperty('--bg-gradient-to', '#f0f0ff');
      }
    },
    handleScroll() {
      this.isScrolled = window.scrollY > 20;
    },
    animateChart() {
      // Animate the chart line
      gsap.to(".chart-line", {
        height: "80%",
        duration: 1.5,
        ease: "power2.out",
        delay: 0.5
      });

      // Animate the chart bars sequentially
      gsap.to(".chart-bars .bar", {
        scaleY: 1,
        duration: 0.8,
        stagger: 0.1,
        ease: "elastic.out(1, 0.5)",
        delay: 0.8
      });

      // Animate the target line
      gsap.to(".chart-target", {
        opacity: 1,
        duration: 0.5,
        delay: 1.5
      });
    }
  },
  mounted() {
    // Initialize dark mode from the service
    this.darkMode = getDarkModePreference();

    // Listen for dark mode changes from other components
    window.addEventListener('darkModeChange', (event) => {
      this.darkMode = event.detail.isDark;
      this.updateGradient();
    });

    // Add scroll listener
    window.addEventListener('scroll', this.handleScroll);

    // Initialize AOS (Animate on Scroll)
    AOS.init({
      duration: 1000,
      offset: 100,
      once: true,
      easing: 'ease-out-cubic'
    });

    // Register GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // Animate background shapes
    gsap.to('.shape-1', {
      x: '10%',
      y: '5%',
      rotation: 15,
      duration: 20,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });

    gsap.to('.shape-2', {
      x: '-15%',
      y: '-10%',
      rotation: -20,
      duration: 18,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });

    gsap.to('.shape-3', {
      x: '20%',
      y: '-5%',
      rotation: 30,
      duration: 22,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });

    gsap.to('.shape-4', {
      x: '-10%',
      y: '15%',
      rotation: -10,
      duration: 25,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });

    // Header animation on scroll
    gsap.from(this.$refs.headerRef, {
      y: -80,
      opacity: 0,
      duration: 1,
      ease: 'power3.out',
    });

    // Hero animation
    gsap.from('.hero-title', {
      y: 50,
      opacity: 0,
      duration: 1,
      ease: 'power3.out',
    });

    gsap.from('.hero-description', {
      y: 50,
      opacity: 0,
      duration: 1,
      delay: 0.2,
      ease: 'power3.out',
    });

    // Force logo visibility on page load
    this.$nextTick(() => {
      const logoElement = document.querySelector('.landing-header .logo');
      if (logoElement) {
        // Force visibility with inline styles
        logoElement.style.opacity = '1';
        logoElement.style.visibility = 'visible';

        // Set initial color based on page position
        if (window.scrollY > 20) {
          // Use gradient for scrolled state
          logoElement.style.background = 'linear-gradient(135deg, var(--primary-color), var(--accent-pink))';
          logoElement.style.webkitBackgroundClip = 'text';
          logoElement.style.backgroundClip = 'text';
          logoElement.style.webkitTextFillColor = 'transparent';
        } else {
          // Use solid color for top position
          logoElement.style.color = 'white';
          logoElement.style.background = 'none';
          logoElement.style.webkitBackgroundClip = 'initial';
          logoElement.style.backgroundClip = 'initial';
          logoElement.style.webkitTextFillColor = 'initial';
        }
      }
    });

    gsap.from('.hero-buttons', {
      y: 50,
      opacity: 0,
      duration: 1,
      delay: 0.4,
      ease: 'power3.out',
    });

    gsap.from('.features-preview', {
      y: 50,
      opacity: 0,
      duration: 1,
      delay: 0.6,
      ease: 'power3.out',
    });

    // Chart animation when in view
    ScrollTrigger.create({
      trigger: '.dashboard-preview',
      start: 'top 80%',
      onEnter: () => this.animateChart()
    });

    // Set up scroll trigger for hero section
    ScrollTrigger.create({
      trigger: '.hero-section',
      start: 'top top',
      end: 'bottom top',
      onEnter: () => { this.showScrollDown = true },
      onLeave: () => { this.showScrollDown = false },
      onEnterBack: () => { this.showScrollDown = true },
      onLeaveBack: () => { this.showScrollDown = false },
    });

    // Set initial gradient
    this.updateGradient();
  },
  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('darkModeChange', this.onDarkModeChange);
    window.removeEventListener('scroll', this.handleScroll);
  }
}
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css");
@import "aos/dist/aos.css";

/* Custom CSS Variables */
:root {
  --primary-hue: 265;
  --bg-gradient-from: #f9f9ff;
  --bg-gradient-to: #f0f0ff;

  /* Accent colors */
  --accent-blue: #4f46e5;
  --accent-purple: #9061ff;
  --accent-pink: #ec4899;

  /* Animation timings */
  --transition-fast: 0.2s;
  --transition-medium: 0.3s;
  --transition-slow: 0.5s;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.08);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
}

/* Main container */
.landing-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, var(--bg-gradient-from), var(--bg-gradient-to));
  color: var(--text-primary);
  position: relative;
  overflow-x: hidden;
  transition: all var(--transition-medium) ease;
}

/* -------------- Header/Navigation -------------- */
.landing-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2.5rem;
  background-color: transparent;
  backdrop-filter: blur(0);
  -webkit-backdrop-filter: blur(0);
  z-index: 50;
  transition: all var(--transition-medium) ease;
}

/* Logo Fix for Landing Page */
.landing-header .logo {
  font-size: 1.8rem;
  font-weight: 800;
  color: white; /* Make the logo white for better visibility on dark background */
  letter-spacing: -0.5px;
  position: relative;
  text-decoration: none;

  /* Remove gradient text styling that might be causing issues */
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
  -webkit-text-fill-color: initial;

  /* Add a text shadow for better visibility */
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);

  /* Make sure it's visible */
  display: block;
  z-index: 100;
}

/* When page scrolls, logo will switch to the gradient style */
.landing-header.scrolled .logo {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: none;
}

.landing-header.scrolled {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: var(--shadow-md);
  padding: 0.75rem 2.5rem;
}

body.dark-mode .landing-header.scrolled {
  background-color: rgba(20, 20, 30, 0.8);
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--primary-color);
  background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
  position: relative;
}

.logo::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-pink));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--transition-medium) ease;
}

.logo:hover::after {
  transform: scaleX(1);
}

nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-btn {
  position: relative;
  padding: 0.625rem 1.25rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--radius-full);
  transition: all var(--transition-medium) ease;
  overflow: hidden;
}

.nav-btn .hover-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background-color: rgba(123, 73, 255, 0.1);
  transform: translate(-50%, -50%);
  transition: width var(--transition-medium) ease-out,
  height var(--transition-medium) ease-out;
  z-index: -1;
}

.nav-btn:hover .hover-circle {
  width: 250%;
  height: 300%;
}

.nav-btn.primary {
  color: white;
  background-color: var(--primary-color);
  padding-right: 2.75rem;
  font-weight: 600;
}

.nav-btn.primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.arrow-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%) translateX(0);
  transition: transform var(--transition-medium) ease;
}

.nav-btn:hover .arrow-icon {
  transform: translateY(-50%) translateX(3px);
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  color: var(--text-primary);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all var(--transition-medium) ease;
}

.theme-toggle:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: scale(1.05);
}

.sun-icon, .moon-icon {
  transition: transform var(--transition-medium) ease, opacity var(--transition-medium) ease;
}

.theme-toggle:hover .sun-icon,
.theme-toggle:hover .moon-icon {
  transform: rotate(15deg);
}

/* -------------- Hero Section -------------- */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 6rem 2rem 4rem;
  overflow: hidden;
}

.hero-bg-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.3;
  filter: blur(50px);
}

.shape-1 {
  top: 10%;
  left: 10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, var(--accent-purple) 0%, rgba(144, 97, 255, 0) 70%);
}

.shape-2 {
  bottom: 20%;
  right: 5%;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, var(--accent-pink) 0%, rgba(236, 72, 153, 0) 70%);
}

.shape-3 {
  top: 30%;
  right: 15%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, var(--accent-blue) 0%, rgba(79, 70, 229, 0) 70%);
}

.shape-4 {
  bottom: 10%;
  left: 20%;
  width: 180px;
  height: 180px;
  background: radial-gradient(circle, var(--primary-color) 0%, rgba(123, 73, 255, 0) 70%);
}

.hero-content-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.hero-content {
  flex: 1;
  max-width: 550px;
}

.hero-title {
  font-size: 3.75rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.accent {
  color: var(--primary-color);
  position: relative;
}

.accent::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-pink));
  opacity: 0.3;
  transform: translateY(4px);
}

.hero-description {
  font-size: 1.25rem;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  background-color: var(--primary-color);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-medium) ease;
  text-decoration: none;
  box-shadow: var(--shadow-md);
}

.btn-primary svg {
  transition: transform var(--transition-medium) ease;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-primary:hover svg {
  transform: translateX(3px);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.875rem 1.75rem;
  background-color: transparent;
  color: var(--primary-color);
  font-weight: 600;
  font-size: 1rem;
  border: 2px solid var(--primary-color);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-medium) ease;
}

.btn-secondary:hover {
  background-color: rgba(123, 73, 255, 0.1);
  transform: translateY(-2px);
}

.features-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.feature-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: rgba(255, 255, 255, 0.8);
  color: var(--text-secondary);
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-medium) ease;
}

body.dark-mode .feature-tag {
  background-color: rgba(30, 30, 48, 0.8);
}

.feature-tag:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  background-color: white;
  color: var(--primary-color);
}

body.dark-mode .feature-tag:hover {
  background-color: rgba(40, 40, 64, 0.9);
}

.feature-tag svg {
  color: var(--primary-color);
}

/* Dashboard preview in hero section */
.hero-image {
  flex: 1;
  max-width: 550px;
}

.dashboard-preview {
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  transform: perspective(1000px) rotateY(-5deg) rotateX(5deg);
  transition: all var(--transition-medium) ease;
}

body.dark-mode .dashboard-preview {
  background-color: #1e1e30;
}

.dashboard-preview:hover {
  transform: perspective(1000px) rotateY(-2deg) rotateX(2deg) translateY(-5px);
  box-shadow: var(--shadow-xl), 0 20px 20px rgba(123, 73, 255, 0.2);
}

.preview-header {
  background-color: #f5f5f7;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
}

body.dark-mode .preview-header {
  background-color: #2a2a42;
  border-bottom: 1px solid #3a3a52;
}

.preview-dots {
  display: flex;
  gap: 0.375rem;
  margin-right: 1rem;
}

.preview-dots span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.preview-dots span:nth-child(1) {
  background-color: #ff605c;
}

.preview-dots span:nth-child(2) {
  background-color: #ffbd44;
}

.preview-dots span:nth-child(3) {
  background-color: #00ca4e;
}

.preview-title {
  font-weight: 500;
  font-size: 0.9rem;
  color: #888;
}

body.dark-mode .preview-title {
  color: #aaa;
}

.preview-content {
  padding: 1.5rem;
}

.chart-container {
  margin-bottom: 1.5rem;
  background-color: #f9f9fa;
  border-radius: var(--radius-md);
  padding: 1rem;
  overflow: hidden;
}

body.dark-mode .chart-container {
  background-color: #252538;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.chart-legend {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.legend-dot.blue {
  background-color: #4f46e5;
}

.legend-dot.purple {
  background-color: var(--primary-color);
}

.legend-text {
  font-size: 0.8rem;
}

.chart-visual {
  height: 120px;
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.chart-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 0;
  background: linear-gradient(to bottom, rgba(79, 70, 229, 0.2), rgba(79, 70, 229, 0));
  border-top: 2px dashed #4f46e5;
  z-index: 1;
}

.chart-target {
  position: absolute;
  bottom: 70%;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--primary-color);
  opacity: 0;
  z-index: 1;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  padding: 0 0.5rem;
  z-index: 2;
}

.bar {
  width: 12%;
  background: linear-gradient(to top, #4f46e5, #818cf8);
  border-radius: 4px 4px 0 0;
  transform-origin: bottom;
  transform: scaleY(0);
}

.bar.highlight {
  background: linear-gradient(to top, var(--primary-color), var(--primary-light));
  box-shadow: 0 0 10px rgba(123, 73, 255, 0.5);
}

.grades-preview {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.grade-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background-color: #f9f9fa;
  border-radius: var(--radius-md);
  transition: all var(--transition-medium) ease;
}

body.dark-mode .grade-item {
  background-color: #252538;
}

.grade-item:hover {
  transform: translateX(5px);
  box-shadow: var(--shadow-md);
}

.grade-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.grade-icon.n {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.grade-icon.p {
  background: linear-gradient(135deg, #ec4899, #be185d);
}

.grade-icon.q {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
}

.grade-details {
  flex: 1;
}

.grade-name {
  font-weight: 500;
  font-size: 0.9rem;
  color: var(--text-primary);
}

.grade-credits {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.grade-value {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.grade-value.highlight {
  color: var(--primary-color);
}

/* Scroll indicator */
.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all var(--transition-medium) ease;
}

.scroll-indicator:hover {
  transform: translateX(-50%) translateY(-5px);
}

.mouse {
  width: 28px;
  height: 44px;
  border: 2px solid var(--text-secondary);
  border-radius: 60px;
  position: relative;
  overflow: hidden;
}

.wheel {
  width: 4px;
  height: 8px;
  background-color: var(--primary-color);
  border-radius: 2px;
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  animation: scrollDown 2s infinite;
}

@keyframes scrollDown {
  0% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) translateY(25px);
  }
}

.scroll-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* -------------- Calculator Section -------------- */
.calculator-section {
  padding: 6rem 2rem;
  background-color: white;
  position: relative;
  z-index: 2;
}

body.dark-mode .calculator-section {
  background-color: #0f0f1a;
}

.section-header {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 4rem;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.section-header p {
  font-size: 1.125rem;
  color: var(--text-secondary);
}

.calculator-container {
  display: flex;
  gap: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

.calc-form {
  flex: 1;
  background-color: white;
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
}

body.dark-mode .calc-form {
  background-color: #1e1e30;
}

.calc-form h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: all var(--transition-medium) ease;
  background-color: #f9f9fa;
  color: var(--text-primary);
}

body.dark-mode .form-group input {
  border-color: #3a3a52;
  background-color: #252538;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 73, 255, 0.2);
}

.stats-card-container {
  flex: 1.5;
}

.card-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.card-tabs button {
  padding: 0.625rem 1.5rem;
  background-color: #f9f9fa;
  border: 1px solid #e0e0e0;
  border-radius: var(--radius-full);
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-medium) ease;
}

body.dark-mode .card-tabs button {
  background-color: #252538;
  border-color: #3a3a52;
}

.card-tabs button:hover {
  background-color: rgba(123, 73, 255, 0.05);
}

.card-tabs button.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.stats-card {
  background-color: white;
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
}

body.dark-mode .stats-card {
  background-color: #1e1e30;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.stats-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.overall-grade {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}

.progress-container {
  margin-bottom: 2rem;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.progress-bar {
  height: 12px;
  background-color: #f0f0f0;
  border-radius: var(--radius-full);
  overflow: hidden;
  display: flex;
}

body.dark-mode .progress-bar {
  background-color: #252538;
}

.progress-segment {
  height: 100%;
}

.progress-segment.achieved {
  background: linear-gradient(to right, var(--primary-color), var(--primary-light));
}

.progress-segment.remaining {
  background-color: transparent;
}

.modules-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.module {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #f9f9fa;
  border-radius: var(--radius-md);
  transition: all var(--transition-medium) ease;
}

body.dark-mode .module {
  background-color: #252538;
}

.module:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.module-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.module-info {
  flex: 1;
}

.module-name {
  font-weight: 500;
  color: var(--text-primary);
}

.module-credits {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.module-grade {
  font-weight: 700;
  font-size: 1.125rem;
  color: var(--text-primary);
}

.module-grade.highlight {
  color: var(--primary-color);
}

/* -------------- Features Section -------------- */
.features-section {
  padding: 6rem 2rem;
  background-color: #f9f9ff;
  position: relative;
}

body.dark-mode .features-section {
  background-color: #1a1a2e;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background-color: white;
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-medium) ease;
  position: relative;
  overflow: hidden;
}

body.dark-mode .feature-card {
  background-color: #1e1e30;
}

.feature-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 0;
  background: linear-gradient(to bottom, var(--primary-color), var(--accent-pink));
  transition: height var(--transition-slow) ease;
}

.feature-card:hover::before {
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: var(--shadow-xl);
}

.feature-icon {
  background: linear-gradient(135deg, rgba(123, 73, 255, 0.1), rgba(236, 72, 153, 0.1));
  color: var(--primary-color);
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  transition: all var(--transition-medium) ease;
}

.feature-card:hover .feature-icon {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
  color: white;
  transform: scale(1.1);
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.feature-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* -------------- Systems Section -------------- */
.systems-section {
  padding: 6rem 2rem;
  background-color: white;
  position: relative;
}

body.dark-mode .systems-section {
  background-color: #0f0f1a;
}

.systems-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.system-card {
  background-color: #f9f9ff;
  border-radius: var(--radius-lg);
  padding: 2rem;
  text-align: center;
  transition: all var(--transition-medium) ease;
  position: relative;
  border: 1px solid rgba(123, 73, 255, 0.1);
}

body.dark-mode .system-card {
  background-color: #1e1e30;
  border-color: rgba(123, 73, 255, 0.2);
}

.system-card:hover {
  transform: translateY(-10px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.system-icon {
  background: linear-gradient(135deg, rgba(123, 73, 255, 0.1), rgba(236, 72, 153, 0.1));
  color: var(--primary-color);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  transition: all var(--transition-medium) ease;
}

.system-card:hover .system-icon {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
  color: white;
  transform: scale(1.1);
}

.system-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.system-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* -------------- CTA Section -------------- */
.cta-section {
  padding: 6rem 2rem;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-pink));
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.3;
}

.cta-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
  margin: 0 auto;
}

.cta-section h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
}

.cta-section p {
  font-size: 1.125rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.btn-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background-color: white;
  color: var(--primary-color);
  padding: 1rem 2rem;
  border-radius: var(--radius-full);
  font-weight: 600;
  text-decoration: none;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-medium) ease;
}

.btn-cta:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-xl);
}

.btn-cta svg {
  transition: transform var(--transition-medium) ease;
}

.btn-cta:hover svg {
  transform: translateX(3px);
}

/* -------------- Responsive Styles -------------- */
@media (max-width: 1200px) {
  .hero-content-wrapper {
    padding: 0 2rem;
  }

  .hero-title {
    font-size: 3.25rem;
  }
}

@media (max-width: 992px) {
  .hero-content-wrapper {
    flex-direction: column;
    text-align: center;
    gap: 3rem;
  }

  .hero-content {
    max-width: 100%;
  }

  .hero-buttons {
    justify-content: center;
  }

  .features-preview {
    justify-content: center;
  }

  .hero-image {
    max-width: 90%;
  }

  .dashboard-preview {
    transform: perspective(1000px) rotateY(0) rotateX(0);
  }

  .calculator-container {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .landing-header {
    padding: 1rem;
  }

  .logo {
    font-size: 1.5rem;
  }

  .nav-btn {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }

  .hero-section {
    padding: 6rem 1rem 3rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-description {
    font-size: 1.125rem;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .section-header h2 {
    font-size: 2rem;
  }

  .calculator-section,
  .features-section,
  .systems-section,
  .cta-section {
    padding: 4rem 1rem;
  }

  .features-grid,
  .systems-container {
    grid-template-columns: 1fr;
  }

  .cta-section h2 {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .feature-tag {
    font-size: 0.75rem;
    padding: 0.4rem 0.75rem;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .section-header h2 {
    font-size: 1.75rem;
  }
}

/* -------------- Animations & Transitions -------------- */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity var(--transition-medium) ease, transform var(--transition-medium) ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

@keyframes floating {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
</style>