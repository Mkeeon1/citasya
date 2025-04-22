CREATE DATABASE agenda_citas;
USE agenda_citas;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role ENUM('user', 'doctor') NOT NULL
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(50),
    rh VARCHAR(5),
    specialty VARCHAR(50) NOT NULL
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    patient_name VARCHAR(50),
    doctor_id INT,
    date DATE,
    time TIME,
    cubicle VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    doctor_id INT,
    specialty VARCHAR(50),
    order_number VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Insertar usuario 'juan'
INSERT INTO users (username, password, role) VALUES ('juan', '1234', 'user');

-- Insertar doctores de medicina general
INSERT INTO doctors (name, phone, email, rh, specialty) VALUES 
('John Doe', '123456789', 'john.doe@example.com', 'O+', 'medicina general'),
('Jane Smith', '123456789', 'jane.smith@example.com', 'A+', 'medicina general'),
('Robert Brown', '123456789', 'robert.brown@example.com', 'B+', 'medicina general'),
('Emily Davis', '123456789', 'emily.davis@example.com', 'AB+', 'medicina general'),
('Michael Wilson', '123456789', 'michael.wilson@example.com', 'O-', 'medicina general');

-- Insertar doctores de Cardiología
INSERT INTO doctors (name, phone, email, rh, specialty) VALUES 
('Carlos Martinez', '123456789', 'carlos.martinez@example.com', 'O+', 'Cardiologia'),
('Ana Lopez', '987654321', 'ana.lopez@example.com', 'A-', 'Cardiologia'),
('Luis Hernandez', '456789123', 'luis.hernandez@example.com', 'B+', 'Cardiologia'),
('Maria Gonzalez', '789123456', 'maria.gonzalez@example.com', 'AB-', 'Cardiologia'),
('Jorge Ramirez', '321654987', 'jorge.ramirez@example.com', 'O-', 'Cardiologia');

-- Insertar doctores de Pediatría
INSERT INTO doctors (name, phone, email, rh, specialty) VALUES 
('Laura Torres', '123123123', 'laura.torres@example.com', 'A+', 'Pediatria'),
('Pedro Sanchez', '321321321', 'pedro.sanchez@example.com', 'B-', 'Pediatria'),
('Claudia Perez', '456456456', 'claudia.perez@example.com', 'O+', 'Pediatria'),
('Fernando Diaz', '654654654', 'fernando.diaz@example.com', 'AB+', 'Pediatria'),
('Sofia Morales', '789789789', 'sofia.morales@example.com', 'O-', 'Pediatria');

-- Insertar doctores de Ginecología
INSERT INTO doctors (name, phone, email, rh, specialty) VALUES 
('Andrea Castillo', '111222333', 'andrea.castillo@example.com', 'A-', 'Ginecologia'),
('Gabriel Vargas', '444555666', 'gabriel.vargas@example.com', 'B+', 'Ginecologia'),
('Monica Reyes', '777888999', 'monica.reyes@example.com', 'O+', 'Ginecologia'),
('Diego Cruz', '222333444', 'diego.cruz@example.com', 'AB-', 'Ginecologia'),
('Patricia Ortiz', '555666777', 'patricia.ortiz@example.com', 'O-', 'Ginecologia');

-- Insertar doctores de Neurología
INSERT INTO doctors (name, phone, email, rh, specialty) VALUES 
('Ricardo Flores', '888999000', 'ricardo.flores@example.com', 'A+', 'Neurologia'),
('Elena Rojas', '333444555', 'elena.rojas@example.com', 'B-', 'Neurologia'),
('Hector Medina', '666777888', 'hector.medina@example.com', 'O+', 'Neurologia'),
('Isabel Vega', '999000111', 'isabel.vega@example.com', 'AB+', 'Neurologia'),
('Francisco Navarro', '444555666', 'francisco.navarro@example.com', 'O-', 'Neurologia');

-- Insertar doctores de Psiquiatría
INSERT INTO doctors (name, phone, email, rh, specialty) VALUES 
('Carmen Alvarez', '555444333', 'carmen.alvarez@example.com', 'A-', 'Psiquiatria'),
('Alberto Ruiz', '222111000', 'alberto.ruiz@example.com', 'B+', 'Psiquiatria'),
('Natalia Herrera', '777666555', 'natalia.herrera@example.com', 'O+', 'Psiquiatria'),
('Victor Castro', '333222111', 'victor.castro@example.com', 'AB-', 'Psiquiatria'),
('Julia Mendoza', '999888777', 'julia.mendoza@example.com', 'O-', 'Psiquiatria');

