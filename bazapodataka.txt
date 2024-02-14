-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 14, 2024 at 09:12 PM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `baze`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `ime` varchar(50) NOT NULL,
  `prezime` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `uloga` int NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `ime`, `prezime`, `email`, `uloga`, `password`) VALUES
(1, 'demo', 'demo', 'demoivc', 'demovic@mail.com', 1, '$2b$12$v6txDULYXfW1WSE0PTY/6u9bQJz3HarGy.rMlsaGJnDZn02lXegUS'),
(2, 'test', 'test', 'testic', 'markoviclazar20@gmail.com', 1, '$2b$12$U93G2OW.IpD94.8./67NB.4dKey0O8or2B6Qhi8M3XGE6b1HaSNVq'),
(3, 'novinar', 'novinar', 'novinarovic', 'novinar@mail.com', 3, '$2b$12$rk.jSnZ1gy5cnR7LEqrMXeM0WuA8o9iKspvjsVdUwc1fWssw/xsue'),
(4, 'urednik', 'urednik', 'urednikovic', 'urednik@mail.com', 1, '$2b$12$zl9TFkorJrquPbKq2DkpUekUTfKe11H3wAN0n1S12M58T1Tww.itq'),
(5, 'novi', 'novi', 'novi', 'novi@mail.com', 3, '$2b$12$4DoscJCQRQf2KgYOKgoR7ujeLKvB0cepUuVgJyGW6AEjLkWt.UMum'),
(6, 'urednik2', 'urednik2', 'urednikdvakovic', 'urednik2@gmail.com', 2, '$2b$12$RmX.WzVLAoZkDlPX2pfWJevtMZH7LNKJxQHrkT4sKeg6quhn5MlSO');

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
CREATE TABLE IF NOT EXISTS `images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_image_name` (`filename`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `images`
--

INSERT INTO `images` (`id`, `filename`) VALUES
(1, 'test.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `kategorije`
--

DROP TABLE IF EXISTS `kategorije`;
CREATE TABLE IF NOT EXISTS `kategorije` (
  `id` int NOT NULL AUTO_INCREMENT,
  `naziv` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kategorije`
--

INSERT INTO `kategorije` (`id`, `naziv`) VALUES
(1, 'sport'),
(5, 'tehnologija'),
(6, 'politika');

-- --------------------------------------------------------

--
-- Table structure for table `komentari`
--

DROP TABLE IF EXISTS `komentari`;
CREATE TABLE IF NOT EXISTS `komentari` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vest_id` int NOT NULL,
  `ime` varchar(25) NOT NULL,
  `komentar` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lajkovi_komentara`
--

DROP TABLE IF EXISTS `lajkovi_komentara`;
CREATE TABLE IF NOT EXISTS `lajkovi_komentara` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_komentara` int NOT NULL,
  `ip_adresa` varchar(15) NOT NULL,
  `tip` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_lajk_komentara` (`id_komentara`,`ip_adresa`),
  KEY `idx_lajk_komentara_tip` (`id_komentara`,`tip`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lajkovi_vesti`
--

DROP TABLE IF EXISTS `lajkovi_vesti`;
CREATE TABLE IF NOT EXISTS `lajkovi_vesti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_vesti` int NOT NULL,
  `ip_adresa` varchar(15) NOT NULL,
  `tip` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `novinari_kategorije`
--

DROP TABLE IF EXISTS `novinari_kategorije`;
CREATE TABLE IF NOT EXISTS `novinari_kategorije` (
  `id` int NOT NULL AUTO_INCREMENT,
  `novinar_id` int NOT NULL,
  `kategorija_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `novinari_kategorije`
--

INSERT INTO `novinari_kategorije` (`id`, `novinar_id`, `kategorija_id`) VALUES
(11, 3, 5),
(10, 3, 1),
(8, 5, 1),
(12, 3, 6),
(13, 6, 5);

-- --------------------------------------------------------

--
-- Table structure for table `novosti`
--

DROP TABLE IF EXISTS `novosti`;
CREATE TABLE IF NOT EXISTS `novosti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `naziv` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `kategorija` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sadrzaj` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_autora` int NOT NULL,
  `status` int NOT NULL,
  `datum` datetime NOT NULL,
  `tagovi` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`id_autora`)
) ENGINE=MyISAM AUTO_INCREMENT=18264 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `zahtevi`
--

DROP TABLE IF EXISTS `zahtevi`;
CREATE TABLE IF NOT EXISTS `zahtevi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_autora` int DEFAULT NULL,
  `id_novosti` int DEFAULT NULL,
  `datum` datetime DEFAULT NULL,
  `zahtev` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_autora` (`id_autora`),
  KEY `id_novosti` (`id_novosti`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
