# Question Bank - Visual Walkthrough

## 🎨 UI Design & Features

### Color Scheme
```
Primary:    #667eea (Purple/Blue)
Secondary:  #764ba2 (Dark Purple)
Success:    #4caf50 (Green)
Error:      #f44336 (Red)
Warning:    #ff9800 (Orange)
Background: Gradient (Purple to Purple)
Text:       #333 (Dark Grey)
```

---

## 📱 Screen Layouts

### 1. LOGIN PAGE
```
┌─────────────────────────────────────────────────────────┐
│                  📚 Question Bank          🔓 Logout    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│                  ┌──────────────────────┐               │
│                  │ Login to Question    │               │
│                  │ Bank                 │               │
│                  │                      │               │
│                  │ Username             │               │
│                  │ [_______________]    │               │
│                  │                      │               │
│                  │ Password             │               │
│                  │ [_______________]    │               │
│                  │                      │               │
│                  │  [ Login Button ]    │               │
│                  │                      │               │
│                  │ Try: demo / demo123  │               │
│                  └──────────────────────┘               │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 2. DASHBOARD PAGE (After Login)
```
┌─────────────────────────────────────────────────────────┐
│           📚 Question Bank    Demo User (JEE Main)      │
│           [Dashboard] [Browse] [Logout]                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  📊 Your Dashboard                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │    5     │  │    3     │  │   60%    │             │
│  │ Questions│  │ Correct  │  │ Accuracy │             │
│  │Attempted │  │ Answers  │  │          │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                           │
│  📌 Your Weak Topics (< 60% Accuracy)                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Optics                         40% accuracy │ 5 Qs   │
│  │ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │       │
│  │ Waves                          50% accuracy │ 4 Qs   │
│  │ █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │       │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  🎯 AI Recommendations                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Optics] [Light] [Medium]                       │   │
│  │ "A light ray enters glass (n=1.5)..."           │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Waves] [Sound] [Medium]                        │   │
│  │ "Two sound waves have frequencies 256 Hz..."    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│                  [Start Practicing →]                   │
└─────────────────────────────────────────────────────────┘
```

### 3. BROWSE QUESTIONS PAGE
```
┌─────────────────────────────────────────────────────────┐
│           📚 Question Bank    Demo User (JEE Main)      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  🔍 Browse Questions                                    │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │ Subject      │  │ Topic        │                   │
│  │ [All ▼]      │  │ [All ▼]      │                   │
│  └──────────────┘  └──────────────┘                   │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │ Difficulty   │  │ Search...    │                   │
│  │ [All ▼]      │  │ [__________] │                   │
│  └──────────────┘  └──────────────┘                   │
│                                                           │
│  Question 1 of 9                                        │
│  [Physics] [Mechanics] [Easy]                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ "A car accelerates from rest at 2 m/s². What   │   │
│  │ is its velocity after 5 seconds?"               │   │
│  │                                                  │   │
│  │ ○ A) 5 m/s                                      │   │
│  │ ● B) 10 m/s                  ✓ Correct!        │   │
│  │ ○ C) 25 m/s                                     │   │
│  │ ○ D) 50 m/s                                     │   │
│  │                                                  │   │
│  │ ✓ Explanation:                                  │   │
│  │ Using v = u + at, where u=0, a=2, t=5:        │   │
│  │ v = 0 + 2×5 = 10 m/s                           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  Question 2 of 9                                        │
│  [Physics] [Mechanics] [Easy]                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ "What is the SI unit of force?"                 │   │
│  │                                                  │   │
│  │ ○ A) Dyne                                       │   │
│  │ ○ B) Newton                                     │   │
│  │ ○ C) Erg                                        │   │
│  │ ○ D) Joule                                      │   │
│  │                                                  │   │
│  │ [Select an option...]                          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 4. REGISTER PAGE
```
┌─────────────────────────────────────────────────────────┐
│           📚 Question Bank          [Register]           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│                  ┌──────────────────────┐               │
│                  │ Create New Account   │               │
│                  │                      │               │
│                  │ Full Name            │               │
│                  │ [_______________]    │               │
│                  │                      │               │
│                  │ Email                │               │
│                  │ [_______________]    │               │
│                  │                      │               │
│                  │ Username             │               │
│                  │ [_______________]    │               │
│                  │                      │               │
│                  │ Password             │               │
│                  │ [_______________]    │               │
│                  │                      │               │
│                  │ Target Exam          │               │
│                  │ [JEE Main ▼]        │               │
│                  │                      │               │
│                  │  [Register Button]   │               │
│                  └──────────────────────┘               │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Visual Elements

### Badges (Color Coded)
```
[Physics]  - Purple badge
[Chemistry] - Purple badge
[Mechanics] - Blue badge
[Optics]   - Blue badge
[Easy]     - Green badge
[Medium]   - Orange badge  
[Hard]     - Red badge
```

### Buttons
```
Primary: [Button with gradient background]
Hover:   Button lifts up 2px with shadow
Active:  Button returns to normal position
Disabled: Button becomes transparent
```

### Cards
```
┌─────────────────────────────────┐
│  Card Title                     │
│                                 │
│  Content here...                │
│                                 │
│  [Buttons/Links]               │
└─────────────────────────────────┘
 └─ Shadow effect (10px blur)
