-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 14, 2024 at 07:05 PM
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
(1, 'test.jpeg'),
(3, 'magic2.jpg'),
(4, 'jugavsdragibravo.png');

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

--
-- Dumping data for table `komentari`
--

INSERT INTO `komentari` (`id`, `vest_id`, `ime`, `komentar`) VALUES
(1, 1, 'Test', 'Dobra vest, nema sta!'),
(2, 1, 'test2', 'test2'),
(3, 1, 'test3', 'teest3'),
(4, 1, 'top', 'top'),
(5, 1, 'neko', 'nesto'),
(6, 2, 'test2', 'dobar komentar'),
(7, 2, 'coda', 'coda brat'),
(8, 2, 'Wow', 'radi'),
(9, 6, 'demo', 'demo tekst\r\n');

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

--
-- Dumping data for table `lajkovi_komentara`
--

INSERT INTO `lajkovi_komentara` (`id`, `id_komentara`, `ip_adresa`, `tip`) VALUES
(6, 1, '178.237.218.221', 0),
(9, 6, '178.237.218.221', 1),
(13, 6, '178.149.16.165', 1),
(14, 7, '178.149.16.165', 1);

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
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `lajkovi_vesti`
--

INSERT INTO `lajkovi_vesti` (`id`, `id_vesti`, `ip_adresa`, `tip`) VALUES
(11, 1, '178.237.218.220', 0),
(19, 1, '178.237.218.221', 1),
(24, 2, '178.237.218.221', 0),
(25, 2, '178.149.16.165', 1),
(26, 6, '178.149.16.165', 0);

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
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `novinari_kategorije`
--

INSERT INTO `novinari_kategorije` (`id`, `novinar_id`, `kategorija_id`) VALUES
(8, 5, 1),
(9, 6, 5),
(10, 6, 5),
(11, 3, 5);

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
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `novosti`
--

