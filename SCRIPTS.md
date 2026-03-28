# Development Scripts

Helper scripts for common development tasks.

## Setup Scripts

### setup.sh (Linux/Mac)

```bash
#!/bin/bash
set -e

echo "🚀 Setting up Vinyl Aggregator..."

# Backend setup
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo "✅ Backend setup complete"

# Frontend setup
echo "📦 Setting up frontend..."
cd ../frontend
npm install
echo "✅ Frontend setup complete"

echo "✅ Setup complete!"
echo "📚 Next steps:"
echo "  1. Start Docker: docker-compose up -d"
echo "  2. Start backend: cd backend && python main.py"
echo "  3. Start frontend: cd frontend && npm run dev"
```

### setup.bat (Windows)

```batch
@echo off
REM Vinyl Aggregator Windows Setup

echo 🚀 Setting up Vinyl Aggregator...

REM Backend setup
echo 📦 Setting up backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
echo ✅ Backend setup complete

REM Frontend setup
echo 📦 Setting up frontend...
cd ..\frontend
call npm install
echo ✅ Frontend setup complete

echo ✅ Setup complete!
echo 📚 Next steps:
echo   1. Start Docker: docker-compose up -d
echo   2. Start backend: cd backend && python main.py
echo   3. Start frontend: cd frontend && npm run dev
```

## Running Services

### All at Once (requires tmux on Mac/Linux)

```bash
#!/bin/bash
tmux new-session -d -s vinyl

tmux send-keys -t vinyl:0 "docker-compose up" Enter
tmux send-keys -t vinyl:1 "cd backend && python main.py" Enter
tmux send-keys -t vinyl:2 "cd frontend && npm run dev" Enter

echo "✅ Services started in tmux. Use 'tmux attach -t vinyl' to view"
```

## Database Management

### Backup Database

```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U user -d vinyl_aggregator > backups/db_backup_$TIMESTAMP.sql
echo "✅ Database backed up to backups/db_backup_$TIMESTAMP.sql"
```

### Restore Database

```bash
#!/bin/bash
# psql -h localhost -U user -d vinyl_aggregator < backups/db_backup_YYYYMMDD_HHMMSS.sql
echo "Enter backup file path:"
read backup_file
psql -h localhost -U user -d vinyl_aggregator < $backup_file
echo "✅ Database restored"
```

### Reset Database

```bash
#!/bin/bash
echo "⚠️  This will delete all data!"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    psql -h localhost -U user -c "DROP DATABASE vinyl_aggregator;"
    psql -h localhost -U user -c "CREATE DATABASE vinyl_aggregator;"
    echo "✅ Database reset"
fi
```

---

These scripts automate common tasks. Modify paths and credentials as needed for your environment.

