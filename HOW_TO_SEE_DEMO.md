# How to See the Question Bank Demo in Action

## 🎬 Quick Access (Right Now!)

### In v0 Preview
The demo should be running automatically. Click the **Preview** button on the right side of your screen to see the live application!

**URL:** `http://localhost:3000/demo.html`

---

## 📸 What You'll See

### 1. Login Screen
```
Welcome to Question Bank
Username: demo
Password: demo123
[Login Button]
```

**Try it now:** 
- Type "demo" in username
- Type "demo123" in password
- Click Login

### 2. Dashboard (After Login)
You'll see:
- **📊 Statistics:** Questions attempted, correct answers, accuracy percentage
- **📌 Weak Topics:** Topics where you scored below 60%
  - Optics: 40% accuracy
  - Waves: 50% accuracy
- **🎯 AI Recommendations:** Personalized questions based on weak areas

### 3. Browse Questions
Click the "Browse" button to:
- View 9 sample questions
- Filter by Subject (Physics, Chemistry, Math)
- Filter by Topic (Mechanics, Optics, Waves)
- Filter by Difficulty (Easy, Medium, Hard)
- Search for keywords

### 4. Answer Questions
- Click any answer option (A, B, C, or D)
- See if it's correct (green highlight)
- Read the explanation
- Your dashboard updates automatically!

---

## 🎯 Try These Features

### Feature 1: Answer Questions
1. In Browse tab, select any question
2. Click on option **B** for the first question
3. You'll see: "✓ Correct!" in green
4. Read the explanation below

### Feature 2: Filter Questions
1. In Browse tab, click "Difficulty" dropdown
2. Select "Medium"
3. See only medium-difficulty questions

### Feature 3: Search Questions
1. In Browse tab, type "light" in search box
2. See only questions about light

### Feature 4: Check Weak Topics
1. Return to Dashboard
2. See section: "Your Weak Topics (< 60% Accuracy)"
3. Notice "Optics" is your weakest area (40%)
4. "AI Recommendations" suggests Optics questions

### Feature 5: Test Recommendations
1. Go to Browse → Filter by Topic "Optics"
2. Answer all 3 Optics questions correctly
3. Return to Dashboard
4. Accuracy increased! Recommendations changed!

---

## 💻 On Your Computer (After Download)

Once you download the code:

```bash
# Navigate to frontend folder
cd question-bank/frontend

# Start simple web server
python3 -m http.server 3000

# Open browser to
http://localhost:3000/demo.html
```

---

## 🧠 How AI Works (Live Demo)

The demo shows AI recommendations working like this:

**Your Current Performance:**
```
Mechanics:  100% accuracy (10/10 correct)  ✓ Strong
Optics:      40% accuracy (2/5 correct)   ⚠️ Weak!
Waves:       50% accuracy (3/6 correct)   ⚠️ Weak!
```

**What AI Recommends:**
```
1. All Optics questions you haven't answered (weakest topic)
2. Sorted from easy to hard (better learning)
3. Reason: "Your weak area - 40% accuracy"
```

**What Happens When You Practice:**
```
You answer 2 more Optics questions correctly
  ↓
Optics accuracy: 40% → 57% (still weak)
  ↓
AI keeps recommending Optics
  ↓
You answer 2 more correctly
  ↓
Optics accuracy: 57% → 71% (no longer weak!)
  ↓
AI stops recommending Optics
  ↓
AI now recommends Waves (your next weak topic)
```

---

## 📊 Real Data in Demo

### 9 Sample Questions Included

#### Physics - Mechanics
1. Car acceleration with kinematic equation
2. SI unit of force
3. Projectile motion calculation

#### Physics - Optics  
4. Speed of light in vacuum
5. Refractive index of water
6. Snell's law refraction calculation

#### Physics - Waves
7. Frequency from wavelength formula
8. Frequency from period calculation
9. Beat frequency calculation

---

## 🔄 How It Works Behind the Scenes

### Frontend (What You See)
- HTML/CSS: Beautiful user interface
- JavaScript: Handles interactions
- Local storage: Remembers your answers during session
- Simulated API: Mimics real backend

### Backend (Real App - Not in Demo)
- FastAPI: Web server
- PostgreSQL: Database storage
- SQLAlchemy: Database models
- JWT: Secure authentication
- ML: Recommendation engine