-- Insertar usuarios para los doctores
INSERT INTO users (username, password, role) VALUES 
('John', '2345', 'doctor'),
('Jane', '2345', 'doctor'),
('Robert', '2345', 'doctor'),
('Emily', '2345', 'doctor'),
('Michael', '2345', 'doctor'),

('Carlos', '2345', 'doctor'),
('Ana', '2345', 'doctor'),
('Luis', '2345', 'doctor'),
('Maria', '2345', 'doctor'),
('Jorge', '2345', 'doctor'),

('Laura', '2345', 'doctor'),
('Pedro', '2345', 'doctor'),
('Claudia', '2345', 'doctor'),
('Fernando', '2345', 'doctor'),
('Sofia', '2345', 'doctor'),

('Andrea', '2345', 'doctor'),
('Gabriel', '2345', 'doctor'),
('Monica', '2345', 'doctor'),
('Diego', '2345', 'doctor'),
('Patricia', '2345', 'doctor'),

('Ricardo', '2345', 'doctor'),
('Elena', '2345', 'doctor'),
('Hector', '2345', 'doctor'),
('Isabel', '2345', 'doctor'),
('Francisco', '2345', 'doctor'),

('Carmen', '2345', 'doctor'),
('Alberto', '2345', 'doctor'),
('Natalia', '2345', 'doctor'),
('Victor', '2345', 'doctor'),
('Julia', '2345', 'doctor');

-- Insertar citas médicas para cada doctor
INSERT INTO appointments (doctor_id, date, time, cubicle) VALUES 
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '09:00:00', 'A1'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '10:00:00', 'A2'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '11:00:00', 'A3'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '12:00:00', 'A4'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '13:00:00', 'A5'),

