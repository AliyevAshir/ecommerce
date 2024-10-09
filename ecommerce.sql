

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `Review`;
CREATE TABLE `Review` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Review_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `Review_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `cart`;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `parent_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `contact`;
CREATE TABLE `contact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `discount`;
CREATE TABLE `discount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `discount_percentage` float NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `discount_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `favorites`;
CREATE TABLE `favorites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_product` (`user_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `otp`;
CREATE TABLE `otp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `otp` varchar(6) NOT NULL,
  `expires_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `new_price` float NOT NULL,
  `image` text NOT NULL,
  `extra_info` text,
  `category_id` int NOT NULL,
  `discount_price` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `product_images`;
CREATE TABLE `product_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `image` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `user` (`id`, `name`, `photo`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1,	'sasaas',	'',	'asuraliyev405@gmail.com',	'As?dj/fur12324343',	'2024-09-20 09:58:59',	'2024-09-20 09:58:59'),
(2,	'sasaas22332',	NULL,	'asuraliye2223v405@gmail.com',	'As?dj/fur12324343',	'2024-09-20 11:45:06',	'2024-09-20 11:45:06'),
(3,	'Alice Johnson',	'https://example.com/photos/alice.jpg',	'alice@example.com',	'password123',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(4,	'Bob Smith',	'https://example.com/photos/bob.jpg',	'bob@example.com',	'securepass456',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(5,	'Charlie Brown',	'https://example.com/photos/charlie.jpg',	'charlie@example.com',	'mypassword789',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(6,	'Daisy Miller',	'https://example.com/photos/daisy.jpg',	'daisy@example.com',	'passw0rd!',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(7,	'Ethan Hunt',	'https://example.com/photos/ethan.jpg',	'ethan@example.com',	'agent007',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(8,	'Fiona Green',	'https://example.com/photos/fiona.jpg',	'fiona@example.com',	'fionapass',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(9,	'George Black',	'https://example.com/photos/george.jpg',	'george@example.com',	'george123',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(10,	'Hannah White',	'https://example.com/photos/hannah.jpg',	'hannah@example.com',	'hannah@321',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(11,	'Ian Gold',	'https://example.com/photos/ian.jpg',	'ian@example.com',	'goldenpass',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(12,	'Julia Blue',	'https://example.com/photos/julia.jpg',	'julia@example.com',	'julia2021',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(13,	'Kevin Red',	'https://example.com/photos/kevin.jpg',	'kevin@example.com',	'kevin2022',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(14,	'Lily Violet',	'https://example.com/photos/lily.jpg',	'lily@example.com',	'lily@pass',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(15,	'Mike Silver',	'https://example.com/photos/mike.jpg',	'mike@example.com',	'mikesecure',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(16,	'Nina Gray',	'https://example.com/photos/nina.jpg',	'nina@example.com',	'nina@pass',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00'),
(17,	'Oscar White',	'https://example.com/photos/oscar.jpg',	'oscar@example.com',	'oscarpass123',	'2024-09-20 16:57:00',	'2024-09-20 16:57:00');

-- 2024-10-06 05:22:33
