Here’s a well-structured and visually appealing README.md file with better formatting, clear sections, and improved readability:

📚 GradeHome

 

GradeHome is a university grade-tracking and calculator application designed with Azure Functions, Vue.js, and Capacitor. It includes:

✅ Session-based authentication (Azure Functions in Python + Azure Cosmos DB)
✅ Vue + Capacitor frontend (runs in a browser or as a mobile app)
✅ Google OAuth integration (optional for authentication)

📌 Table of Contents
	1.	🔧 Project Structure
	2.	🚀 Prerequisites
	3.	⚙️ Backend Setup
	4.	🌐 Frontend Setup
	5.	🔑 Environment Variables
	6.	🚀 Running the App
	7.	☁️ Deployment
	8.	📜 License

🔧 Project Structure

GradeHome/
├── backend/                   # Azure Functions backend (Python)
│   ├── function_app.py        # Main Azure Functions entry point
│   ├── user_routes.py         # Session-based authentication
│   ├── google_auth.py         # Google OAuth logic
│   ├── database.py            # Cosmos DB integration
│   ├── models.py              # Pydantic models
│   ├── requirements.txt       # Python dependencies
│   └── ...                    # Additional backend files
│
├── filter/                    # (Optional / unused if empty)
│
├── gradehome-frontend/        # Frontend (Vue + Capacitor)
│   ├── android/               # Android Capacitor project
│   ├── ios/                   # iOS Capacitor project
│   ├── public/                # Static assets
│   ├── src/                   # Vue source code
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
│   ├── vite.config.js         
│   └── ...                    # Additional configurations
│
└── .gitignore

🚀 Prerequisites

Before running GradeHome, ensure you have:

Backend Requirements
	•	Azure Functions Core Tools
	•	Python 3.9+ (3.10+ recommended) ➝ Download Python
	•	Azure Cosmos DB (or Cosmos DB Emulator) ➝ Docs

Frontend Requirements
	•	Node.js 16+ (Node.js 18 recommended)
	•	npm or yarn for managing dependencies
	•	Capacitor CLI (optional for mobile builds):

npm install -g @ionic/cli @capacitor/cli

⚙️ Backend Setup

1️⃣ Install Python Dependencies:

cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

2️⃣ Set Environment Variables:
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

3️⃣ Run the Azure Functions backend:

func start

By default, the API runs on http://localhost:7071.

🌐 Frontend Setup

1️⃣ Install Node.js Dependencies:

cd gradehome-frontend
npm install

2️⃣ Start the Development Server:

npm run dev

By default, the frontend runs on http://localhost:5173.

3️⃣ (Optional) Capacitor Setup for Mobile:

# For iOS:
npx cap add ios
npx cap open ios

# For Android:
npx cap add android
npx cap open android

# Sync changes:
npx cap sync

🔑 Environment Variables

Variable	Description	Example
COSMOS_ENDPOINT	Cosmos DB endpoint URL	https://<your-db-name>.documents.azure.com
COSMOS_KEY	Cosmos DB primary key	xxxxxx==
COSMOS_DBNAME	Your Cosmos DB name	gradehome-db
COSMOS_CONTAINER	Container for users	users
COSMOS_UNI_CONTAINER	Container for universities	universities
GOOGLE_CLIENT_ID	Google OAuth client ID	123456-abcdef.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET	Google OAuth client secret	GOCSPX-xyz
GOOGLE_REDIRECT_URI	Google OAuth callback URL	https://your-site.com/auth/google/callback
FRONTEND_REDIRECT_URL	Frontend redirect after auth success	http://localhost:5173/dashboard

🚀 Running the App

1️⃣ Start the Backend:

cd backend
func start

Runs on: http://localhost:7071

2️⃣ Start the Frontend:

cd gradehome-frontend
npm run dev

Runs on: http://localhost:5173

3️⃣ Test the App:
	•	Open http://localhost:5173/ (Landing Page)
	•	Go to http://localhost:5173/login (Login/Register)
	•	On success, a session cookie is stored by the backend
	•	Navigate to /dashboard to verify authentication

☁️ Deploying

🚀 Backend Deployment (Azure Functions)
	•	Deploy the backend to Azure Functions
	•	Configure environment variables in Azure Function App settings

🌐 Frontend Deployment
	•	For Web:

cd gradehome-frontend
npm run build

	•	Deploy the dist/ folder to a static site provider like Netlify or Azure Static Web Apps.

	•	For Mobile:

npx cap copy

	•	Open the project in Xcode (iOS) or Android Studio (Android) for final packaging.

📜 License

Licensed under the MIT License.
See LICENSE for details.

🎉 Happy coding with GradeHome!
If you have any questions, feel free to open an issue in the repository. 🚀

This version enhances readability, formatting, and aesthetics while keeping all essential details! Let me know if you need further refinements. 🚀