# StockBreak Pro - Troubleshooting Guide

## Quick Start
1. Run `DIAGNOSE_PROBLEMS.bat` to check your system
2. Run `FIX_DEPENDENCIES.bat` if you have dependency issues
3. Run `START_STOCKBREAK.bat` to start the application
4. Run `STOP_STOCKBREAK.bat` to stop all services

## Common Issues

### Frontend won't start
1. Run `DIAGNOSE_PROBLEMS.bat` first
2. Check if port 3000 is already in use
3. Run `FIX_DEPENDENCIES.bat` to reinstall dependencies
4. Delete `frontend/node_modules` and run `yarn install`

### Backend won't start
1. Check if Python is installed: `python --version`
2. Check if port 8001 is already in use
3. Verify `backend/.env` file exists with MONGO_URL
4. Run: `pip install -r backend/requirements.txt`

### "Port already in use" Error
1. Run `STOP_STOCKBREAK.bat` to stop existing services
2. Or manually kill processes:
   - `taskkill /F /IM node.exe`
   - `taskkill /F /IM python.exe`

### MongoDB Connection Error
1. Check your `backend/.env` file
2. Ensure MONGO_URL is set correctly
3. Verify your MongoDB Atlas cluster is running

### Dependency Conflicts
1. Run `FIX_DEPENDENCIES.bat`
2. This cleans and reinstalls all packages

## Support
If issues persist, please check the console output for specific error messages.
