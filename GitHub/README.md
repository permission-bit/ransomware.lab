# Fix Missing GitHub Contributions (Rewrite Old Commit Emails)

> Rewrite old Git commit emails so GitHub correctly links your commits and restores missing contribution squares.

---

# 1. Create a Backup

```bash
cd ..
cp -R YOUR_REPO YOUR_REPO_BACKUP
cd YOUR_REPO
```

---

# 2. Install git-filter-repo

macOS (Homebrew):

```bash
brew install git-filter-repo
```

---

# 3. Rewrite Old Commit Emails

Replace old commit emails with your current verified GitHub email.

## Example

Old email:

```text
old@example.com
```

New verified GitHub email:

```text
new@example.com
```

## Rewrite Emails

```bash
git filter-repo --force --email-callback '
if email == b"old@example.com":
    return b"new@example.com"
return email
'
```

---

# 4. Optional: Rewrite Author Name

```bash
git filter-repo --force --name-callback '
return b"Your Name"
' --email-callback '
if email == b"old@example.com":
    return b"new@example.com"
return email
'
```

---

# 5. Verify Changes

```bash
git log --pretty=format:"%h | %an | %ae | %ad" --date=short -20
```

You should now only see your new verified GitHub email.

Example:

```text
abc1234 | Your Name | new@example.com | 2025-05-18
```

---

# 6. Check Remote

```bash
git remote -v
```

If `origin` is missing:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

---

# 7. Force Push Rewritten History

```bash
git push --force --all origin
git push --force --tags origin
```

---

# 8. Wait For GitHub Reindexing

GitHub may need some time to update contribution graphs.

Possible delay:

- a few minutes
- sometimes several hours

---

# 9. Configure Git Correctly For Future Commits

```bash
git config --global user.name "Your Name"
git config --global user.email "new@example.com"
```

Verify:

```bash
git config --global --list
```

---

# 10. Check If Contributions Work

Create a test commit:

```bash
echo "test" >> test.txt
git add .
git commit -m "Test contribution"
git push
```

If the new commit appears in your GitHub contribution graph, your setup is correct.

---

# Notes

- Commit dates stay unchanged
- Old contribution days are preserved
- Commit hashes change after rewrite
- Force push is required
- Recommended only for repositories you control

---

# Useful GitHub Settings

Enable private contributions:

GitHub → Settings → Profile

Enable:

```text
Include private contributions on my profile
```

This does NOT expose private repositories or source code.
