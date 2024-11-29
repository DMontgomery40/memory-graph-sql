---
title: Setup Guide
layout: default
nav_order: 2
---

# Setup Guide

## Prerequisites

- Python 3.8+
- Git
- SQLite3

## Installation Steps

1. Clone the Repository:
   ```bash
   git clone https://github.com/DMontgomery40/memory-graph-sql.git
   cd memory-graph-sql
   ```

2. Create a Virtual Environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the Database:
   ```python
   python
   >>> from database import init_db
   >>> init_db()
   >>> exit()
   ```

5. Run the MCP Server:
   ```bash
   uvicorn main:app --reload
   ```

The server will start at http://127.0.0.1:8000