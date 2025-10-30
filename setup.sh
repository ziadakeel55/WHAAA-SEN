#!/bin/bash

echo "───────────────────────────────────────────────"
echo "🚀 WhatsApp Sender Setup Script"
echo "───────────────────────────────────────────────"
echo ""

if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 not found. Please install it first."
    exit 1
fi

if ! command -v pip &> /dev/null
then
    echo "❌ pip not found. Please install it first."
    exit 1
fi

echo "📦 Creating virtual environment..."
python3 -m venv venv

echo "✅ Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ All requirements installed successfully!"
echo ""

echo "🚀 Running WhatsApp Sender..."
python3 whatsapp_sender.py

echo ""
echo "✨ Done!"
