#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}[+] Starting install MutOS...${NC}"

if [ "$(uname)" != "Linux" ]; then
    echo -e "${RED}[!] Error: MutOS only working Linux. ${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[!] Error: Python3 or pip3 not found"
    exit 1
fi

echo -e "${GREEN}[+] Installing requirements...${NC}"
python3 -m pip install psutil --break-system-packages 2>/dev/null || python3 -m pip install psutil

if [ $? -ne 0 ]; then
    echo -e "${RED}[!] Error installing psutil automatic, try manually pip install psutil${NC}"
fi
echo -e "${GREEN}[+] Issuance of rights starting script. ${NC}"
chmod +x start.py 2>/dev/null

if [ -d "games" ]; then
    chmod +x games/* 2>/dev/null
fi

echo -e "${GREEN}[+] Great! write 'python3 start.py' ${NC}"
