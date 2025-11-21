const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let pythonProcess;

const isDev = process.env.NODE_ENV === 'development';

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  if (isDev) {
    // Dev mode: load Vite dev server
    win.loadURL('http://localhost:5173'); 
  } else {
    // Production: load built frontend
    win.loadFile(path.join(__dirname, '../frontend/dist/index.html'));
  }

  win.on('closed', () => {
    if (pythonProcess) {
      pythonProcess.kill();
    }
  });
}

function startPythonServer() {
  if (isDev) return;
  // Linux path to venv Python
  const pythonExe = path.join(__dirname, 'python_api', '.venv', 'bin', 'python');

  pythonProcess = spawn(pythonExe, ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'], {
    cwd: path.join(__dirname, 'python_api'),
    shell: true,
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`PYTHON: ${data.toString()}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`PYTHON ERR: ${data.toString()}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python server exited with code ${code}`);
  });
}

// Launch Python server first, then create Electron window
app.whenReady().then(() => {
  startPythonServer();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (pythonProcess) pythonProcess.kill();
    app.quit();
  }
});