((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '09:00:00', 'B1'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '10:00:00', 'B2'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '11:00:00', 'B3'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '12:00:00', 'B4'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '13:00:00', 'B5'),

((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '09:00:00', 'C1'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '10:00:00', 'C2'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '11:00:00', 'C3'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '12:00:00', 'C4'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '13:00:00', 'C5'),

((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '09:00:00', 'D1'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '10:00:00', 'D2'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '11:00:00', 'D3'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '12:00:00', 'D4'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '13:00:00', 'D5'),

((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '09:00:00', 'E1'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '10:00:00', 'E2'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '11:00:00', 'E3'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '12:00:00', 'E4'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '13:00:00', 'E5'),

-- Insertar citas médicas para los doctores de Cardiología
((SELECT id FROM doctors WHERE name = 'Carlos Martinez'), '2023-11-02', '09:00:00', 'F1'),
((SELECT id FROM doctors WHERE name = 'Carlos Martinez'), '2023-11-02', '10:00:00', 'F2'),
((SELECT id FROM doctors WHERE name = 'Carlos Martinez'), '2023-11-02', '11:00:00', 'F3'),
((SELECT id FROM doctors WHERE name = 'Carlos Martinez'), '2023-11-02', '12:00:00', 'F4'),
((SELECT id FROM doctors WHERE name = 'Carlos Martinez'), '2023-11-02', '13:00:00', 'F5'),

((SELECT id FROM doctors WHERE name = 'Ana Lopez'), '2023-11-02', '14:00:00', 'G1'),
((SELECT id FROM doctors WHERE name = 'Ana Lopez'), '2023-11-02', '15:00:00', 'G2'),
((SELECT id FROM doctors WHERE name = 'Ana Lopez'), '2023-11-02', '16:00:00', 'G3'),
((SELECT id FROM doctors WHERE name = 'Ana Lopez'), '2023-11-02', '17:00:00', 'G4'),
((SELECT id FROM doctors WHERE name = 'Ana Lopez'), '2023-11-02', '18:00:00', 'G5'),

-- Insertar citas médicas para los doctores de Pediatría
((SELECT id FROM doctors WHERE name = 'Laura Torres'), '2023-11-03', '09:00:00', 'H1'),
((SELECT id FROM doctors WHERE name = 'Laura Torres'), '2023-11-03', '10:00:00', 'H2'),
((SELECT id FROM doctors WHERE name = 'Laura Torres'), '2023-11-03', '11:00:00', 'H3'),
((SELECT id FROM doctors WHERE name = 'Laura Torres'), '2023-11-03', '12:00:00', 'H4'),
((SELECT id FROM doctors WHERE name = 'Laura Torres'), '2023-11-03', '13:00:00', 'H5'),

((SELECT id FROM doctors WHERE name = 'Pedro Sanchez'), '2023-11-03', '14:00:00', 'I1'),
((SELECT id FROM doctors WHERE name = 'Pedro Sanchez'), '2023-11-03', '15:00:00', 'I2'),
((SELECT id FROM doctors WHERE name = 'Pedro Sanchez'), '2023-11-03', '16:00:00', 'I3'),
((SELECT id FROM doctors WHERE name = 'Pedro Sanchez'), '2023-11-03', '17:00:00', 'I4'),
((SELECT id FROM doctors WHERE name = 'Pedro Sanchez'), '2023-11-03', '18:00:00', 'I5'),

-- Insertar citas médicas para los doctores de Ginecología
((SELECT id FROM doctors WHERE name = 'Andrea Castillo'), '2023-11-04', '09:00:00', 'J1'),
((SELECT id FROM doctors WHERE name = 'Andrea Castillo'), '2023-11-04', '10:00:00', 'J2'),
((SELECT id FROM doctors WHERE name = 'Andrea Castillo'), '2023-11-04', '11:00:00', 'J3'),
((SELECT id FROM doctors WHERE name = 'Andrea Castillo'), '2023-11-04', '12:00:00', 'J4'),
((SELECT id FROM doctors WHERE name = 'Andrea Castillo'), '2023-11-04', '13:00:00', 'J5'),

((SELECT id FROM doctors WHERE name = 'Gabriel Vargas'), '2023-11-04', '14:00:00', 'K1'),
((SELECT id FROM doctors WHERE name = 'Gabriel Vargas'), '2023-11-04', '15:00:00', 'K2'),
((SELECT id FROM doctors WHERE name = 'Gabriel Vargas'), '2023-11-04', '16:00:00', 'K3'),
((SELECT id FROM doctors WHERE name = 'Gabriel Vargas'), '2023-11-04', '17:00:00', 'K4'),
((SELECT id FROM doctors WHERE name = 'Gabriel Vargas'), '2023-11-04', '18:00:00', 'K5'),

-- Insertar citas médicas para los doctores de Neurología
((SELECT id FROM doctors WHERE name = 'Ricardo Flores'), '2023-11-05', '09:00:00', 'L1'),
((SELECT id FROM doctors WHERE name = 'Ricardo Flores'), '2023-11-05', '10:00:00', 'L2'),
((SELECT id FROM doctors WHERE name = 'Ricardo Flores'), '2023-11-05', '11:00:00', 'L3'),
((SELECT id FROM doctors WHERE name = 'Ricardo Flores'), '2023-11-05', '12:00:00', 'L4'),
((SELECT id FROM doctors WHERE name = 'Ricardo Flores'), '2023-11-05', '13:00:00', 'L5'),

((SELECT id FROM doctors WHERE name = 'Elena Rojas'), '2023-11-05', '14:00:00', 'M1'),
((SELECT id FROM doctors WHERE name = 'Elena Rojas'), '2023-11-05', '15:00:00', 'M2'),
((SELECT id FROM doctors WHERE name = 'Elena Rojas'), '2023-11-05', '16:00:00', 'M3'),
((SELECT id FROM doctors WHERE name = 'Elena Rojas'), '2023-11-05', '17:00:00', 'M4'),
((SELECT id FROM doctors WHERE name = 'Elena Rojas'), '2023-11-05', '18:00:00', 'M5'),

-- Insertar citas médicas para los doctores de Psiquiatría
((SELECT id FROM doctors WHERE name = 'Carmen Alvarez'), '2023-11-06', '09:00:00', 'N1'),
((SELECT id FROM doctors WHERE name = 'Carmen Alvarez'), '2023-11-06', '10:00:00', 'N2'),
((SELECT id FROM doctors WHERE name = 'Carmen Alvarez'), '2023-11-06', '11:00:00', 'N3'),
((SELECT id FROM doctors WHERE name = 'Carmen Alvarez'), '2023-11-06', '12:00:00', 'N4'),
((SELECT id FROM doctors WHERE name = 'Carmen Alvarez'), '2023-11-06', '13:00:00', 'N5'),

((SELECT id FROM doctors WHERE name = 'Alberto Ruiz'), '2023-11-06', '14:00:00', 'O1'),
((SELECT id FROM doctors WHERE name = 'Alberto Ruiz'), '2023-11-06', '15:00:00', 'O2'),
((SELECT id FROM doctors WHERE name = 'Alberto Ruiz'), '2023-11-06', '16:00:00', 'O3'),
((SELECT id FROM doctors WHERE name = 'Alberto Ruiz'), '2023-11-06', '17:00:00', 'O4'),
((SELECT id FROM doctors WHERE name = 'Alberto Ruiz'), '2023-11-06', '18:00:00', 'O5');
