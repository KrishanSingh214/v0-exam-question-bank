# How to Download Question Bank to Your Computer

This guide shows you the easiest ways to download and run the Question Bank application locally.

---

## Option 1: Using Git (Recommended)

### Step 1: Install Git
- **Windows**: https://git-scm.com/download/win
- **macOS**: `brew install git`
- **Linux**: `sudo apt install git`

### Step 2: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/your-username/question-bank.git
cd question-bank
```

**Benefits:**
- Easy to pull latest updates
- Can contribute changes back
- Proper version control

---

## Option 2: Download as ZIP (Simplest)

### Step 1: Go to GitHub
1. Open: https://github.com/your-username/question-bank
2. Click green **"Code"** button
3. Click **"Download ZIP"**

### Step 2: Extract ZIP
1. Right-click the ZIP file
2. Select "Extract All..." (Windows) or "Extract" (macOS)
3. Choose your folder

### Step 3: Open in Terminal
```bash
cd question-bank
# Now you're ready to setup!
```

---

## Option 3: Using GitHub Desktop (GUI)

### Step 1: Install GitHub Desktop
- Download from: https://desktop.github.com/

### Step 2: Clone in GitHub Desktop
1. Open GitHub Desktop
2. File → Clone Repository
3. Enter: `your-username/question-bank`
4. Choose where to save
5. Click "Clone"

---

## What You Get After Download

```
question-bank/
├── backend/                  # Python server code
│   ├── main.py             # Main FastAPI app
│   ├── models.py           # Database models
│   ├── database.py         # Database config
│   ├── routes/             # API endpoints
│   ├── database/           # SQL schemas
│   ├── scripts/            # Data import tools
│   ├── requirements.txt    # Python packages
│   └── .env                # Configuration
│
├── frontend/               # Website code
│   ├── index.html         # Main page
│   ├── css/               # Styling
│   ├── js/                # JavaScript logic
│   └── public/            # Images/files
│
├── QUICK_START_GUIDE.md   # Setup instructions
├── ML_RECOMMENDATION_SYSTEM.md  # How AI works
└── PROJECT_SUMMARY.md     # Full documentation
```

---

## Quick Setup After Download

### 1. Open Terminal in the Folder
```bash
cd question-bank
```

### 2. Run Setup Script (Auto Setup)
```bash
# Windows
python setup.py

# macOS/Linux
python3 setup.py
```

Or follow manual steps in `QUICK_START_GUIDE.md`

---

## Folder Structure Explained

### `backend/` - The Server

This runs the API that:
- Stores questions in database
- Authenticates users
- Handles answers
- Generates recommendations

**Key files:**
- `main.py` - Starts the server
- `models.py` - Database structure
- `routes/` - API endpoints
  - `auth.py` - Login/Register
  - `questions.py` - Question operations
  - `recommendations.py` - AI suggestions
  - `admin.py` - Admin features

**Start it with:**
```bash
python -m uvicorn main:app --reload
```

### `frontend/` - The Website

This is what you see in the browser:
- Login/Register page
- Browse questions page
- Dashboard with stats
- Admin panel

**Key files:**
- `index.html` - Main webpage
- `css/styles.css` - All styling
- `js/app.js` - Main logic
- `js/api.js` - Talks to backend
- `js/auth.js` - Login logic
- `js/dashboard.js` - Shows stats
- `js/admin.js` - Admin features

**Start it with:**
```bash
# Just open index.html in browser
# Or use: python -m http.server 3000
```

### `database/` - Question Storage

PostgreSQL database tables:
- `users` - Student accounts
- `questions` - All exam questions
- `user_progress` - Answers you've given
- `bookmarks` - Saved questions
- `topics` - Question categories

---

## Typical Workflow After Download

```
1. Download/Extract → You have all files
   ↓
2. Install Python & PostgreSQL → Tools to run app
   ↓
3. Setup Backend
   - Create venv
   - Install libraries
   - Configure .env
   - Create database
   - Run server (http://localhost:8000)
   ↓
4. Load Questions
   - Run import script
   - Questions now in database
   ↓
5. Start Frontend
   - Open index.html
   - Or use Python server
   ↓
6. Test Application
   - Register → Login → Browse → Solve → Get Recommendations
```

---

## Common Questions

**Q: Do I need internet?**
A: No! Everything runs on your computer. Internet only needed for initial download.

**Q: Can I modify the code?**
A: Yes! It's yours to customize. Change colors, add features, etc.

**Q: Where are questions stored?**
A: In PostgreSQL database on your computer. Not in cloud.

**Q: Can I backup my data?**
A: Yes! Export database: `pg_dump question_bank > backup.sql`

**Q: Can I run on a server?**
A: Yes! Deploy to AWS, Heroku, or any Linux server.

---

## System Requirements

### Minimum:
- **CPU**: 2 GHz processor
- **RAM**: 4 GB
- **Disk**: 2 GB free space
- **OS**: Windows 10+, macOS 10.12+, any Linux

### Recommended:
- **CPU**: 4 GHz processor
- **RAM**: 8 GB
- **Disk**: 10 GB free space
- **Internet**: For initial download (~100 MB)

---

## Troubleshooting Downloads

### Issue: "Git not found"
**Solution**: Install Git from https://git-scm.com

### Issue: "ZIP extraction failed"
**Solution**: Use 7-Zip (Windows) or built-in extractor:
- Windows: Right-click → Extract All
- macOS: Double-click to extract
- Linux: `unzip question-bank.zip`

### Issue: "Can't find downloaded files"
**Solution**: Check your Downloads folder:
- Windows: `C:\Users\YourName\Downloads`
- macOS: `~/Downloads`
- Linux: `~/Downloads`

### Issue: "Extraction permission denied"
**Solution**: 
```bash
# macOS/Linux
chmod -R 755 question-bank
```

---

## Getting Latest Updates

If you used Git to clone:

```bash
cd question-bank
git pull
```

This downloads any new features/fixes.

If you used ZIP:
1. Delete old folder
2. Download new ZIP
3. Extract again

---

## Need Help?

Check these files after download:
1. `QUICK_START_GUIDE.md` - Step-by-step setup
2. `ML_RECOMMENDATION_SYSTEM.md` - How AI works
3. `PROJECT_SUMMARY.md` - Full architecture
4. `backend/` - API documentation

---

## Next: Actually Run It!

After downloading, follow `QUICK_START_GUIDE.md` to:
1. Install prerequisites
2. Setup database
3. Start backend server
4. Open frontend in browser
5. Register and start learning!

You'll have a fully functional Question Bank running on your computer! 🚀

---

**Happy Learning!** If you have questions, check the documentation files included in the download.
