-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 30-09-2025 a las 05:30:15
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda_ropa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `order_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pendiente','enviado','entregado','cancelado') DEFAULT 'pendiente',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `order_details`
--

DROP TABLE IF EXISTS `order_details`;
CREATE TABLE IF NOT EXISTS `order_details` (
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price_at_purchase` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `price` decimal(10,2) NOT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock`, `image_url`) VALUES
(3, 'Sudadera con Capucha', 'Sudadera cálida y con capucha, perfecta para el invierno.', 30.00, 75, 'https://via.placeholder.com/300x200?text=Sudadera'),
(4, 'Gorra Urbana', 'La gorra urbana es un símbolo de identidad y actitud, directamente influenciada por la cultura del hip-hop, el skateboarding y el deporte. Está diseñada para complementar un look casual, moderno y desenfadado.', 20.00, 100, NULL),
(5, 'Pantalon Vaquero', '', 10.00, 30, '/static/uploads/FONDO-1.jpeg'),
(6, 'Camiseta Roja', 'Camiseta de algodón, talla M', 19.99, 50, '/static/uploads/camiseta_roja.jpg'),
(7, 'Pantalón Jeans', 'Pantalón azul oscuro, talla 32', 39.99, 30, '/static/uploads/pantalon_jeans.jpg'),
(8, 'Chaqueta Negra', 'Chaqueta de cuero sintético, talla L', 59.99, 0, '/static/uploads/chaqueta_negra.jpg'),
(10, 'pantalon ', 'pantalon urbano', 39.00, 0, '/static/uploads/pngegg.png'),
(11, 'medias', 'algodon', 5.00, 50, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('cliente','admin') DEFAULT 'cliente',
  `phone` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `phone`, `email`) VALUES
(9, 'Yunny Cueva', 'scrypt:32768:8:1$7ZfjSDa5ZnzyP5G5$2617de2973de32ef910d0b9da78c5c5883dc2c7fbed309a594943034a116cc30d1730cf73e279295e3b9c0d75b841fbd4faa8f5e5c5ad3808d6bfcedb985dc47', 'admin', '0997549254', 'yv.cuevas.uea@edu.ec'),
(11, 'Yunny Cueva Cliente', 'scrypt:32768:8:1$tSe41xIQrBv7trqG$92a731dd2b01ed2d035229a151cffcf05a2f6c2d384594dfd0bb98ce8222ced823b1185772f68b54b97286658df925fd0ee051a89ef1734b7d63e1e36b910fd7', 'cliente', '0997549254', 'yv.cuevascliente.uea@edu.ec'),
(12, 'Juan manuel', 'scrypt:32768:8:1$UbmptesCecUBfvBa$ea61e0f47607a1d1ff3e0196327885035255744d94a8808deebcf768e35443e2ae2ae48cb8589940b558225058b609ca6599cc0440fd61f9cd67965749913b6b', 'cliente', '4444444466', 'juanmanuel@uea.edu.ec'),
(13, 'Abigail', 'scrypt:32768:8:1$yXcaFHozbZKnVREX$ec38052b150977d52dbf3d640bd2923525c81025fd01f4349ff0f189fc6b45c728468cc86a6979665d17733e33fb754bff699ec564a77a4b18cb65b49d21f49d', 'cliente', '0993577541', 'abigailchila@gmail.com'),
(14, 'julio', 'scrypt:32768:8:1$rWh7OqMHWdO6JpVn$6bbbb589472ca7aa882524e13655881f44e0447461da5f18d35ffa679c07818d49c0c8efe5e7ade5cbf1499d4932c132e450d0402312bfb8932bc25eb4bc8266', 'cliente', '0968664520', 'juliomera@gmail.com'),
(15, 'David Ochoa', 'scrypt:32768:8:1$lbJtIwiS1GK5G3x2$551e9532f49cdea43eb70f0564c71586190a399bd259752c84e357be487665130f9a80bb3a6c83288b36d456ccdff27652dc7a94667f13f04f1db76dd1a23acd', 'admin', '0968564512', 'davidochoa@gmail.com'),
(16, 'gaby', 'scrypt:32768:8:1$yZ71Qzts6emVF1oD$017f414fbcdade02565e958fe5ceb6a81561250d348e0fcfe64cdd1bf575f05903cc1d3530bb38cf63cba9dd9de1496106f100224a05a8783dccedd33f93c077', 'cliente', '0968542154', 'gaby2025@gmail.com');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
