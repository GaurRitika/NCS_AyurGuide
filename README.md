# AyurGuide - Holistic Ayurvedic Health & AI Guidance System

AyurGuide is a comprehensive, multi-service digital health platform that bridges traditional Ayurvedic wellness wisdom with modern artificial intelligence, 3D interactive visualizations, and telehealth capabilities. The system offers personalized Prakriti (Dosha) analysis, AI-driven consultation recommendations, 3D herbal and chakra energy explorations, video consultations with certified practitioners, and educational resources.

---

Documentation : https://23cse132.mintlify.site/

## Table of Contents

1. [Executive Overview](#executive-overview)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [Repository Directory Structure](#repository-directory-structure)
5. [Technology Stack](#technology-stack)
6. [Prerequisites](#prerequisites)
7. [Installation and Setup Guide](#installation-and-setup-guide)
   - [1. Auth Backend Setup](#1-auth-backend-setup)
   - [2. Python AI Backend Setup](#2-python-ai-backend-setup)
   - [3. Frontend Setup](#3-frontend-setup)
8. [API Reference](#api-reference)
9. [Environment Variables Configuration](#environment-variables-configuration)
10. [License and Credits](#license-and-credits)

---

## Executive Overview

Traditional Ayurveda relies on identifying an individual's unique biological constitution—composed of the three fundamental energies or Doshas: **Vata**, **Pitta**, and **Kapha**. AyurGuide digitizes and enhances this analytical framework through:

- **Algorithmic Dosha Scoring**: Processing comprehensive physical, mental, and lifestyle inputs to derive exact dosha percentage distributions.
- **Generative AI Consultations**: Leveraging state-of-the-art Large Language Models (LLM) tuned with Ayurvedic principles to generate custom regimen advice.
- **Immersive 3D Learning**: Interactive WebGL renderings of medicinal herbs and chakra energy systems.
- **Telehealth Integration**: Direct WebRTC video consultation booking and scheduling with verified Ayurvedic doctors.

---

## Key Features

### 1. Dosha Analysis & Assessment Engine
- Multi-dimensional questionnaire evaluating physiological characteristics, digestion, sleep patterns, and mental tendencies.
- Dynamic scoring algorithm computing precise percentage breakdowns for Vata, Pitta, and Kapha.
- Identification of primary and secondary Dosha profiles.

### 2. AI-Powered Personal Consultation
- Integration with Groq Llama 3.3 (70B) model for natural language health analysis.
- Takes into account personal medical history, existing ailments, and lifestyle factors.
- Generates tailored dietary plans, herb suggestions, and routine modifications.

### 3. Interactive 3D Herbal Remedies Explorer
- 3D interactive renders of medicinal plants using Three.js / React Three Fiber.
- Comprehensive database detailing botanical names, active constituents, doshic impacts, and traditional preparation methods.

### 4. Interactive 3D Chakra & Sacred Geometry System
- 3D visual exploration of human energetic centers (Chakras).
- Guided meditation assistance, mantra audio players, mudra visualizers, and breathing rhythm guides.

### 5. Telehealth Expert Consultation
- Schedule management and slot booking for certified Ayurvedic doctors.
- WebRTC-backed live video conferencing capability.
- Centralized medical record and prescription attachment storage.

### 6. Wellness Center Directory & Education
- Geolocation-based discovery of authentic Ayurvedic centers and Panchakarma clinics.
- Educational repository featuring structured articles, videos, and wellness guides.

---

## System Architecture

AyurGuide is structured as a modular three-tier architecture:

```
                  +--------------------------------+
                  |         React Frontend         |
                  |  (Material-UI, Three.js, Redux)|
                  +---------------+----------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  Node.js Auth Backend |                   |  Python AI Backend    |
| (Express, MongoDB)    |                   |  (FastAPI, Groq LLM)  |
+-----------------------+                   +-----------------------+
```

- **Client Tier (`Frontend`)**: Serves single-page application (SPA) with responsive Material UI design, state management with Redux Toolkit, and 3D graphics rendering via Three.js.
- **Authentication Tier (`AuthBackend`)**: Express.js microservice handling user identity, secure password hashing, JWT session tokens, and MongoDB database persistence.
- **Intelligence Tier (`PythonBackend`)**: High-performance FastAPI microservice handling heavy computational tasks, dosha analysis algorithms, and Groq LLM inference pipelines.

---

## Repository Directory Structure

```
AyurGuide/
├── AuthBackend/                # Node.js Express Authentication Microservice
│   ├── controllers/            # Request handlers (Register, Login)
│   ├── middleware/             # Auth & token validation middleware
│   ├── models/                 # MongoDB schemas (User, Profile)
│   ├── routes/                 # Express API routes
│   ├── index.js                # Server entry point
│   ├── package.json            # Node.js dependencies
│   └── .gitignore
├── Frontend/                   # React.js Single Page Application
│   ├── public/                 # Static web assets
│   ├── src/
│   │   ├── components/         # Reusable UI, Chakra 3D & Layout components
│   │   ├── pages/              # Application views (Home, Dosha, Consultation, etc.)
│   │   ├── redux/              # Redux slices and store configuration
│   │   ├── services/           # Axios API integrations
│   │   ├── styles/             # Modular CSS stylesheets
│   │   ├── App.js              # Application routing configuration
│   │   └── index.js            # React entry point
│   ├── package.json            # Frontend dependencies
│   └── .gitignore
├── PythonBackend/              # Python FastAPI AI & Recommendation Service
│   ├── app/
│   │   ├── api/                # FastAPI router definitions
│   │   ├── models/             # Pydantic data schemas
│   │   └── services/           # Dosha analyzer & Groq LLM consultation service
│   ├── main.py                 # FastAPI server runner
│   ├── requirements.txt        # Python package dependencies
│   └── .gitignore
├── .gitignore                  # Global repository gitignore
└── README.md                   # Project documentation
```

---

## Technology Stack

### Frontend
- **Framework**: React 18 (Create React App)
- **UI Components**: Material UI (MUI v5), Lucide React
- **State Management**: Redux Toolkit, React-Redux
- **3D & Graphics**: Three.js, React Three Fiber, React Three Drei
- **Routing & Communication**: React Router v6, Axios, Socket.io-client / WebRTC

### Auth Backend
- **Runtime**: Node.js (ES Modules)
- **Framework**: Express.js
- **Database**: MongoDB with Mongoose ORM
- **Security**: JSON Web Tokens (JWT), Bcrypt.js, Cookie Parser, CORS

### Python AI Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **AI / LLM Orchestration**: Groq API (`llama-3.3-70b-versatile`), Requests / LangChain
- **Validation**: Pydantic v2

---

## Prerequisites

Ensure the following tools are installed on your environment before proceeding:

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Python**: v3.9 or higher
- **MongoDB**: Active local instance or MongoDB Atlas connection URI
- **Groq API Key**: Active API key from Groq Cloud (for AI recommendations)

---

## Installation and Setup Guide

### 1. Auth Backend Setup

1. Navigate to the `AuthBackend` directory:
   ```bash
   cd AuthBackend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file inside `AuthBackend/`:
   ```env
   PORT=3000
   MONGO_URI=mongodb://localhost:27017/ayurguide
   JWT_SECRET=your_jwt_secret_key
   ```
4. Start the server:
   ```bash
   # Development mode
   npm run dev

   # Production mode
   npm start
   ```

---

### 2. Python AI Backend Setup

1. Navigate to the `PythonBackend` directory:
   ```bash
   cd PythonBackend
   ```
2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file inside `PythonBackend/`:
   ```env
   PORT=8080
   GROQ_API_KEY=your_groq_api_key_here
   ```
5. Start the FastAPI service:
   ```bash
   python main.py
   ```
   *The FastAPI server will start on `http://localhost:8080` (API documentation accessible at `http://localhost:8080/docs`).*

---

### 3. Frontend Setup

1. Navigate to the `Frontend` directory:
   ```bash
   cd Frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file inside `Frontend/`:
   ```env
   REACT_APP_AUTH_API=http://localhost:3000
   REACT_APP_AI_API=http://localhost:8080/api/v1
   ```
4. Launch the application:
   ```bash
   npm start
   ```
   *The application will open in your default browser at `http://localhost:3000`.*

---

## API Reference

### Auth Service (`http://localhost:3000`)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/auth/register` | `POST` | Registers a new user with FullName, Email, and Password. |
| `/auth/login` | `POST` | Authenticates user credentials and returns JWT token & HTTP-only cookie. |

### AI & Analytics Service (`http://localhost:8080/api/v1`)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/analyze-dosha` | `POST` | Evaluates submitted characteristics and returns Vata/Pitta/Kapha percentages and primary dosha. |
| `/recommendations/{dosha_type}` | `GET` | Fetches targeted Ayurvedic lifestyle and dietary guidelines for a given dosha type. |
| `/personal-consultation` | `POST` | Processes personal health data, medical history, and symptoms through Groq LLM to generate custom health strategy. |

---

## Environment Variables Configuration

### `AuthBackend/.env`
```env
PORT=3000
MONGO_URI=<your_mongodb_connection_string>
JWT_SECRET=<your_jwt_secret>
```

### `PythonBackend/.env`
```env
PORT=8080
GROQ_API_KEY=<your_groq_api_key>
```

### `Frontend/.env`
```env
REACT_APP_AUTH_API=http://localhost:3000
REACT_APP_AI_API=http://localhost:8080/api/v1
```

---

## License and Credits

Developed and maintained by **Ritika Gaur** & the **NCS AyurGuide Project Team**.

For questions, issues, or contributions, please refer to the official repository at [GitHub - GaurRitika/NCS_AyurGuide](https://github.com/GaurRitika/NCS_AyurGuide).
