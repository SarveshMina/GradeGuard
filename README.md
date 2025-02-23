# GradeHome

> A versatile university grade-tracking and calculator application built with **Azure Functions**, **Vue.js**, and **Capacitor**.

![Azure Functions](https://img.shields.io/badge/Azure%20Functions-Python%203.9%2B-blue.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green.svg)
![Capacitor](https://img.shields.io/badge/Capacitor-Mobile%20App-orange.svg)

GradeHome includes:
- ✅ Session-based authentication (Azure Functions in Python + Azure Cosmos DB)  
- ✅ Vue + Capacitor frontend (runs in a browser or as a mobile app)  
- ✅ Optional Google OAuth integration  

---

## Table of Contents
1. [Project Structure](#project-structure)  
2. [Prerequisites](#prerequisites)  
3. [Backend Setup](#backend-setup)  
4. [Frontend Setup](#frontend-setup)  
5. [Environment Variables](#environment-variables)  
6. [Running the App](#running-the-app)  
7. [Deployment](#deployment)  
8. [License](#license)

---

## Project Structure

```
GradeHome/
├── backend/                # Azure Functions backend (Python)
│   ├── function_app.py     # Main Azure Functions entry point
│   ├── user_routes.py      # Session-based authentication
│   ├── google_auth.py      # Google OAuth logic
│   ├── database.py         # Cosmos DB integration
│   ├── models.py           # Pydantic models
│   ├── requirements.txt    # Python dependencies
│   └── ...                 # Additional backend files
│
├── filter/                 # (Optional / unused if empty)
│
├── gradehome-frontend/     # Frontend (Vue + Capacitor)
│   ├── android/            # Android Capacitor project
│   ├── ios/                # iOS Capacitor project
│   ├── public/             # Static assets
│   ├── src/                # Vue source code
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
│   └── ...                 # Additional configs
│
└── .gitignore
```

---

## Prerequisites

### Backend Requirements
- [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local)  
- Python 3.9+ (3.10+ recommended) → [Download Python](https://www.python.org/downloads/)  
- Azure Cosmos DB or Cosmos DB Emulator → [Docs](https://learn.microsoft.com/azure/cosmos-db/)

### Frontend Requirements
- Node.js 16+ (Node.js 18 recommended)  
- npm or yarn for dependency management  
- Capacitor CLI (optional for mobile builds):
```bash
npm install -g @ionic/cli @capacitor/cli
```

---

## Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Set environment variables** (example on Windows PowerShell):
   ```powershell
   $env:COSMOS_ENDPOINT="https://your-cosmos-url/"
   $env:COSMOS_KEY="your-cosmos-key"
   $env:COSMOS_DBNAME="gradehome-db"
   $env:COSMOS_CONTAINER="users"
   $env:COSMOS_UNI_CONTAINER="universities"
   $env:GOOGLE_CLIENT_ID="your-google-client-id"
   $env:GOOGLE_CLIENT_SECRET="your-google-client-secret"
   $env:GOOGLE_REDIRECT_URI="https://your-site.com/auth/google/callback"
   $env:FRONTEND_REDIRECT_URL="http://localhost:5173/dashboard"
   ```

3. **Run the Azure Functions backend**:
   ```bash
   func start
   ```
   - By default, the API runs on [http://localhost:7071](http://localhost:7071).

---

## Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd gradehome-frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```
   - The frontend runs on [http://localhost:5173](http://localhost:5173).

3. *(Optional)* **Capacitor setup for mobile**:
   ```bash
   # For iOS:
   npx cap add ios
   npx cap open ios

   # For Android:
   npx cap add android
   npx cap open android

   # Sync changes:
   npx cap sync
   ```

---

## Environment Variables

| Variable             | Description                           | Example                                         |
|----------------------|---------------------------------------|-------------------------------------------------|
| `COSMOS_ENDPOINT`    | Cosmos DB endpoint URL                | `https://<your-db-name>.documents.azure.com`    |
| `COSMOS_KEY`         | Cosmos DB primary key                 | `xxxxxx==`                                      |
| `COSMOS_DBNAME`      | Your Cosmos DB name                   | `gradehome-db`                                  |
| `COSMOS_CONTAINER`   | Container for users                   | `users`                                         |
| `COSMOS_UNI_CONTAINER` | Container for universities          | `universities`                                  |
| `GOOGLE_CLIENT_ID`   | Google OAuth client ID                | `123456-abcdef.apps.googleusercontent.com`      |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret          | `GOCSPX-xyz`                                    |
| `GOOGLE_REDIRECT_URI` | Google OAuth callback URL            | `https://your-site.com/auth/google/callback`    |
| `FRONTEND_REDIRECT_URL` | Frontend redirect after auth success | `http://localhost:5173/dashboard`               |

---

## Running the App

1. **Start the backend**:
   ```bash
   cd backend
   func start
   ```
   - Runs on: [http://localhost:7071](http://localhost:7071).

2. **Start the frontend**:
   ```bash
   cd gradehome-frontend
   npm run dev
   ```
   - Runs on: [http://localhost:5173](http://localhost:5173).

3. **Test the app**:
   - Open [http://localhost:5173/](http://localhost:5173/) (Landing Page)
   - Go to [http://localhost:5173/login](http://localhost:5173/login) (Login/Register)
   - On success, a session cookie is stored by the backend
   - Navigate to `/dashboard` to verify authentication

---

## Deployment

### 1. Backend Deployment (Azure Functions)
- Deploy the backend to Azure Functions.  
- Configure environment variables in the Azure Function App settings.

### 2. Frontend Deployment
- **For Web**:
   ```bash
   cd gradehome-frontend
   npm run build
   ```
   - Deploy the `dist/` folder to a static site provider (Netlify, Azure Static Web Apps, etc.).

- **For Mobile**:
   ```bash
   npx cap copy
   ```
   - Open the project in Xcode (iOS) or Android Studio (Android) for final packaging.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

> **Happy coding with GradeHome!**  
> If you have any questions, feel free to open an issue in the repository. 