# ⚡ Quick Start - 5 Minutes

## 🐳 Docker (Easiest)

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env - Change SECRET_KEY and JWT_SECRET_KEY

# 3. Start everything
docker-compose up -d

# 4. Open browser
http://localhost:5173
```

**Done!** ✅

---

## 🪟 Windows (Automated)

```bash
# 1. Install backend
install_backend.bat

# 2. Install frontend (new terminal)
install_frontend.bat

# 3. Start backend
run_backend.bat

# 4. Start frontend (new terminal)
run_frontend.bat

# 5. Open browser
http://localhost:5173
```

**Done!** ✅

---

## 🛠 Manual Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python download_model.py
python app.py
```

### Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```

### Open Browser
```
http://localhost:5173
```

**Done!** ✅

---

## 📚 Documentation

- **Full Setup:** `SETUP.md`
- **Docker Guide:** `DOCKER_GUIDE.md`
- **Backend Docs:** `backend/README.md`
- **Frontend Docs:** `frontend/README.md`
- **Project Summary:** `PROJECT_SUMMARY.md`

---

## 🆘 Troubleshooting

**Port in use:**
```bash
# Change ports in docker-compose.yml or .env
```

**Docker not starting:**
```bash
docker-compose logs -f
```

**Backend errors:**
```bash
cd backend
python app.py
# Check terminal output
```

**Frontend errors:**
```bash
cd frontend
npm run dev
# Check terminal output
```

---

## ✅ Verify Setup

1. **Backend Health:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Frontend:**
   Open http://localhost:5173

3. **Create Account:**
   - Click "Sign Up"
   - Fill form
   - Login

4. **Test Detection:**
   - Upload test image
   - View result

**All working?** You're ready! 🚀

---

## 🎓 For FYP Demo

1. Start services (Docker or manual)
2. Create test account
3. Prepare sample images/videos
4. Practice workflow
5. Review `PROJECT_SUMMARY.md`

**Good luck!** 🎓