```

### Answer Options
```
Unselected:  ○ A) Option text
Selected:    ● B) Option text (highlighted blue)
Correct:     ✓ ● B) Option text (green background)
Incorrect:   ✗ ○ C) Option text (red background)
```

---

## 🔄 User Flow Diagram

```
START
  │
  ├─→ [Login Page]
  │     │
  │     ├─ Enter username "demo"
  │     ├─ Enter password "demo123"
  │     └─ Click "Login"
  │
  ├─→ [Dashboard Page]
  │     │
  │     ├─ View Statistics:
  │     │   • Questions Attempted: 5
  │     │   • Correct Answers: 3
  │     │   • Accuracy: 60%
  │     │
  │     ├─ View Weak Topics:
  │     │   • Optics: 40% (Weak!)
  │     │   • Waves: 50%
  │     │
  │     ├─ View Recommendations:
  │     │   • Questions from weak topics
  │     │   • Sorted by difficulty
  │     │
  │     └─ Click "Start Practicing"
  │
  ├─→ [Browse Questions Page]
  │     │
  │     ├─ Filter by:
  │     │   • Subject: Physics
  │     │   • Topic: Optics
  │     │   • Difficulty: Easy
  │     │
  │     ├─ View Questions:
  │     │   1. "What is speed of light?"
  │     │   2. "What is refraction?"
  │     │
  │     ├─ Select Answer:
  │     │   ○ A) ...
  │     │   ● B) ... ✓ CORRECT!
  │     │   ○ C) ...
  │     │   ○ D) ...
  │     │
  │     └─ Read Explanation
  │
  ├─→ [Dashboard Updates]
  │     │
  │     ├─ Questions Attempted: 6
  │     ├─ Correct Answers: 4
  │     ├─ Accuracy: 67%
  │     │
  │     └─ Weak Topics Updated!
  │         Optics: 40% → 50%
  │
  └─→ Repeat until mastery!
```

---

## 📊 Data Display Patterns

### Statistics Card
```
┌─────────────────────┐
│        50           │
│   Questions         │
│    Attempted        │
└─────────────────────┘
    Gradient background
    Large white number
    Grey label text
```

### Weak Topic Item
```
┌──────────────────────────────────────┐
│ Optics                   40% │ 5 Qs  │
├──────────────────────────────────────┤
│ ████░░░░░░░░░░░░░░░░░░░░░░░░│       │
│ (Progress bar shows accuracy)         │
└──────────────────────────────────────┘
```

### Question Card
```
┌────────────────────────────────────┐
│ Question 1 of 9                    │
│ [Physics][Mechanics][Easy]         │
│                                    │
│ "Question text goes here?"         │
│                                    │
│ ○ A) Option 1                     │
│ ○ B) Option 2                     │
│ ○ C) Option 3                     │
│ ○ D) Option 4                     │
│                                    │
│ [Explanation hidden until answer] │
└────────────────────────────────────┘
```

---

## 🎯 Interactive Elements

### Hover Effects
```
Button:   Moves up 2px, shadow increases
Option:   Border turns blue, background lightens
Link:     Color changes to primary color
Card:     Shadow deepens slightly
```

### Click Effects
```
Button:   Depresses, shadow decreases
Option:   Border becomes solid, radio fills
Checkbox: Toggle between ☐ and ☑
```

### Focus Effects (Keyboard Navigation)
```
Input:    Border becomes primary color
Buttons:  Outline highlights
```

---

## 📱 Responsive Design

### Desktop (> 1024px)
```
┌────────────────────────────────────────────┐
│ Header with full navigation                │
├────────────────────────────────────────────┤
│                                            │
│  ┌─────────────────────────────────────┐  │
│  │                                     │  │
│  │    Main Content (max-width 900px)   │  │
│  │                                     │  │
│  └─────────────────────────────────────┘  │
│                                            │
└────────────────────────────────────────────┘
```

### Tablet (768px - 1024px)
```
┌──────────────────────────────┐
│ Header with stacked nav      │
├──────────────────────────────┤
│                              │
│  ┌──────────────────────┐   │
│  │ Content (100% width) │   │
│  └──────────────────────┘   │
│                              │
└──────────────────────────────┘
```

### Mobile (< 768px)
```
┌──────────────────┐
│ Mobile Header    │
├──────────────────┤
│ Single column    │
│ layout           │
│                  │
│ Full width       │
│ content          │
│                  │
└──────────────────┘
```

---

## 🎨 Animation Keyframes

### Page Load
```
Opacity: 0 → 1
Transform: translateY(20px) → translateY(0)
Duration: 500ms
Easing: ease-out
```

### Button Hover
```
Transform: translateY(-2px)
Box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3)
Duration: 200ms
```

### Answer Selection
```
Border-color: #e0e0e0 → #667eea
Background: white → #f5f7ff
Duration: 300ms
```

---

## 💡 User Experience Features

### Visual Feedback
- ✓ Green checkmark for correct answers
- ✗ Red X for incorrect answers
- ⚠️ Orange warning for weak topics
- 📊 Progress bars showing accuracy
- 🎯 Animated recommendations

### Information Hierarchy
1. **Primary:** Question text (large, bold)
2. **Secondary:** Answer options (normal size)
3. **Tertiary:** Metadata (badges, counts)
4. **Quaternary:** Explanations (smaller, muted)

### Accessibility
- Clear color contrast (WCAG AA)
- Readable fonts (Segoe UI, fallbacks)
- Keyboard navigation support
- Focus states visible
- Labels for all inputs

---

## 🚀 Summary

The Question Bank UI is designed for:
- **Clean Visual Design:** Modern gradient background, smooth animations
- **Intuitive Navigation:** Clear menu structure, logical page flow
- **Visual Feedback:** Color-coded badges, progress indicators
- **Responsive Layout:** Works on desktop, tablet, mobile
- **Accessible Interface:** High contrast, readable, keyboard-navigable

This creates an engaging, professional exam prep experience! 📚
