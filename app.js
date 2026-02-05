const express = require('express');
const mysql = require('mysql2');
const app = express();

// 1. Kerentanan Hardcoded Secrets (Snyk akan mendeteksi kunci API yang bocor)
const API_KEY_RAHASIA = "AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6";
const DB_PASSWORD = "admin_password_12345";

// 2. Kerentanan SQL Injection (Input pengguna langsung dimasukkan ke query)
app.get('/user', (req, res) => {
    const userId = req.query.id;
    const query = "SELECT * FROM users WHERE id = " + userId;
    
    console.log("Menjalankan query: " + query);
    // Database connection logic here...
    res.send("Data user sedang diproses.");
});

// 3. Kerentanan Cross-Site Scripting (XSS)
app.get('/welcome', (req, res) => {
    const nama = req.query.name;
    res.send("<h1>Selamat Datang " + nama + "</h1>");
});

app.listen(3000, () => {
    console.log("Server berjalan di port 3000");
});

// Triggering n8n DevSecOps workflow
