---
name: git-commit-push
description: Standard procedure for committing code changes and pushing to the remote repository.
---

# Git Commit & Push Workflow

Use this skill when you need to save changes to the version control system and synchronize with the remote repository.

## 1. Check Status

Always start by checking the current status of the repository to understand what files have been modified, added, or deleted.

```bash
git status
```

## 2. Stage Changes

Stage the changes you want to commit.

- To stage **all** changes (most common):
  ```bash
  git add .
  ```
- To stage **specific** files:
  ```bash
  git add path/to/file1 path/to/file2
  ```

## 3. Commit Changes

Create a commit with a descriptive message following conventional commit guidelines (e.g., `feat:`, `fix:`, `docs:`, `style:`, `refactor:`).

```bash
git commit -m "type: brief description of changes"
```

_Example: `git commit -m "feat: add new product management endpoints"`_

## 4. Push to Remote

Push the committed changes to the current branch on the remote repository.

```bash
git push
```

_Note: If the upstream branch is not set, use `git push -u origin <branch-name>`._

## 5. Verify

Run `git status` again to ensure the working tree is clean and your branch is up to date with origin.
