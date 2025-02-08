const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/user", {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log("MongoDB Connected"))
  .catch(err => console.log(err));

// User Schema
const userSchema = new mongoose.Schema({
    username: String,
    email: String,
    password: String // Storing passwords as plain text (Not recommended for production)
});

const User = mongoose.model("User", userSchema);

// Signup API
app.post("/signup", async (req, res) => {
    const { username, email, password } = req.body;

    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return res.status(400).json({ message: "User already exists 💡" });
    }

    // Create new user
    const newUser = new User({ username, email, password });
    await newUser.save();

    res.status(201).json({ message: "User registered successfully 👍" });
});

// Login API (Redirects after login)
app.post("/login", async (req, res) => {
    const { username, password } = req.body;

    // Find user by username
    const user = await User.findOne({ username });
    if (!user) {
        return res.status(400).json({ message: "User not found ❌" });
    }

    // Compare password directly
    if (password !== user.password) {
        return res.status(400).json({ message: "Invalid credentials 👎" });
    }

    // Redirect user to the dashboard (http://localhost:8501)
    res.status(200).json({ message: "Login successful✅ ", redirectURL: "http://localhost:8501" });
});

// Start the server
app.listen(5000, () => console.log("Server running on port 5000"));

