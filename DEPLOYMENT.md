# Deployment Guide

This document provides comprehensive instructions for deploying the Vibe Fitness Platform to production environments.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Docker Deployment](#docker-deployment)
- [Manual Deployment](#manual-deployment)
- [Database Migration](#database-migration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Rollback Procedures](#rollback-procedures)

## Overview

The Vibe Fitness Platform can be deployed using:
1. **Docker Compose** (Recommended for simple deployments)
2. **Manual deployment** (For more control)
3. **Cloud platforms** (AWS, GCP, Azure - future)

### Deployment Architecture

```
┌────────────────┐
│  Load Balancer │
│    (Nginx)     │
└───────┬────────┘
        │
   ┌────┴─────┐
   │          │
┌──▼──┐   ┌──▼──┐
│ API │   │ API │  (Multiple instances)
└──┬──┘   └──┬──┘
   └────┬────┘
        │
   ┌────▼─────┐
   │PostgreSQL│
   │(Primary) │
   └──────────┘
```

## Prerequisites

### System Requirements

**Minimum:**
- 2 CPU cores
- 4 GB RAM
- 20 GB disk space
- Ubuntu 20.04+ or similar Linux distribution

**Recommended:**
- 4+ CPU cores
- 8+ GB RAM
- 50+ GB disk space (SSD preferred)

### Software Requirements

- Docker 24.0+
- Docker Compose 2.20+
- Git
- Python 3.11+ (for manual deployment)
- Node.js 18+ (for manual deployment)
- PostgreSQL 16+ (for manual deployment)
- Nginx 1.24+ (for reverse proxy)

### Domain & SSL

- Domain name configured with DNS
- SSL certificate (Let's Encrypt recommended)

## Environment Configuration

### Backend Environment Variables

Create `backend/.env` file:

```env
# Application
APP_NAME=Vibe Fitness Platform
APP_VERSION=1.0.0
ENVIRONMENT=production
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/vibe_db
DB_ECHO=False

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional: Email (for future use)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
```

### Frontend Environment Variables

Create `frontend/.env.production`:

```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENV=production
```

### Security Checklist

- [ ] Generate strong SECRET_KEY (use `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- [ ] Use strong database password
- [ ] Configure CORS to allow only your domain
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS for all connections
- [ ] Keep environment files out of version control

## Docker Deployment

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: vibe_db
      POSTGRES_USER: vibe_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    networks:
      - vibe-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      DATABASE_URL: postgresql+asyncpg://vibe_user:${DB_PASSWORD}@db:5432/vibe_db
      SECRET_KEY: ${SECRET_KEY}
      ALLOWED_ORIGINS: https://yourdomain.com
      DEBUG: "False"
    depends_on:
      - db
    restart: always
    networks:
      - vibe-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        REACT_APP_API_URL: https://api.yourdomain.com
    restart: always
    networks:
      - vibe-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - frontend_build:/usr/share/nginx/html
    depends_on:
      - backend
      - frontend
    restart: always
    networks:
      - vibe-network

networks:
  vibe-network:
    driver: bridge

volumes:
  postgres_data:
  frontend_build:
```

### Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
            
            # Cache static assets
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    }
}
```

### Deployment Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rafi653/vibe_project.git
   cd vibe_project
   ```

2. **Set up environment variables**:
   ```bash
   # Create .env file in project root
   cat > .env << EOF
   DB_PASSWORD=your-secure-password
   SECRET_KEY=your-secret-key
   EOF
   ```

3. **Build and start services**:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Run database migrations**:
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
   ```

5. **Create admin user** (optional):
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python -m app.scripts.create_admin
   ```

6. **Verify deployment**:
   ```bash
   curl https://yourdomain.com/api/v1/health
   ```

## Manual Deployment

### Backend Deployment

1. **Set up Python environment**:
   ```bash
   cd backend
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Run with Gunicorn**:
   ```bash
   gunicorn app.main:app \
     --workers 4 \
     --worker-class uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:8000 \
     --access-logfile - \
     --error-logfile -
   ```

### Frontend Deployment

1. **Build production assets**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Serve with Nginx**:
   ```bash
   # Copy build files to nginx directory
   sudo cp -r build/* /var/www/html/
   ```

### Database Setup

1. **Install PostgreSQL**:
   ```bash
   sudo apt update
   sudo apt install postgresql-16
   ```

2. **Create database and user**:
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE vibe_db;
   CREATE USER vibe_user WITH PASSWORD 'secure-password';
   GRANT ALL PRIVILEGES ON DATABASE vibe_db TO vibe_user;
   \q
   ```

3. **Configure PostgreSQL**:
   ```bash
   # Edit /etc/postgresql/16/main/postgresql.conf
   listen_addresses = 'localhost'
   max_connections = 100
   shared_buffers = 256MB
   ```

## Database Migration

### Running Migrations

```bash
# In production environment
cd backend
alembic upgrade head
```

### Creating New Migrations

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Review the generated migration file
# Edit if necessary

# Apply migration
alembic upgrade head
```

### Rollback

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

## Monitoring

### Application Logs

**Docker:**
```bash
# View all logs
docker-compose logs -f

# View backend logs
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 backend
```

**Manual deployment:**
```bash
# Backend logs
tail -f /var/log/vibe/backend.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Health Checks

Set up automated health checks:

```bash
# Add to crontab
*/5 * * * * curl -f https://yourdomain.com/api/v1/health || echo "Health check failed"
```

### Metrics (Future Enhancement)

Consider implementing:
- Prometheus for metrics collection
- Grafana for visualization
- ELK stack for log aggregation
- Sentry for error tracking

## Troubleshooting

### Common Issues

**1. Database connection errors**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U vibe_user -d vibe_db -h localhost

# Review database logs
sudo tail -f /var/log/postgresql/postgresql-16-main.log
```

**2. Port conflicts**
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill process if needed
sudo kill -9 <PID>
```

**3. SSL certificate errors**
```bash
# Check certificate validity
openssl x509 -in /etc/nginx/ssl/fullchain.pem -text -noout

# Renew Let's Encrypt certificate
sudo certbot renew
```

**4. Out of memory**
```bash
# Check memory usage
free -m

# Check disk space
df -h

# Increase swap if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Rollback Procedures

### Docker Deployment Rollback

1. **Stop current deployment**:
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

2. **Checkout previous version**:
   ```bash
   git checkout <previous-tag-or-commit>
   ```

3. **Rebuild and deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Rollback database** (if needed):
   ```bash
   docker-compose exec backend alembic downgrade -1
   ```

### Manual Deployment Rollback

1. **Stop services**:
   ```bash
   sudo systemctl stop vibe-backend
   sudo systemctl stop nginx
   ```

2. **Restore previous version**:
   ```bash
   cd /opt/vibe_project
   git checkout <previous-version>
   ```

3. **Restore database backup** (if needed):
   ```bash
   sudo -u postgres psql vibe_db < backup.sql
   ```

4. **Restart services**:
   ```bash
   sudo systemctl start vibe-backend
   sudo systemctl start nginx
   ```

## Backup and Recovery

### Database Backup

**Automated daily backups**:

Create `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="vibe_db_$DATE.sql"

# Create backup
docker-compose exec -T db pg_dump -U vibe_user vibe_db > "$BACKUP_DIR/$FILENAME"

# Compress backup
gzip "$BACKUP_DIR/$FILENAME"

# Keep only last 7 days
find $BACKUP_DIR -name "vibe_db_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $FILENAME.gz"
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

### Restore from Backup

```bash
# Decompress backup
gunzip /backups/vibe_db_YYYYMMDD_HHMMSS.sql.gz

# Restore database
docker-compose exec -T db psql -U vibe_user vibe_db < /backups/vibe_db_YYYYMMDD_HHMMSS.sql
```

## Performance Optimization

### Backend Optimization

1. **Use production ASGI server** (Gunicorn + Uvicorn workers)
2. **Enable database connection pooling**
3. **Add caching layer** (Redis)
4. **Optimize database queries** (add indexes, use EXPLAIN)
5. **Enable gzip compression**

### Frontend Optimization

1. **Enable code splitting**
2. **Optimize images**
3. **Use CDN for static assets**
4. **Enable browser caching**
5. **Minify and compress assets**

### Database Optimization

1. **Regular VACUUM and ANALYZE**:
   ```bash
   docker-compose exec db psql -U vibe_user -d vibe_db -c "VACUUM ANALYZE;"
   ```

2. **Monitor slow queries**:
   ```sql
   -- Enable slow query logging
   ALTER DATABASE vibe_db SET log_min_duration_statement = 1000;
   ```

3. **Add indexes for frequently queried columns**

## Security Best Practices

1. **Keep software updated**:
   ```bash
   sudo apt update && sudo apt upgrade
   docker-compose pull
   ```

2. **Configure firewall**:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

3. **Enable fail2ban** for SSH protection

4. **Regular security audits**:
   ```bash
   # Scan for vulnerabilities
   docker scan vibe_project_backend
   ```

5. **Rotate secrets regularly**

## Scaling

### Horizontal Scaling

1. **Add load balancer** (nginx, HAProxy, or cloud load balancer)
2. **Deploy multiple backend instances**
3. **Use read replicas** for database
4. **Add caching layer** (Redis)
5. **Use CDN** for static assets

### Vertical Scaling

1. **Increase server resources** (CPU, RAM)
2. **Optimize database configuration**
3. **Increase worker processes**

## Support

For deployment issues:
1. Check logs first
2. Review this documentation
3. Check GitHub Issues
4. Contact the development team

## Changelog

Document significant deployment changes:
- **2025-01-11**: Initial deployment documentation created
- **Future**: Add cloud deployment guides (AWS, GCP, Azure)

---

**Note**: This guide is continuously updated. Always refer to the latest version before deployment.
