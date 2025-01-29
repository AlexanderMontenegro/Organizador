const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const app = express();

app.use(express.json());

app.post('/run-script', (req, res) => {
  const { rutaOrigen, rutaDestino } = req.body;
  const scriptPath = path.join(__dirname, 'public', 'Principal.py');
  
  // Ejecutar el script de Python con los argumentos de origen y destino
  exec(`python ${scriptPath} "${rutaOrigen}" "${rutaDestino}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error al ejecutar el script: ${error.message}`);
      return res.status(500).json({ error: 'Error al ejecutar el script' });
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return res.status(500).json({ error: stderr });
    }
    console.log(`stdout: ${stdout}`);
    res.json({ message: 'Script ejecutado exitosamente', output: stdout });
  });
});

app.listen(5000, () => {
  console.log('Servidor corriendo en http://localhost:5000');
});
