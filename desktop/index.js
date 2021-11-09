const { app, BrowserWindow } = require('electron');
const path = require('path');

const createWindow = () => {
    const mainWindow = new BrowserWindow({
        width: 400,
        height: 700,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });

    mainWindow.loadFile(path.join(__dirname, 'index.html'))
}

app.on('ready', createWindow);

app.on('window-all-closed', ()=> {
    if (process.platform !== "darwin") {
        app.quit();
    }
});