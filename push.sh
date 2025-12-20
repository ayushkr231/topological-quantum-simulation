#!/bin/bash
# Helper script to push to GitHub

echo "Attempting to push to GitHub..."
echo ""

# Capture push output to analyze the error
push_output=$(git push -u origin main 2>&1)
push_exit_code=$?

if [ $push_exit_code -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    exit 0
else
    echo ""
    echo "❌ Push failed with the following error:"
    echo "$push_output"
    echo ""
    
    # Check for specific error types and provide targeted guidance
    if echo "$push_output" | grep -qiE "authentication|could not read Username|Permission denied|publickey|unauthorized|403|401"; then
        echo "This appears to be an authentication issue."
        echo ""
        echo "AUTHENTICATION OPTIONS:"
        echo ""
        echo "Option 1: HTTPS with Personal Access Token"
        echo "1. Go to: https://github.com/settings/tokens"
        echo "2. Click 'Generate new token (classic)'"
        echo "3. Name it and check 'repo' scope"
        echo "4. Copy the token"
        echo "5. Run: git push -u origin main"
        echo "6. When prompted, enter your GitHub username and paste the token"
        echo ""
        echo "Option 2: SSH (one-time setup)"
        echo "1. Generate SSH key: ssh-keygen -t ed25519 -C 'your_email@example.com'"
        echo "2. Display public key: cat ~/.ssh/id_ed25519.pub"
        echo "3. Add the key to GitHub: https://github.com/settings/keys"
        echo "4. Update remote: git remote set-url origin git@github.com:$(git config --get remote.origin.url | sed 's|.*github.com/||' | sed 's|\.git$||')"
        echo "5. Push: git push -u origin main"
    elif echo "$push_output" | grep -qiE "divergent|non-fast-forward|rejected|failed to push|cannot push|updates were rejected"; then
        echo "This appears to be a branch divergence or rejection issue."
        echo ""
        echo "SOLUTIONS:"
        echo "1. Pull first: git pull origin main --rebase"
        echo "2. Or merge: git pull origin main"
        echo "3. Resolve any conflicts if they occur"
        echo "4. Then push again: git push origin main"
        echo ""
        echo "Note: If you're sure you want to overwrite remote changes:"
        echo "  git push --force origin main  (use with caution!)"
    elif echo "$push_output" | grep -qiE "network|timeout|connect|connection|unreachable|refused"; then
        echo "This appears to be a network connectivity issue."
        echo ""
        echo "SOLUTIONS:"
        echo "1. Check your internet connection"
        echo "2. Try again later"
        echo "3. If using SSH, try HTTPS instead (or vice versa)"
        echo "4. Check if GitHub is experiencing issues: https://www.githubstatus.com"
    elif echo "$push_output" | grep -qiE "remote.*not found|repository.*not found|404"; then
        echo "This appears to be a repository access or existence issue."
        echo ""
        echo "SOLUTIONS:"
        echo "1. Verify the repository exists and you have access"
        echo "2. Check the remote URL: git remote -v"
        echo "3. Verify your repository permissions"
    else
        echo "Please review the error message above and consult git documentation."
        echo ""
        echo "Common issues and solutions:"
        echo "- Authentication problems: See authentication options above"
        echo "- Branch divergence: Pull/merge first, then push"
        echo "- Network issues: Check connection and try again"
        echo "- Permission issues: Verify repository access"
        echo "- Repository not found: Check remote URL and permissions"
    fi
    exit $push_exit_code
fi

