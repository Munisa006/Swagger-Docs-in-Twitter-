## Swagger Docs in Twitter

FastAPI backend for a Twitter-like API with auth, posts, likes, and follows.

### Requirements

- Python 3.13
- A virtual environment
- Environment variables in `app/.env` or `.env`

### Environment variables

Create one of these files:

- `.env`
- `app/.env`

Add these values:

```env
DATABASE_URL=sqlite:///./twitter.db
SECRET_KEY=change-me-to-a-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run locally

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Open the docs at:

```text
http://127.0.0.1:8000/docs
```
  
