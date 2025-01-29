const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    openFolder: () => ipcRenderer.invoke('dialog:openFolder'),
    organizeFiles: (ruta_origen, ruta_destino) => ipcRenderer.invoke('organize:files', ruta_origen, ruta_destino)
});
