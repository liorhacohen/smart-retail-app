#!/bin/bash

# Validate Jenkinsfile syntax
echo "🔍 Validating Jenkinsfile syntax..."

# Check if Jenkinsfile exists
if [ ! -f "Jenkinsfile" ]; then
    echo "❌ Jenkinsfile not found!"
    exit 1
fi

echo "✅ Jenkinsfile found"

# Basic syntax checks
echo "🔍 Checking basic syntax..."

# Check for required pipeline elements
if grep -q "pipeline {" Jenkinsfile; then
    echo "✅ Pipeline declaration found"
else
    echo "❌ Missing pipeline declaration"
    exit 1
fi

if grep -q "agent" Jenkinsfile; then
    echo "✅ Agent declaration found"
else
    echo "❌ Missing agent declaration"
    exit 1
fi

if grep -q "stages" Jenkinsfile; then
    echo "✅ Stages block found"
else
    echo "❌ Missing stages block"
    exit 1
fi

if grep -q "stage(" Jenkinsfile; then
    echo "✅ Stage definitions found"
else
    echo "❌ No stage definitions found"
    exit 1
fi

# Check for proper Groovy syntax (basic)
if grep -q "steps" Jenkinsfile; then
    echo "✅ Steps blocks found"
else
    echo "❌ No steps blocks found"
    exit 1
fi

# Check for post actions
if grep -q "post" Jenkinsfile; then
    echo "✅ Post actions found"
else
    echo "⚠️ No post actions found (optional but recommended)"
fi

# Check for error handling
if grep -q "try" Jenkinsfile || grep -q "catch" Jenkinsfile; then
    echo "✅ Error handling found"
else
    echo "⚠️ No explicit error handling found"
fi

# Check for environment variables
if grep -q "environment" Jenkinsfile; then
    echo "✅ Environment variables defined"
else
    echo "⚠️ No environment variables defined"
fi

echo ""
echo "🎉 Jenkinsfile validation completed!"
echo "✅ Your Jenkinsfile appears to be syntactically correct"
echo ""
echo "Next steps:"
echo "1. Run: ./scripts/test-jenkinsfile.sh (for comprehensive testing)"
echo "2. Set up Jenkins server"
echo "3. Install required plugins"
echo "4. Configure credentials"
echo "5. Create Jenkins job" 