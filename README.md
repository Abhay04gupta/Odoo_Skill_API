# 🔍 Odoo Skill Match API

This project provides a FastAPI backend that converts natural language queries into MongoDB queries using Google Gemini (LLM). It retrieves user IDs from a cloud MongoDB collection based on the skills they offer. It also includes a Streamlit frontend to test the API interactively.

---

## 🚀 Features

- ✅ Natural language to MongoDB query using Gemini
- ✅ MongoDB Atlas integration (cloud DB)
- ✅ FastAPI backend deployed on Render
- ✅ Streamlit frontend for interactive search
- ✅ Environment variable support

---

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – Backend API
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) – Cloud database
- [Google Gemini API](https://ai.google.dev/) – Natural language → query generator
- [Streamlit](https://streamlit.io/) – Frontend interface
- [Render](https://render.com/) – API hosting

---

## 🗂️ Project Structure

├── main.py # FastAPI app
├── requirements.txt # Dependencies
├── start.sh # Startup script for Render
├── .env # Env variables (for local use only)
├── streamlit_app.py # Frontend
├── README.md # This file
