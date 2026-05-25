# Smart Market Network

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange)

## Overview

Smart Market Network is a full-stack marketplace and retail management platform designed to help local retailers manage inventory, products, and customer interactions through a scalable digital system.

The project combines a responsive frontend with a FastAPI backend architecture and is designed with future AI-powered analytics integration in mind.

This project focuses on practical implementation of:
- Full-stack development
- Backend API integration
- Deployment workflows
- Scalable project architecture
- Real-world marketplace systems

---

# Problem Statement

Small and medium-scale retailers often struggle with:

- Manual inventory tracking
- Lack of digital presence
- Poor customer management systems
- Inefficient order handling
- Difficulty analyzing sales and business growth

Smart Market Network aims to provide a centralized platform that helps businesses digitally manage their operations efficiently while preparing for future AI-driven analytics integration.

---

# Objectives

- Develop a scalable marketplace platform
- Build a clean and responsive user interface
- Create RESTful backend APIs using FastAPI
- Improve practical understanding of full-stack development
- Learn deployment workflows using cloud platforms
- Implement modular project architecture for scalability

---

# Key Features

## Marketplace Management
- Product listing interface
- Product viewing and browsing
- Organized marketplace structure
- Dynamic frontend interactions

## Inventory Handling
- Inventory management support
- Product organization workflows
- Smart tracking foundation

## Backend API System
- FastAPI-based backend architecture
- REST API integration
- Backend modularization
- API endpoint structure

## Responsive Frontend
- Responsive HTML/CSS design
- Interactive JavaScript components
- User-friendly navigation
- Mobile-friendly structure

## Deployment Support
- Render backend deployment support
- Netlify frontend deployment compatibility
- Production-ready structure

---

# Tech Stack

## Frontend Technologies
- HTML5
- CSS3
- JavaScript

## Backend Technologies
- Python
- FastAPI
- Uvicorn

## Tools & Platforms
- Git
- GitHub
- VS Code
- Render
- Netlify

---

# Project Architecture

```bash
Smart-Market-Network/
│
├── app/                    # FastAPI backend application
│   ├── main.py             # Main backend entry point
│   └── ...
│
├── frontend/               # Frontend files
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── ...
│
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment configuration
├── runtime.txt             # Runtime configuration
└── README.md
```

---

# Working Flow

1. User accesses the frontend marketplace interface
2. Frontend sends requests to FastAPI backend
3. Backend processes API requests
4. Data is returned dynamically to frontend
5. Marketplace operations are displayed to users

---

# Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Market-Network.git
```

---

## 2. Navigate to Project Folder

```bash
cd Smart-Market-Network
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

---

## 7. Run Frontend

Open:

```bash
frontend/index.html
```

Recommended:
Use VS Code Live Server extension.

---

# Deployment

## Backend Deployment (Render)

1. Push code to GitHub
2. Connect repository to Render
3. Add build command:

```bash
pip install -r requirements.txt
```

4. Add start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Frontend Deployment (Netlify)

1. Connect GitHub repository to Netlify
2. Select frontend folder
3. Deploy site

---

# Future Enhancements

- User authentication system
- JWT authorization
- Database integration
- Payment gateway integration
- AI-powered analytics dashboard
- Recommendation system
- Admin dashboard
- Cloud storage support
- Real-time notifications
- Sales prediction models

---

# Learning Outcomes

This project helped in understanding:

- Full-stack project structure
- FastAPI backend development
- REST API concepts
- Frontend-backend integration
- Deployment workflows
- Git and GitHub workflows
- Practical software project organization

---

# Challenges Faced

- Frontend-backend integration setup
- API connectivity handling
- Deployment configuration
- Managing project structure
- Environment setup and dependency management

---

# Screenshots

## Home Page
<img width="957" height="998" alt="image" src="https://github.com/user-attachments/assets/8f92e596-8f4e-42a7-9e2e-41f2a5ff367b" />


## Marketplace Interface
<img width="1050" height="623" alt="image" src="https://github.com/user-attachments/assets/816e3319-29f1-4b70-9b5a-7cd324631b22" />
<img width="1050" height="623" alt="image" src="https://github.com/user-attachments/assets/7c2882c8-293a-46f9-8f1d-21a9ced463b1" />
<img width="1050" height="624" alt="image" src="https://github.com/user-attachments/assets/2eddcbd9-ccea-4f56-9ae0-546a2fb84892" />
<img width="1919" height="1021" alt="image" src="https://github.com/user-attachments/assets/33afabc9-2873-4b1c-87f2-b833398900c7" />
<img width="1050" height="623" alt="image" src="https://github.com/user-attachments/assets/9bb916f0-7563-40f9-92f7-f32152865c4f" />
<img width="1050" height="483" alt="image" src="https://github.com/user-attachments/assets/df4e97ca-5acc-44ef-8770-c065df5f3ddf" />
<img width="1050" height="624" alt="image" src="https://github.com/user-attachments/assets/f929a017-775b-415c-a240-685dfbe399f7" />






## Backend API
<img width="1009" height="1034" alt="image" src="https://github.com/user-attachments/assets/246d7b08-b9d4-4d6a-9966-baf1f1e11e56" />


---

# Author

## Nandana Vinothkumar

Integrated M.Tech CSE (Data Science)  
VIT Vellore

### Areas of Interest
- Data Science
- AI/ML
- Full Stack Development
- Cloud & DevOps
- Backend Development

---

# GitHub Repository

Repository Link:

```bash
https://github.com/YOUR_USERNAME/Smart-Market-Network
```

---

# License
This project is developed for educational, learning, and portfolio purposes.
