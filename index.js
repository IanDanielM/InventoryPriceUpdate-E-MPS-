const express = require('express');
const PORT = require('./config/port');

// Instantiate express as app
const app = express();

// Routes
app.use('/emps/dropbox', require('./routes/api'))

// Create a server
app.listen(PORT, () => console.log(`Server running on port: ${PORT}`))