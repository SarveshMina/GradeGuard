# ------------------------------------------------------------------
# PowerShell script to edit a GitHub repository's metadata:
#   - Description
#   - Website
#   - Topics (via --add-topic per topic)
# Requires:
#   1. GitHub CLI installed (https://cli.github.com/)
#   2. Authenticated via 'gh auth login'
# ------------------------------------------------------------------

$repoSlug       = "SarveshMina/Grade-Home"
$newDescription = "A versatile university grade-tracking and calculator application built with Azure Functions, Vue.js, and Capacitor."
$newWebsite     = "https://example-website.com"
$newTopics      = @("education", "grades", "vue", "python", "azure", "capacitor")

Write-Host "Editing repository details for: $repoSlug"
Write-Host "New description: $newDescription"
Write-Host "New website: $newWebsite"
Write-Host "New topics will be added individually..."

# Update description and homepage
gh repo edit $repoSlug `
  --description $newDescription `
  --homepage $newWebsite

# Add each topic individually, if supported by the user's GH CLI version
foreach ($topic in $newTopics) {
    gh repo edit $repoSlug --add-topic $topic
}

Write-Host "Repository details updated successfully."