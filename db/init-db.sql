CREATE DATABASE IF NOT EXISTS logs_db;
USE logs_db;

CREATE TABLE IF NOT EXISTS access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    client_ip VARCHAR(255),
    internal_ip VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS counter (
    id INT PRIMARY KEY,
    count INT
);

INSERT INTO counter (id, count) VALUES (1, 0)
    ON DUPLICATE KEY UPDATE count = count;