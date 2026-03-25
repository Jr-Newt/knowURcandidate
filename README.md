# Know Your Candidate — Kerala Election Platform

A decision-support web application for Kerala voters to explore, compare, and dynamically rank election candidates based on personal preferences.

## Project Structure

```
knowURcandidate/
├── backend/          # FastAPI API server
├── frontend/         # React + Tailwind UI
├── scraper/          # Python scrapers (Playwright)
└── data/             # Seed SQL for Supabase
```

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
# Copy .env.example to .env and add your Supabase credentials
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server proxies API requests to `localhost:8000`.

### 3. Database

1. Create a [Supabase](https://supabase.com) project
2. Run `data/seed.sql` in the Supabase SQL editor
3. Add your Supabase URL and key to `backend/.env`

## Features

- **Explore** — Browse candidates by district and constituency
- **Profiles** — View education, criminal record, assets, profession
- **Compare** — Side-by-side comparison of up to 4 candidates
- **Rank** — Dynamic ranking with adjustable weight sliders
- **News** — Recent news articles per candidate
- **Red Flags** — Criminal cases and unusual wealth highlighted

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/districts` | List all districts |
| GET | `/constituencies?district=` | Constituencies in a district |
| GET | `/candidates?district=&constituency=` | Filtered candidate list |
| GET | `/candidate/{id}` | Candidate detail |
| GET | `/candidate/{id}/news` | Candidate news |
| POST | `/rank` | Dynamic ranking with weights |

## Tech Stack

- **Backend**: Python, FastAPI, Supabase
- **Frontend**: React 18, Tailwind CSS 3, Vite
- **Scraper**: Python, Playwright, httpx
- **Database**: Supabase (PostgreSQL)