INSERT INTO `novosti` (`id`, `naziv`, `kategorija`, `sadrzaj`, `id_autora`, `status`, `datum`, `tagovi`) VALUES
(1, 'Demo novostii', '1', '<h2>What is Lorem Ipsum?</h2>\r\n<p><strong>Lorem Ipsum</strong>&nbsp;is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.<br><br><em><s>test<img style=\"height: 100px; width: 100px;\" src=\"https://imgur.com/gallery/ByJo3Xz\" alt=\"\"></s></em></p>\r\n<h2>Why do we use it?</h2>\r\n<p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).<br><br>&nbsp;</p>\r\n<h2>Where does it come from?m a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum et Malorum\" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of et</h2>\r\n<p>Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, frohics, very popular during the Renaissance. The first line of Lorem Ipsum, \"Lorem ipsum dolor sit amet..\", comes from a line in section 1.10.32.</p>\r\n<p>&nbsp;</p>\r\n<h2>Where can I get some?</h2>\r\n<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.</p>', 1, 0, '0000-00-00 00:00:00', ''),
(2, 'Novost 2', '2', '<p>Sedamnaestog sunčanog jutra, u zabačenom selu podno planina, mladi istraživač kroči stazom prepunom misterija. Sa svakim korakom osećao je uzbuđenje i tajanstvenu prisutnost prirode koja je &scaron;aptom komunicirala sa svakim drvećem. <strong>U daljini, brujanje reke dopiralo je do njegovih u&scaron;iju kao melodija koja je pozivala na istraživanje nepoznatog. Sunce je igralo svoju igru sa li&scaron;ćem, stvarajući sjenke koje su pričale priču o pro&scaron;losti i budućnosti istovremeno.</strong><br />\r\n&nbsp;</p>\r\n', 1, 0, '0000-00-00 00:00:00', ''),
(3, 'test', '1', '<p><img src=\"../static/uploads/test.jpeg\" alt=\"\" width=\"348\" height=\"261\"></p>\n<h2>What is Lorem Ipsum?</h2>\n<p><strong>Lorem Ipsum</strong>&nbsp;is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>', 2, 0, '0000-00-00 00:00:00', ''),
(4, 'test', '1', '<p><img src=\"../static/uploads/test.jpeg\" alt=\"\" width=\"340\" height=\"255\"></p>\r\n<h2>What is Lorem Ipsum?</h2>\r\n<p><strong>Lorem Ipsum</strong>&nbsp;is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>', 2, 1, '0000-00-00 00:00:00', ''),
(5, 'test 2', '1', '<h2>What is Lorem Ipsum?</h2>\n<p><strong>Lorem Ipsum</strong>&nbsp;is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.<img src=\"../static/uploads/test.jpeg\" alt=\"\" width=\"340\" height=\"255\"></p>', 2, 0, '0000-00-00 00:00:00', ''),
(6, 'Vest fudbal', '1', '<p><img src=\"../static/uploads/magic2.jpg\" alt=\"\" width=\"716\" height=\"477\"></p>\r\n<p>Uzbudljive vesti iz sveta sporta stižu nam danas, dok je fudbalski svet potresao neočekivan transfer jednog od najtalentovanijih mladih igrača. Prema na&scaron;im izvorima, virtuozni vezista, Maksimilian \"Magični\" Petrović, prelazi iz neprikosnovenog tima \"Vatrene Stene\" u evropskog giganta \"Neumoljivi Torpedi\".</p>\r\n<p>Transfer je postao tema broj jedan među ljubiteljima fudbala &scaron;irom sveta, jer se očekuje da će Petrovićev izuzetan talenat doneti novu dimenziju igri \"Neumoljivih Torpeda\". Maksimilian je pro&scaron;le sezone briljirao svojim driblinzima, preciznim pasovima i neodoljivim &scaron;utevima, stvarajući pravo malo čudo na terenu.</p>\r\n<p>Izvor blizak igraču otkriva nam da je sam Petrović bio iznenađen brzinom transfera, ali da je uzbuđen zbog novih izazova i prilike da igra za jedan od najprestižnijih klubova u Evropi. \"Neumoljivi Torpedi\" su već poznati po osvajanju mnogobrojnih trofeja, a sada će imati priliku da u svom sastavu imaju mladog čarobnjaka koji obećava da će zasijati na najvećim evropskim terenima.</p>\r\n<p>&nbsp;</p>', 1, 0, '0000-00-00 00:00:00', ''),
(7, 'Lorem ipsum', '5', '<h1>Lorem Ipsum</h1>\r\n<h4>\"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...\"</h4>\r\n<h5>\"Не постоји нико ко воли бол, ко га тражи и жели, једноставно зато што је бол...\"</h5>\r\n<p>&nbsp;</p>', 2, 0, '2024-02-06 22:02:57', '<p>lorem, ipsum, demo, tekst</p>'),
(8, 'test', '1', '<p>test</p>', 2, 0, '2024-02-06 22:42:07', 'test, test, test2'),
(9, 'test', '1', '<p>test</p>', 2, 0, '2024-02-06 22:42:20', 'test, test, test'),
(10, 'reste1', '1', '<p>test</p>', 2, 0, '2024-02-06 22:43:15', '2024-02-06 22:43:15'),
(12, 'aasdasda', '5', '<p>sadadasd</p>', 6, 0, '2024-02-14 16:49:11', 'dasda');

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
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `zahtevi`
--

INSERT INTO `zahtevi` (`id`, `id_autora`, `id_novosti`, `datum`, `zahtev`) VALUES
(1, 2, 10, '2024-02-06 23:42:34', 'Korisnik test je zatražio odobrenje za sledeću vest: reste'),
(2, 2, 9, '2024-02-06 23:46:35', 'Korisnik test je zatražio izmenu za sledeću vest: test'),
(3, 1, 1, '2024-02-08 12:17:25', 'Odobrenje'),
(12, 3, 14, '2024-02-14 17:20:05', 'Odobrenje');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;