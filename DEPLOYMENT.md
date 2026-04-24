# DEPLOYMENT GUIDE for Crop2X Backend

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Production Checklist](#production-checklist)

---

## Local Development

### Prerequisites
- Python 3.8+
- pip, virtualenv
- Git

### Setup Steps

```bash
# Clone repository
git clone <repo-url>
cd crop-2x_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python -c "from run import app; app.app_context().push(); from app import db; db.create_all()"

# Run development server
python run.py
```

Access at: `http://localhost:5000`

---

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Quick Start

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Manual Docker Commands

```bash
# Build image
docker build -t crop2x-backend:1.0 .

# Run container
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -v logs:/app/logs \
  --name crop2x-api \
  crop2x-backend:1.0

# Shell access
docker exec -it crop2x-api bash

# View logs
docker logs -f crop2x-api

# Stop container
docker stop crop2x-api
```

---

## AWS Deployment

### Using EC2

#### 1. Launch EC2 Instance
```bash
# AMI: Ubuntu 20.04 LTS
# Instance Type: t3.medium (minimum)
# Storage: 20GB SSD
# Security Group: Allow 80, 443, 5000
```

#### 2. Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql nginx

# Clone repository
git clone <repo-url>
cd crop-2x_backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your credentials
```

#### 3. Setup Database
```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Create database
sudo sudo -u postgres psql -c "CREATE DATABASE crop2x_db;"
sudo -u postgres psql -c "CREATE USER crop2x WITH PASSWORD 'secure_password';"

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://crop2x:secure_password@localhost/crop2x_db
```

#### 4. Setup Gunicorn + Nginx

Create `/etc/systemd/system/crop2x.service`:
```ini
[Unit]
Description=Crop2X Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/crop-2x_backend
Environment="PATH=/home/ubuntu/crop-2x_backend/venv/bin"
ExecStart=/home/ubuntu/crop-2x_backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable crop2x
sudo systemctl start crop2x
```

Configure Nginx (`/etc/nginx/sites-available/crop2x`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/crop-2x_backend/app/static;
    }
}
```

Enable Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/crop2x /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Setup SSL (Let's Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Using Elastic Beanstalk

Create `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: run:app
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
    DATABASE_URL: $AWS_DB_URL
```

Deploy:
```bash
eb init -p python-3.9 crop2x-backend
eb create crop2x-prod
eb deploy
```

### Using RDS for Database

```bash
# Create RDS instance (PostgreSQL)
# Note the endpoint, username, password

# Update .env
DATABASE_URL=postgresql://crop2x:password@your-rds-endpoint.amazonaws.com/crop2x_db
```

### Using S3 for Storage

```python
# In app/config.py
import boto3

S3_BUCKET = 'crop2x-storage'
S3_CLIENT = boto3.client('s3')

def upload_to_s3(file_path, bucket_name):
    S3_CLIENT.upload_file(file_path, bucket_name, f"uploads/{file_path}")
```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Deploy Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create crop2x-backend

# Add PostgreSQL add-on
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set OPENAI_API_KEY=your-key

# Create Procfile
echo "web: gunicorn -w 4 run:app" > Procfile

# Push to Heroku
git push heroku main

# View logs
heroku logs -t

# Open app
heroku open
```

### Heroku Environment Setup
```bash
heroku config:set TWILIO_ACCOUNT_SID=your-sid
heroku config:set TWILIO_AUTH_TOKEN=your-token
heroku config:set TWILIO_WHATSAPP_NUMBER=your-number
```

---

## Production Checklist

- [ ] **Security**
  - [ ] Change SECRET_KEY to strong random value
  - [ ] Disable DEBUG mode
  - [ ] Enable HTTPS/SSL
  - [ ] Set FLASK_ENV=production
  - [ ] Configure CORS properly
  - [ ] Use environment variables for secrets

- [ ] **Database**
  - [ ] Use PostgreSQL (not SQLite)
  - [ ] Setup regular backups
  - [ ] Enable SSL for database connection
  - [ ] Create database user with limited permissions

- [ ] **Performance**
  - [ ] Enable caching (Redis)
  - [ ] Setup CDN for static files
  - [ ] Use 4+ Gunicorn workers
  - [ ] Enable gzip compression
  - [ ] Setup load balancing

- [ ] **Monitoring**
  - [ ] Setup error tracking (Sentry)
  - [ ] Enable application logging
  - [ ] Setup uptime monitoring
  - [ ] Configure alerts

- [ ] **API Keys**
  - [ ] Rotate API keys regularly
  - [ ] Use separate keys for dev/prod
  - [ ] Store in secure environment
  - [ ] Never commit keys to repository

- [ ] **Backup & Recovery**
  - [ ] Setup daily database backups
  - [ ] Test restore procedures
  - [ ] Document recovery steps
  - [ ] Setup off-site backup storage

- [ ] **Documentation**
  - [ ] Document deployment process
  - [ ] Create runbooks for common tasks
  - [ ] Document API changes
  - [ ] Keep deployment guide updated

---

## Monitoring & Maintenance

### Health Checks
```bash
# Monitor endpoint
curl https://your-domain.com/health

# Check database connection
psql -h db-host -U crop2x -d crop2x_db -c "SELECT 1;"
```

### Log Rotation
```bash
# Using logrotate
/var/log/crop2x/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
}
```

### Database Maintenance
```bash
# Analyze tables
ANALYZE;

# Vacuum database
VACUUM;

# Backup database
pg_dump crop2x_db > backup.sql
```

---

## Rollback Procedure

```bash
# Check current version
git log --oneline -5

# Rollback to previous version
git revert HEAD

# Deploy rolled back version
git push heroku main
# or
docker-compose restart
```

---

## Troubleshooting

### Application won't start
```bash
# Check logs
tail -f logs/*.log

# Test imports
python -c "from run import app; print('OK')"

# Check database connection
python -c "from app import db; db.session.execute('SELECT 1')"
```

### Database connection issues
```bash
# Test connection
psql -h db-host -U crop2x -d crop2x_db

# Check environment variables
echo $DATABASE_URL

# Restart database service
sudo systemctl restart postgresql
```

### High memory usage
```bash
# Restart application
sudo systemctl restart crop2x

# Check for memory leaks
ps aux | grep python

# Increase swap (temporary)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Cost Optimization

- Use t3.micro for development
- Use t3.small for production
- Enable auto-scaling
- Use spot instances for non-critical
- Monitor CloudWatch metrics
- Setup billing alerts

---

## Support

For deployment issues:
- Check AWS CloudWatch logs
- Review application logs in `logs/` directory
- Check Heroku documentation
- Contact DevOps team
