# GitHub Guide For First-Time Users

## What Is GitHub?
GitHub is a website where you store your project files and code online.

It helps you:
- keep your project safe
- share your work publicly
- show judges your project
- track changes over time

## What Is A Repository?
A repository is simply your project folder on GitHub.

For this hackathon, your repository should contain:
- source code
- README
- sample data
- architecture notes

## First-Time GitHub Steps

### 1. Create an account
Visit [GitHub](https://github.com/) and sign up.

### 2. Create a new repository
Suggested name:

`costpilot-ai`

Keep visibility as `Public`.

### 3. Copy the repository URL
It will look similar to:

`https://github.com/yourname/costpilot-ai.git`

### 4. Open terminal in this project folder
Use:

```bash
cd "/Users/saurabhbarve/Documents/New project"
```

### 5. Add files into git
```bash
git add .
```

### 6. Save your project snapshot
```bash
git commit -m "Initial hackathon submission"
```

### 7. Connect your local project to GitHub
```bash
git remote add origin https://github.com/yourname/costpilot-ai.git
```

### 8. Push your project online
```bash
git branch -M main
git push -u origin main
```

## Very Simple Push Checklist
Follow these in order:

1. Create a new public repository on GitHub
2. Copy the repository URL
3. Open Terminal
4. Go to your project folder
5. Run `git add .`
6. Run `git commit -m "Initial hackathon submission"`
7. Run `git remote add origin YOUR_URL`
8. Run `git branch -M main`
9. Run `git push -u origin main`

If GitHub asks for login:
- sign in through the browser popup, or
- use your GitHub username and personal access token

## Exact Commands To Type
```bash
cd "/Users/saurabhbarve/Documents/New project"
git add .
git commit -m "Initial hackathon submission"
git branch -M main
git remote add origin https://github.com/yourname/costpilot-ai.git
git push -u origin main
```

## What Judges Usually Check On GitHub
- clear project name
- proper README
- working code
- clean folder structure
- commit history

## Good Practice
- Keep file names simple
- Write clear README sections
- Add screenshots later if possible
- Do not upload passwords or secret API keys
