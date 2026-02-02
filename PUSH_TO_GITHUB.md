# How to Push This Project to GitHub

## If PowerShell says "git is not recognized"

Git is installed but its folder is not in your PATH. Use **one** of these:

### Option A – Add Git to PATH (recommended, permanent)

1. Press **Win + R**, type `sysdm.cpl`, Enter.
2. **Advanced** tab → **Environment Variables**.
3. Under **User variables**, select **Path** → **Edit** → **New**.
4. Add: `C:\Program Files\Git\bin`
5. OK all dialogs. **Close and reopen PowerShell**, then run the commands below.

### Option B – Use the script (no PATH change)

In PowerShell from this folder, run:

```powershell
.\git-push.ps1
```

That script uses Git’s full path. After the first commit, do **Step 3** and **Step 4** below manually (using `.\git-push.ps1` again for push, or add Git to PATH first).

---

The project folder **ai-audit-fairness** is ready with:

- `README.md` – main project readme
- `ai_audit.py` – audit script
- `ai_audit_EXPLAINED.md` – explanation & interview guide
- `requirements.txt` – dependencies
- `.gitignore` – Python/IDE ignores

## Step 1: Open a terminal in the project folder

```powershell
cd C:\Users\shris\ai-audit-fairness
```

## Step 2: Initialize Git and make the first commit

```powershell
git init
git add .
git commit -m "Initial commit: AI fairness audit with Fairlearn"
```

## Step 3: Create a new repo on GitHub

1. Go to **https://github.com/new**
2. Repository name: **ai-audit-fairness** (or any name you like)
3. Choose **Public**
4. Do **not** add a README, .gitignore, or license (we already have them)
5. Click **Create repository**

## Step 4: Add your GitHub repo as remote and push

Replace **YOUR_USERNAME** with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/ai-audit-fairness.git
git branch -M main
git push -u origin main
```

If you use SSH:

```powershell
git remote add origin git@github.com:YOUR_USERNAME/ai-audit-fairness.git
git branch -M main
git push -u origin main
```

## If Git is not installed

1. Download: **https://git-scm.com/download/win**
2. Install (default options are fine)
3. Restart your terminal, then run the commands above from **Step 2**.

After this, your repo will be on GitHub with the README and all project files.
