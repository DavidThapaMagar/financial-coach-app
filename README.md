# Financial Coach App

A simple web app that helps users understand their financial situation and get a basic action plan.

## Live Demo
🔗 https://financial-coach-app.onrender.com

## Screenshot
![App Screenshot](./screenshot.png)

## Features
- Enter income, expenses, savings, and debt
- Instant financial summary/results
- Clean currency formatting with commas
- Simple, beginner-friendly UI

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render
- **Server (prod):** Gunicorn

## Run Locally

```bash
git clone https://github.com/DavidThapaMagar/financial-coach-app.git
cd financial-coach-app
pip install -r requirements.txt
python backend/app.py
```

Then open:  
`http://127.0.0.1:5000`

## Deployment Notes
This app is deployed on Render.  
Free-tier services may sleep after inactivity and take a few seconds to wake up.
