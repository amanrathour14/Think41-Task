# PowerShell script to commit and push milestones
param(
    [Parameter(Mandatory=$true)]
    [int]$MilestoneNumber,
    
    [Parameter(Mandatory=$true)]
    [string]$Description
)

Write-Host "🚀 Committing Milestone $MilestoneNumber: $Description" -ForegroundColor Green

# Check if we have changes to commit
$status = git status --porcelain
if (-not $status) {
    Write-Host "❌ No changes to commit!" -ForegroundColor Red
    exit 1
}

# Show what will be committed
Write-Host "`n📋 Changes to be committed:" -ForegroundColor Yellow
git status --short

# Stage all changes
Write-Host "`n📦 Staging changes..." -ForegroundColor Blue
git add .

# Commit with milestone message
$commitMessage = "Milestone $MilestoneNumber`: $Description"
Write-Host "`n💾 Committing: $commitMessage" -ForegroundColor Cyan
git commit -m $commitMessage

# Push to remote
Write-Host "`n🚀 Pushing to remote..." -ForegroundColor Green
git push origin main

Write-Host "`n✅ Milestone $MilestoneNumber committed and pushed successfully!" -ForegroundColor Green

# Show recent commits
Write-Host "`n📜 Recent commits:" -ForegroundColor Yellow
git log --oneline -5 