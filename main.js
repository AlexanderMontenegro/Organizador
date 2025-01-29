const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { exec } = require('child_process');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'), // Habilita la comunicación segura
            contextIsolation: true,
            enableRemoteModule: false,
        }
    });

    mainWindow.loadURL('http://localhost:3000'); // Cargar la app de React

    // Abre las herramientas de desarrollo (F12)
    mainWindow.webContents.openDevTools();
}

// Manejar la selección de carpetas
ipcMain.handle('dialog:openFolder', async () => {
    const result = await dialog.showOpenDialog({
        properties: ['openDirectory']
    });
    return result.filePaths[0];
});

// Manejar la organización de archivos
ipcMain.handle('organize:files', async (event, ruta_origen, ruta_destino) => {
    const pythonScriptPath = path.join(__dirname, 'Principal.py');
    const command = `python "${pythonScriptPath}" "${ruta_origen}" "${ruta_destino}"`;

    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(`Error al organizar archivos: ${stderr || error.message}`);
                return;
            }
            resolve(stdout);
        });
    });
});

app.whenReady().then(createWindow);

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
