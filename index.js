const express = require('express');
const PORT = require('./config/port');

// Instantiate express as app
const app = express();

// Create a server
app.listen(PORT, () => console.log(`Server running on port: ${PORT}`))