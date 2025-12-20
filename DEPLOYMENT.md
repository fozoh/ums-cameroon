# Deployment Guide

This guide covers deploying UMS Cameroon to production environments.

## Pre-Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up static/media file storage
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for frontend domain
- [ ] Set up email backend
- [ ] Configure payment provider credentials
- [ ] Set up backups and monitoring
- [ ] Run security audit (`make audit`)

---

## 1. Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Heroku account

### Backend Setup

```bash
# Create Heroku app
heroku create ums-cameroon

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set ALLOWED_HOSTS=ums-cameroon.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Frontend Setup

```bash
# Create separate Heroku app for frontend
heroku create ums-cameroon-frontend

# Build and deploy
cd frontend
npm run build
# Use Heroku buildpack for static site
heroku buildpacks:add heroku/static
git push heroku main
```

---

## 2. AWS Deployment (EC2 + RDS)

### Backend on EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# - Type: t3.medium or larger
# - Security group: open 8000, 443

# 2. Connect and setup
ssh -i key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & dependencies
sudo apt install -y python3.12 python3.12-venv postgresql-client

# Clone repo
git clone https://github.com/fozoh/ums-cameroon.git
cd ums-cameroon/backend

# Setup venv
python3.12 -m venv ../.venv
source ../.venv/bin/activate

# Install deps
pip install -r requirements.txt gunicorn

# Configure .env
cp .env.example .env
# Edit with RDS endpoint, password, etc.

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# 3. Setup Gunicorn + Nginx
sudo apt install -y nginx

# Create systemd service
sudo tee /etc/systemd/system/ums-backend.service > /dev/null <<EOF
[Unit]
Description=UMS Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ums-cameroon/backend
ExecStart=/home/ubuntu/ums-cameroon/.venv/bin/gunicorn ums.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable ums-backend
sudo systemctl start ums-backend

# Configure Nginx
sudo tee /etc/nginx/sites-available/ums-backend > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /static/ {
        alias /home/ubuntu/ums-cameroon/backend/staticfiles/;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/ums-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 4. Setup SSL with Let's Encrypt
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### RDS PostgreSQL Setup

```bash
# In AWS Console:
# 1. Create RDS instance (PostgreSQL 14+)
# 2. Multi-AZ: Yes (for production)
# 3. Storage: 20GB gp2 (adjust as needed)
# 4. Backup retention: 30 days

# After creation, update .env:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ums_db
DB_USER=postgres
DB_PASSWORD=<strong-password>
DB_HOST=<rds-endpoint>.rds.amazonaws.com
DB_PORT=5432
```

---

## 3. Docker Deployment (Any Cloud)

### Using Docker Compose on Ubuntu

```bash
# 1. Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 2. Clone and setup
git clone https://github.com/fozoh/ums-cameroon.git
cd ums-cameroon

# 3. Create .env
cp backend/.env.example backend/.env
# Edit .env with production values

# 4. Update docker-compose.yml for production
# - Use PostgreSQL service instead of SQLite
# - Set DEBUG=False
# - Configure Nginx reverse proxy

# 5. Deploy
docker-compose -f docker-compose.yml up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

### Production docker-compose.yml Example

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ums_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    build: ./backend
    environment:
      DEBUG: 'False'
      SECRET_KEY: ${SECRET_KEY}
      DB_ENGINE: django.db.backends.postgresql
      DB_NAME: ums_db
      DB_USER: postgres
      DB_PASSWORD: ${DB_PASSWORD}
      DB_HOST: db
    depends_on:
      - db
    restart: always

  frontend:
    build: ./frontend
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres_data:
```

---

## 4. Environment Variables (Production)

```bash
# Django
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ums_db
DB_USER=postgres
DB_PASSWORD=<strong-password>
DB_HOST=db.example.com
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=<app-password>

# Payment (Flutterwave)
FLUTTERWAVE_PUBLIC_KEY=<live-key>
FLUTTERWAVE_SECRET_KEY=<live-secret>

# SMS (Africa's Talking)
AFRICASTALKING_USERNAME=<live-username>
AFRICASTALKING_API_KEY=<live-key>

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 5. Monitoring & Backups

### Monitoring
- Set up CloudWatch (AWS) or equivalent for logs
- Monitor: CPU, memory, database connections
- Alert on errors and slow queries

### Backups
- Database: Automated daily backups (7-30 day retention)
- Static files: Backup to S3 or equivalent
- Code: All changes tracked in Git

### Logs
```bash
# View Django logs
docker-compose logs -f backend

# View Nginx logs
docker-compose logs -f nginx
```

---

## 6. Scaling Considerations

### Database
- Add read replicas for read-heavy workloads
- Enable connection pooling (PgBouncer)
- Index frequently queried fields

### Backend
- Use load balancer (ALB/NLB)
- Scale horizontally with multiple instances
- Cache with Redis

### Frontend
- Serve from CDN (CloudFront, Cloudflare)
- Compress assets

---

## 7. Security Checklist

- [ ] Update all dependencies (`pip install -U`, `npm audit fix`)
- [ ] Run security audit (`make audit`)
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Configure firewall rules
- [ ] Set secure headers (HSTS, CSP)
- [ ] Rotate sensitive keys regularly
- [ ] Enable database encryption
- [ ] Set up WAF (Web Application Firewall)

---

## Support

For issues or questions, open an issue on GitHub: https://github.com/fozoh/ums-cameroon/issues