### Demo vs Real App

| Aspect | Demo | Real App |
|--------|------|----------|
| Questions | 9 hardcoded | 1000+ from database |
| Data Storage | Browser memory | PostgreSQL database |
| Server | None (HTML only) | Python FastAPI |
| Persistence | Session only | Forever (database) |
| Multi-user | No | Yes |
| AI Model | Simple logic | Advanced ML |
| Speed | Instant | Fast (ms) |

---

## 🎯 What Happens When You...

### ...Login with demo/demo123
- Loads demo user profile
- Shows pre-set test data
- Initializes dashboard

### ...Answer a Question
- JavaScript updates score
- Dashboard recalculates stats
- Recommendations regenerate
- All happens instantly (no server)

### ...Go to Dashboard
- Shows updated statistics
- Recalculates weak topics
- Regenerates recommendations
- Shows progress visualization

### ...Search/Filter
- JavaScript filters the 9 questions
- Shows only matching results
- Updates in real-time

### ...Register New Account
- Creates temporary user
- Clears progress data
- Starts fresh

---

## 📚 Learn More

After exploring the demo, read these docs:

1. **DEMO_GUIDE.md** - Detailed walkthrough
2. **VISUAL_WALKTHROUGH.md** - UI layout details
3. **APPLICATION_FLOW.md** - Feature explanations
4. **ML_RECOMMENDATION_SYSTEM.md** - How AI works
5. **QUICK_START_GUIDE.md** - Setup instructions

---

## ❓ FAQ About Demo

**Q: Why can't I see data after refresh?**
A: Demo data is in browser memory. Refresh clears it. Real app saves to database.

**Q: How many real questions will there be?**
A: 1000+ exam questions from the PDFs you provided.

**Q: Does the AI learn?**
A: Demo shows simple logic. Real app uses ML for better recommendations.

**Q: Can I use this offline?**
A: Yes! The demo works completely offline. Just save the HTML file.

**Q: Is my data secure?**
A: Demo = your browser only. Real app runs on your computer (private).

---

## ✅ Demo Walkthrough Checklist

- [ ] Opened preview (right side of screen)
- [ ] See Question Bank login page
- [ ] Login with demo/demo123
- [ ] View dashboard with statistics
- [ ] See weak topics highlighted
- [ ] Click "Browse" button
- [ ] Answer at least one question
- [ ] See explanation for answer
- [ ] Check updated dashboard
- [ ] Try filtering questions
- [ ] Try searching questions
- [ ] Register new account
- [ ] Understand how recommendations work

---

## 🚀 Next Steps

1. **Explore Demo** (now - 10 minutes)
   - See all features in action
   - Understand how UI works
   - Try answering questions

2. **Read Docs** (10-20 minutes)
   - DEMO_GUIDE.md
   - APPLICATION_FLOW.md
   - ML_RECOMMENDATION_SYSTEM.md

3. **Download Code** (5 minutes)
   - Git clone from GitHub
   - Or download as ZIP

4. **Setup Locally** (30 minutes)
   - Install Python 3.8+
   - Install PostgreSQL
   - Follow QUICK_START_GUIDE.md

5. **Load Real Questions** (15 minutes)
   - Run data import script
   - Load 1000+ exam questions
   - Start studying!

---

## 🎓 What You're Learning

This demo teaches:
- ✓ How exam prep apps work
- ✓ How AI recommendations function
- ✓ How to track learning progress
- ✓ How to identify weak areas
- ✓ Full-stack web application concepts
- ✓ Database design for learning apps
- ✓ ML/AI in education

---

## 📞 Need Help?

1. Check **DEMO_GUIDE.md** - Detailed instructions
2. Read **APPLICATION_FLOW.md** - Feature explanations  
3. See **QUICK_START_GUIDE.md** - Setup help
4. Review **PROJECT_SUMMARY.md** - Technical details

---

## 🎉 You're All Set!

The Question Bank demo is ready to show you:
- Modern, beautiful UI
- Working question system
- AI-powered recommendations
- Real exam preparation workflow

**Go to preview and click the link to see it now!** 🚀

Good luck with your exam prep! 📚✨
