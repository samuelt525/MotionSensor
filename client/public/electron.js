const path = require('path');

const { app, BrowserWindow } = require('electron');
const isDev = require('electron-is-dev');

function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
  });

  // and load the index.html of the app.
  // win.loadFile("index.html");
  win.loadURL(
    isDev
      ? 'http://localhost:3000'
      : `file://${path.join(__dirname, '../build/index.html')}`
  );
  // Open the DevTools.
  if (isDev) {
    win.webContents.openDevTools({ mode: 'detach' });
  }

  // These lines of code are only used as to test the Electron/Flask app
  // without creating a Flask executable file. Comment this out if we're
  // compiling everything and uncomment the next code block.
  // Also change the path to the Flask script as necessary.
  // Also yes I know this is scuffed as fuck.
  // ------------------------------------------------------------------------
  // var python = require('child_process').spawn('py', ['../../server/server.py']);
  // python.stdout.on('data', function (data) {
  //   console.log("data: ", data.toString('utf8'));
  // });
  // python.stderr.on('data', (data) => {
  //   console.log(`stderr: ${data}`); // when error
  // });

  // These lines of code are used once we are ready for a full build and
  // have created an executable file using pyinstaller. Comment this out
  // if we're developing/testing and then uncomment the previous code block.
  // Also change the path to the executable as necessary.
  // ------------------------------------------------------------------------
  // let backend;
  // backend = path.join(process.cwd(), 'resources/backend/dist/app.exe')
  // var execfile = require(‘child_process’).execFile; execfile(
  //   backend,
  //   {
  //     windowsHide: true,
  //   }, (err, stdout, stderr) => {
  //     if (err) {
  //       console.log(err);
  //     } if (stdout) {
  //       console.log(stdout);
  //     } if (stderr) {
  //       console.log(stderr);
  //     }
  //   }
  // )
  // To kill the Flask executable process when exiting the Electron app
  // const { exec } = require(‘child_process’);
  // exec(‘taskkill / f / t / im app.exe’, (err, stdout, stderr) => {
  //   if (err) {
  //     console.log(err)
  //     return;
  //   }
  //   console.log(`stdout: ${stdout}`);
  //   console.log(`stderr: ${stderr}`);
  // });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});