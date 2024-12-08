<?php
$servername = "localhost";
$username = "root"; // Cambiar si tienes un usuario diferente
$password = ""; // Cambiar si tienes una contraseña configurada
$dbname = "reporter_ia";

// Crear la conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}
?>
