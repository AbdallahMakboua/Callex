هذه **النسخة النهائية** لـ `docs/RUNBOOK.md` — انسخها وضعها كما هي:

````md
# Callex Runbook

This document explains how to run, deploy, and operate Callex.

---

## Prerequisites
- Docker
- Docker Compose
- Git

---

## Run locally

1) Clone the repository
```bash
git clone https://github.com/AbdallahMakboua/Callex.git
cd callex
````

2. Create environment file (if available)

```bash
cp .env.example .env
```

3. Start all services

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

4. Check containers

```bash
docker compose -f infra/docker-compose.yml ps
```

5. Test the API

```bash
curl -s http://localhost:8000/health
```

You should receive:

```json
{"status":"ok"}
```

---

## View logs

Backend logs:

```bash
docker compose logs -f backend
```

Database logs:

```bash
docker compose logs -f db
```

---

## Restart services

Restart backend:

```bash
docker compose restart backend
```

Restart database:

```bash
docker compose restart db
```

Restart everything:

```bash
docker compose restart
```

---

## Stop services

Stop containers:

```bash
docker compose down
```

⚠️ This keeps the database data.

To stop and delete all data (DANGEROUS):

```bash
docker compose down -v
```

---

## Deploy to EC2 (Docker Compose)

1. SSH into the server

```bash
ssh ubuntu@<EC2_PUBLIC_IP>
```

2. Go to project folder

```bash
cd callex
```

3. Pull latest changes

```bash
git pull
```

4. Build and start services

```bash
docker compose up -d --build
docker compose ps
```

5. Verify

```bash
curl -s http://localhost:8000/health
```

If using a reverse proxy or domain, also test the public URL.

---

## Troubleshooting

Check running containers:

```bash
docker compose ps
```

Check backend logs:

```bash
docker compose logs -f backend
```

Restart everything:

```bash
docker compose restart
```

Rebuild if something is broken:

```bash
docker compose up -d --build
```
