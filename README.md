# Termux Scripts — Built on Android

Automation scripts built on an Android phone using Termux.
Zero coding experience. Built with Claude AI as coding partner.

## Scripts

### trending_prompts.py
Finds trending AI image prompts from GitHub and HuggingFace.
Saves a dated report with top repos, models, and style tags.

**Run it:**
python trending_prompts.py

**Output:** Dated .txt report with trending repos, models, and content ideas.

### content_ideas.py
Reads the latest trend report and generates platform-specific content ideas.
Outputs YouTube titles, Instagram hooks, newsletter subjects, and a 7-day calendar.

**Run it:**
python content_ideas.py

**Output:** content_ideas_YYYY-MM-DD.txt with 15-20 ready-to-use content ideas.

### auto_push.py
Checks for changed files and automatically commits + pushes them to GitHub.
Runs daily after Scripts 1 and 2, keeping this repo continuously updated.

**Run it:**
python auto_push.py

**Output:** push_log.txt — log of every push attempt and result.
**Note:** Run trending_prompts.py first to generate a fresh trend report.
---
Built by a student from Punjab, India.
Phone: Poco F6 | Environment: Termux on Android
