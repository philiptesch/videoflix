# 🎬 Videoflix

**Videoflix** is a modern video streaming platform that allows users to register, authenticate, and stream videos in multiple resolutions.

Authentication is securely handled using **JWT (JSON Web Tokens)**, and video delivery is based on **HLS (HTTP Live Streaming)** using `.m3u8` playlists and segmented media files.

---

## 🚀 Features

* User registration and email-based account activation
* Secure JWT authentication (login, logout, token refresh)
* Password reset functionality
* Protected API endpoints
* Video streaming in multiple resolutions (360p, 480p, 720p, 1080p)
* HLS streaming with segmented video delivery
* Adaptive bitrate streaming for smooth playback

---

## 🛠️ Tech Stack

* **Backend:** Django 6 & Django REST Framework, Python 3.12
* **Authentication:** JWT (HttpOnly Cookies)
* **Streaming Protocol:** HLS
* **Database:** PostgreSQL / SQLite
* **Web Server:** Gunicorn, Whitenoise

### Required Libraries

asgiref==3.11.1
click==8.3.1
colorama==0.4.6
croniter==6.0.0
Django==6.0.2
django-cors-headers==4.9.0
django-redis==6.0.0
django-rq==3.2.2
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
gunicorn==25.0.1
packaging==26.0
psycopg2-binary==2.9.11
PyJWT==2.11.0
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
pytz==2025.2
redis==7.1.0
rq==2.6.1
six==1.17.0
sqlparse==0.5.5
tzdata==2025.3
whitenoise==6.11.0

---

## 🔐 Authentication

Videoflix uses **cookie-based JWT authentication**:

* **Access Token** → HttpOnly cookie for authorized API requests
* **Refresh Token** → HttpOnly cookie for renewing expired access tokens

Example request (browser automatically includes cookies):

```http
GET /api/protected-endpoint HTTP/1.1
Host: api.videoflix.com
Cookie: access_token=<access_token>; refresh_token=<refresh_token>
```

Renew access token via `/api/token/refresh/`.

---

## 🎥 Video Streaming

* Videos delivered via **HLS**
* Client requests `.m3u8` playlist for selected video and resolution
* Playlist contains references to multiple video segments
* Video segments streamed sequentially
* Adaptive bitrate ensures smooth playback

### Supported Resolutions

* 360p, 480p, 720p, 1080p

---

## ⚙️ Installation & Setup (Docker)

Create a `.env` file in the project root directory (or copy it from `.env.example` if provided):

```
ENV=development
DEBUG=True
```

> ⚠️ Note: This project is built using Docker, so the `.env` file is required for the Docker build process.

Clone the repository and start Docker containers:

```bash
git clone <repository_url>
cd <repository_name>
docker-compose up --build
```

## ▶️ Running the Project (Docker)

### 1️⃣ Prerequisites

- Docker Desktop installed  
- Docker Desktop running on your machine  

> ⚠️ No local Python virtual environment is required; Docker handles everything.

---

### 2️⃣ Build and Start Docker Containers

Run the following command in the project root:

```bash
docker-compose up --build
```

Docker will automatically handle:

The Python environment

Installing all dependencies

Starting the Django application

Running Redis and PostgreSQL containers

3️⃣ Access the Application

Once containers are running, the API will be available at:

```bash
http://127.0.0.1:8000/
```
You can also access the Django Admin panel at:

```bash
http://127.0.0.1:8000/admin/
```
4️⃣ Windows Users: Line Ending Fix (CRLF → LF)

When cloning the project on Windows, Git may automatically convert line endings in shell scripts (backend.entrypoint.sh) to CRLF. This can cause the backend container to fail with:

exec ./backend.entrypoint.sh: no such file or directory
videoflix_backend exited with code 255

Fix:

Open backend.entrypoint.sh in VS Code

Click on the CRLF indicator in the bottom right corner

Select LF

Save the file (Ctrl + S)

Restart Docker containers:
```bash
docker-compose up --build
```


5️⃣ Optional: Running Tests

To run tests inside the Docker container:

docker-compose exec web python manage.py test

Access API at: `http://127.0.0.1:8000/`

**Windows users:** ensure line endings of `backend.entrypoint.sh` are LF (not CRLF).

---

## 🧪 Testing

Run tests:

```bash
python manage.py test
```

---

## 📄 API Endpoints

### User Authentication

**POST /api/register/**
Registers a new user.

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "confirmed_password": "securepassword"
}
```

* Status: 201 Created
* Sends activation email

**GET /api/activate/<uidb64>/<token>/**
Activate user account.

**POST /api/login/**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

* Status: 200 OK
* Sets HttpOnly cookies: access_token & refresh_token

**POST /api/logout/**
Logs out user, invalidates refresh token.

* Status: 200 OK
* Deletes cookies

**POST /api/token/refresh/**

* Provides new access token using refresh token cookie
* Status: 200 OK

**POST /api/password_reset/**

```json
{
  "email": "user@example.com"
}
```

* Sends password reset email

**POST /api/password_confirm/<uidb64>/<token>/**

* Confirms and resets password

### Video Streaming

**GET /api/video/**

* Returns list of all available videos
* Status: 200 OK

**GET /api/video/[int:movie_id](int:movie_id)/[str:resolution](str:resolution)/index.m3u8**

* Returns HLS master playlist for selected video and resolution
* Status: 200 OK

**GET /api/video/[int:movie_id](int:movie_id)/[str:resolution](str:resolution)/[str:segment](str:segment)/**

* Returns specific HLS video segment
* Status: 200 OK

---

## 🤝 Contributing

Contributions are welcome! Open an issue or submit a pull request.

---

## 📄 License

MIT License © philiptesch
