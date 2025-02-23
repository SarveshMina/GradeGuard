GradeHome

GradeHome is a university grade‐tracking and calculator application. It provides:
	•	A session-based authentication backend using Azure Functions (Python) + Azure Cosmos DB.
	•	A Vue + Capacitor frontend that can be deployed as a web app or packaged as a mobile app.

Table of Contents
	1.	Project Structure
	2.	Prerequisites
	3.	Backend Setup
	4.	Frontend Setup
	5.	Environment Variables
	6.	Running the App
	7.	Deploying
	8.	License

Project Structure

GradeHome/
│
├── backend/              # Azure Functions backend (Python)
│   ├── function_app.py   # Main entry point (Azure Functions)
│   ├── user_routes.py    # Session-based auth routes
│   ├── google_auth.py    # Google OAuth logic
│   ├── database.py       # Cosmos DB logic
│   ├── models.py         # Pydantic models
│   ├── requirements.txt  # Python dependencies
│   └── ...               # Other function files, etc.
│
├── filter/               # (Optional/unused folder if not relevant)
│
├── gradehome-frontend/   # Frontend (Vue + Capacitor)
│   ├── android/          # Android Capacitor project
│   ├── ios/              # iOS Capacitor project
│   ├── public/           # Public assets
│   ├── src/              # Vue source code
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
│   ├── vite.config.js    # Vite config
│   └── ...               # Additional config (Capacitor, etc.)
│
└── .gitignore

Prerequisites
	•	Azure Functions Core Tools (for local backend testing)
Installation docs
	•	Python 3.9+ (or 3.10/3.11/3.12, as you prefer)
Download Python
	•	Node.js 14+ (preferably Node 16 or 18)
Download Node.js
	•	npm or yarn (package manager for the frontend)
	•	Cosmos DB (or an emulator) for local or remote testing
Cosmos DB Emulator Docs
	•	Capacitor CLI if you plan to build mobile apps (npm install -g @ionic/cli @capacitor/cli)

Backend Setup
	1.	Install Python dependencies

cd backend
python -m venv venv       # create a virtual environment (optional but recommended)
source venv/bin/activate  # or "venv\Scripts\activate" on Windows

pip install -r requirements.txt


	2.	Set environment variables (see Environment Variables)
Example (on Windows PowerShell):

$env:COSMOS_ENDPOINT="https://your-cosmos-url/"
$env:COSMOS_KEY="your-cosmos-key"
$env:COSMOS_DBNAME="gradehome-db"
$env:COSMOS_CONTAINER="users"
$env:COSMOS_UNI_CONTAINER="universities"
$env:GOOGLE_CLIENT_ID="your-google-oauth-client-id"
$env:GOOGLE_CLIENT_SECRET="your-google-oauth-client-secret"
$env:GOOGLE_REDIRECT_URI="https://your-site.com/auth/google/callback"
$env:FRONTEND_REDIRECT_URL="http://localhost:5173/dashboard"


	3.	Run the Azure Functions backend locally

func start

By default, it listens on http://localhost:7071.
	Note: If you see an error about “cannot find module,” ensure your requirements.txt is updated and that all necessary packages are installed.

Frontend Setup
	1.	Install Node.js dependencies

cd gradehome-frontend
npm install

(or yarn install if you prefer yarn)

	2.	Development server

npm run dev

By default, Vite will serve the app at http://localhost:5173. If your environment variables in the backend’s FRONTEND_REDIRECT_URL or Google OAuth references are set, ensure they match.

	3.	(Optional) Capacitor Setup
If you plan to build for iOS/Android:

# iOS
npx cap add ios
npx cap open ios   # opens Xcode
# Android
npx cap add android
npx cap open android

Then run npx cap sync whenever you change web code.

Environment Variables

Backend environment variables:
	•	COSMOS_ENDPOINT
Your Cosmos DB endpoint URL.
	•	COSMOS_KEY
The primary key for your Cosmos DB.
	•	COSMOS_DBNAME
Name of your Cosmos database.
	•	COSMOS_CONTAINER
The container name for users (e.g., “users”).
	•	COSMOS_UNI_CONTAINER
The container name for universities (e.g., “universities”).
	•	GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
For Google OAuth 2.0 integration.
	•	FRONTEND_REDIRECT_URL
Where Google auth callback will redirect after success (e.g., http://localhost:5173/dashboard).

Make sure these are set in your local environment or in your hosting environment (e.g., Azure).

Running the App
	1.	Start the backend

cd backend
func start

This runs on http://localhost:7071 by default.

	2.	Start the frontend

cd gradehome-frontend
npm run dev

The Vue app is now at http://localhost:5173.

	3.	Test
	•	Visit http://localhost:5173/login or your landing page http://localhost:5173/.
	•	Attempt to register/login. The backend should set a session cookie upon success.
	•	Navigate to the dashboard. The app calls protected endpoints, which will succeed if the session is valid.

Deploying
	•	Backend
Deploy your Azure Functions project (backend/) to Azure (or your chosen environment). Make sure your environment variables (Cosmos, Google OAuth, etc.) are set in the Azure Function App settings.
	•	Frontend
	•	For a web build: npm run build inside gradehome-frontend/ produces a production build in dist/.
	•	Host the dist/ folder on your static hosting (e.g. Azure Static Web Apps, Netlify, Vercel, etc.).
	•	For mobile apps: use npx cap copy ios/android then open in Xcode/Android Studio. Adjust your server URLs as needed.

License

This project is available under the MIT License (or any license you prefer). See LICENSE for details.

Happy coding with GradeHome! If you have questions or issues, feel free to open an issue in the repository.