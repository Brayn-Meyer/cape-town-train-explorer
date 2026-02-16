const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Just connect to MongoDB - no schema needed for basic connection test
mongoose.connect('mongodb+srv://aashiqbenny2:RE5JCvtiW2c99JXQ@traincluster.fzyv4ga.mongodb.net/')
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.log(err));

app.listen(5000, () => console.log('Server running on port 5000'));