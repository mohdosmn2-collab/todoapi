# To-Do API – Dockerised Flask Project

A small REST API (Flask + Gunicorn) packaged as a Docker image and published to Docker Hub.

## Project structure

```
todo-api/
├── app.py            # Flask application
├── test_app.py       # Pytest unit tests
├── requirements.txt  # Python dependencies
├── Dockerfile        # Image build instructions
├── .dockerignore     # Files excluded from the image
└── README.md
```

## API endpoints

| Method | Endpoint       | Description        |
|--------|----------------|--------------------|
| GET    | `/`            | Welcome message    |
| GET    | `/health`      | Health check       |
| GET    | `/todos`       | List all todos     |
| POST   | `/todos`       | Create (`{"title": "..."}`) |
| PUT    | `/todos/<id>`  | Update title/done  |
| DELETE | `/todos/<id>`  | Delete a todo      |

## 1. Run locally (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # run tests
python app.py                    # http://localhost:5000
```

## 2. Build and run with Docker

```bash
docker build -t todo-api:1.0 .
docker run -d -p 5000:5000 --name todo-api todo-api:1.0
```

Test it:

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/todos \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn Docker"}'
curl http://localhost:5000/todos
```

Stop and remove: `docker stop todo-api && docker rm todo-api`

## 3. Push the image to Docker Hub

Replace `<your-username>` with your Docker Hub username.

**Step 1 – Create an account.** Sign up at https://hub.docker.com.

**Step 2 – (Optional) Create a repository.** Docker Hub → *Repositories* → *Create repository* → name it `todo-api` (public). Pushing also auto-creates it.

**Step 3 – Log in from the terminal.**

```bash
docker login
```

Enter your username and password (or a Personal Access Token from Account Settings → Security).

**Step 4 – Tag the image with your username.**

```bash
docker tag todo-api:1.0 <your-username>/todo-api:1.0
docker tag todo-api:1.0 <your-username>/todo-api:latest
```

**Step 5 – Push it.**

```bash
docker push <your-username>/todo-api:1.0
docker push <your-username>/todo-api:latest
```

**Step 6 – Verify.** Open `https://hub.docker.com/r/<your-username>/todo-api` and check the tags.

**Step 7 – Test by pulling on a clean machine.**

```bash
docker rmi <your-username>/todo-api:1.0        # remove local copy
docker run -d -p 5000:5000 <your-username>/todo-api:1.0
curl http://localhost:5000/health
```

## Useful commands

| Task                  | Command                         |
|-----------------------|---------------------------------|
| List images           | `docker images`                 |
| List running containers | `docker ps`                   |
| View logs             | `docker logs todo-api`          |
| Log out of Docker Hub | `docker logout`                 |

## Troubleshooting

- **`denied: requested access to the resource is denied`** – the tag doesn't start with your username, or you aren't logged in. Re-run `docker tag` and `docker login`.
- **Port already in use** – use `-p 8080:5000` and open `http://localhost:8080`.
