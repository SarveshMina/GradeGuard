# GradeHome &middot; ![Azure Functions](https://img.shields.io/badge/Azure%20Functions-Python-blue?logo=azurefunctions&logoColor=white) ![VueJS](https://img.shields.io/badge/Vue-Capacitor%20Frontend-4FC08D?logo=vue.js&logoColor=white)

**GradeHome** is a university grade‐tracking and calculator application. It offers:

- **Session-based authentication** using **Azure Functions** (Python) and **Azure Cosmos DB**.
- A **Vue + Capacitor** frontend that can be run as a web app or packaged into mobile apps.

---

## Table of Contents

1. [Project Structure](#project-structure)  
2. [Prerequisites](#prerequisites)  
3. [Backend Setup](#backend-setup)  
4. [Frontend Setup](#frontend-setup)  
5. [Environment Variables](#environment-variables)  
6. [Running the App](#running-the-app)  
7. [Deploying](#deploying)  
8. [License](#license)  

---

## Project Structure

GradeHome/
│
├── backend/                 # Azure Functions backend (Python)
│   ├── function_app.py      # Main Azure Functions entry point
│   ├── user_routes.py       # Session-based auth routes
│   ├── google_auth.py       # Google OAuth logic
│   ├── database.py          # Cosmos DB logic
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   └── …                  # Other function files, etc.
│
├── filter/                  # (Optional / not used if empty)
│
├── gradehome-frontend/      # Frontend (Vue + Capacitor)
│   ├── android/             # Android Capacitor project
│   ├── ios/                 # iOS Capacitor project
│   ├── public/              # Public assets
│   ├── src/                 # Vue source code
│   │   ├── assets/
│   │   ├── components/
│   │   ├── plugins/
│   │   ├── services/
│   │   ├── views/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── router.js
│   │   └── style.css
│   ├── package.json
│   ├── vite.config.js       # Vite config
│   └── …                  # Additional config (Capacitor, etc.)
│
└── .gitignore

---

## Prerequisites

- **Azure Functions Core Tools** (for local backend testing)  
  [Installation docs](https://learn.microsoft.com/azure/azure-functions/functions-run-local)

- **Python 3.9+** (3.10/3.11/3.12 are also fine)  
  [Download Python](https://www.python.org/downloads/)

- **Node.js 14+** (preferably Node 16 or 18)  
  [Download Node.js](https://nodejs.org/)

- **npm** or **yarn** (for installing frontend dependencies)

- **Azure Cosmos DB** (or a local emulator)  
  [Cosmos DB Emulator Docs](https://learn.microsoft.com/azure/cosmos-db/local-emulator)

- **Capacitor CLI** (optional if building mobile apps)  
  ```bash
  npm install -g @ionic/cli @capacitor/cli

Backend Setup
	1.	Install Python dependencies:

cd backend
python -m venv venv          # create a virtual environment
source venv/bin/activate     # or "venv\Scripts\activate" on Windows

pip install -r requirements.txt


	2.	Set environment variables (see Environment Variables below).
Example on Windows PowerShell:

$env:COSMOS_ENDPOINT="https://your-cosmos-url/"
$env:COSMOS_KEY="your-cosmos-key"
$env:COSMOS_DBNAME="gradehome-db"
$env:COSMOS_CONTAINER="users"
$env:COSMOS_UNI_CONTAINER="universities"
$env:GOOGLE_CLIENT_ID="your-google-client-id"
$env:GOOGLE_CLIENT_SECRET="your-google-client-secret"
$env:GOOGLE_REDIRECT_URI="https://your-site.com/auth/google/callback"
$env:FRONTEND_REDIRECT_URL="http://localhost:5173/dashboard"


	3.	Run the Azure Functions backend locally:

func start

By default, it listens at http://localhost:7071.

	Note: If you see an error about missing modules, ensure your requirements.txt is correct and that you have installed all dependencies.

Frontend Setup
	1.	Install Node.js dependencies:

cd gradehome-frontend
npm install

(or yarn install if you prefer Yarn)

	2.	Start the development server:

npm run dev

This typically runs at http://localhost:5173. Adjust environment variables (like FRONTEND_REDIRECT_URL) if needed.

	3.	(Optional) Capacitor Setup (for mobile):

# iOS
npx cap add ios
npx cap open ios   # opens Xcode

# Android
npx cap add android
npx cap open android

Then run npx cap sync after changing web code.

Environment Variables

Backend

Variable	Description	Example
COSMOS_ENDPOINT	Cosmos DB endpoint URL	https://<your-db-name>.documents.azure.com
COSMOS_KEY	Cosmos DB primary key	xxxxxx==
COSMOS_DBNAME	Name of your Cosmos database	gradehome-db
COSMOS_CONTAINER	Container name for users	users
COSMOS_UNI_CONTAINER	Container name for universities	universities
GOOGLE_CLIENT_ID	Google OAuth client ID	123456-abcdef.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET	Google OAuth client secret	GOCSPX-xyz
GOOGLE_REDIRECT_URI	Google OAuth callback URL	https://your-site.com/auth/google/callback
FRONTEND_REDIRECT_URL	Frontend redirect after successful Google auth	http://localhost:5173/dashboard

Running the App
	1.	Start the backend:

cd backend
func start

Runs on http://localhost:7071.

	2.	Start the frontend:

cd gradehome-frontend
npm run dev

Runs on http://localhost:5173.

	3.	Test:
	•	Go to http://localhost:5173/ (landing page).
	•	Register or Login at http://localhost:5173/login.
	•	The backend sets a session cookie upon successful login.
	•	Check protected endpoints (like /dashboard) to confirm the session works.

Deploying
	•	Backend: Deploy the backend/ Azure Functions project to Azure. Make sure your environment variables (Cosmos, Google OAuth, etc.) are configured in the Azure Function App settings.
	•	Frontend:
	•	For a web build: npm run build inside gradehome-frontend/ to produce a production build in dist/. Host the dist/ folder on a static site (Azure Static Web Apps, Netlify, etc.).
	•	For mobile: run npx cap copy to sync your web build into iOS/Android, then open in Xcode/Android Studio.

License

Licensed under the MIT License. See LICENSE for details.

Happy coding with GradeHome!
If you have any questions or issues, please open an issue in the repository.
Enjoy building your grade-tracking application!

