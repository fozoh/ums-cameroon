# Contributing to UMS Cameroon

Thank you for contributing! Follow these steps to set up a development environment.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Git

## Backend Setup

### 1. Clone and Navigate
```bash
git clone https://github.com/fozoh/ums-cameroon.git
cd ums-cameroon/backend
```

### 2. Create Virtual Environment
```bash
python3.12 -m venv ../.venv
source ../.venv/bin/activate  # On Windows: ..\.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start Dev Server
```bash
python manage.py runserver 0.0.0.0:8000
```

## Frontend Setup

### 1. Navigate to Frontend
```bash
cd ums-cameroon/frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm start
```

The frontend will run at `http://localhost:3000` and connect to the backend at `http://localhost:8000/api/`.

## Running Tests

### Backend
```bash
cd backend
python manage.py test --verbosity=2
```

### Frontend
```bash
cd frontend
npm test
```

## Code Quality

### Backend Linting
```bash
flake8 backend/students --max-line-length=120 --exclude=migrations
```

### Frontend Build
```bash
cd frontend
npm run build
```

## Git Workflow

1. Create a branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git add . && git commit -m "Feature: description"`
3. Push: `git push origin feature/your-feature`
4. Open a Pull Request on GitHub

## CI/CD

All pushes and PRs trigger GitHub Actions CI:
- Backend: migrations, tests, linting
- Frontend: tests, build

Check the [.github/workflows/ci.yml](.github/workflows/ci.yml) for details.

## Project Structure

```
ums-cameroon/
├── backend/                    # Django backend
│   ├── students/              # Main app
│   ├── ums/                   # Settings
│   ├── requirements.txt        # Python deps
│   └── manage.py
├── frontend/                  # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/                      # Documentation
├── deployment/                # Docker & deploy scripts
└── README.md
```

## API Endpoints

Base URL: `http://localhost:8000/api/`

Key endpoints:
- `POST /login/` — Student login
- `GET /ca/` — Continuous Assessment marks
- `GET /results/` — Exam results (payment required)
- `GET /health/` — Health check

Full API docs: See `docs/api_docs.html`

## Troubleshooting

### Database Issues
```bash
cd backend
python manage.py flush --noinput
python manage.py migrate
```

### Node Modules Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
- Backend: `python manage.py runserver 0.0.0.0:8001`
- Frontend: `PORT=3001 npm start`

## Questions?

Open an issue on GitHub or check the existing documentation in `docs/`.

---

Happy coding! 🚀
