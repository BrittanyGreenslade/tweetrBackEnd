-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 35.239.75.152    Database: sustainappbility
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.18-MariaDB-1:10.4.18+maria~stretch

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment_likes`
--

DROP TABLE IF EXISTS `comment_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_likes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `comment_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_likes_UN` (`comment_id`,`user_id`),
  KEY `comment_likes_FK_1` (`user_id`),
  CONSTRAINT `comment_likes_FK` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_likes_FK_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_likes`
--

LOCK TABLES `comment_likes` WRITE;
/*!40000 ALTER TABLE `comment_likes` DISABLE KEYS */;
INSERT INTO `comment_likes` VALUES (31,24,167),(28,24,172),(29,25,172),(30,30,172),(32,32,177);
/*!40000 ALTER TABLE `comment_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  `content` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `comments_FK` (`user_id`),
  KEY `comments_FK_1` (`tweet_id`),
  CONSTRAINT `comments_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comments_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (15,167,91,'again!','2021-07-02 21:48:08'),(24,172,163,'new comment','2021-07-06 20:39:11'),(25,172,163,'antoher one','2021-07-06 20:39:48'),(26,172,163,'again','2021-07-06 20:49:22'),(27,172,163,'post','2021-07-06 20:57:18'),(28,172,163,'post\n','2021-07-06 21:07:35'),(29,172,163,'post','2021-07-06 21:10:33'),(30,172,137,'','2021-07-06 21:16:53'),(31,167,162,'','2021-07-06 21:17:20'),(32,177,169,'first comment from da postman','2021-07-09 14:41:47');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_likes`
--

DROP TABLE IF EXISTS `tweet_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_likes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_likes_UN` (`user_id`,`tweet_id`),
  KEY `tweet_likes_FK_1` (`tweet_id`),
  CONSTRAINT `tweet_likes_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_likes_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=258 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_likes`
--

LOCK TABLES `tweet_likes` WRITE;
/*!40000 ALTER TABLE `tweet_likes` DISABLE KEYS */;
INSERT INTO `tweet_likes` VALUES (244,167,139),(243,167,163),(253,172,163),(257,177,163);
/*!40000 ALTER TABLE `tweet_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweets`
--

DROP TABLE IF EXISTS `tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweets` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `content` varchar(200) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `image_url` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweets_FK` (`user_id`),
  CONSTRAINT `tweets_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweets`
--

LOCK TABLES `tweets` WRITE;
/*!40000 ALTER TABLE `tweets` DISABLE KEYS */;
INSERT INTO `tweets` VALUES (91,167,'new post!','2021-07-02 20:19:05',NULL),(100,167,'new!','2021-07-05 13:37:49',NULL),(101,168,'first','2021-07-05 13:39:21',NULL),(102,167,'third','2021-07-05 13:39:21',NULL),(103,167,'second tweet','2021-07-05 13:39:22',NULL),(107,167,'again','2021-07-05 13:42:48',NULL),(108,167,'new post','2021-07-05 16:13:53',NULL),(109,167,'new post','2021-07-05 16:13:54',NULL),(135,167,'new tweet','2021-07-05 17:20:15',NULL),(136,167,'newer tweet','2021-07-05 17:50:00',NULL),(137,167,'post','2021-07-05 17:50:11',NULL),(138,167,'new','2021-07-05 17:52:14',NULL),(139,167,'post','2021-07-05 17:55:11',NULL),(149,172,'tweets','2021-07-05 21:29:32',NULL),(150,172,'tweets','2021-07-05 21:29:32',NULL),(151,172,'are','2021-07-05 21:29:34',NULL),(152,172,'fun','2021-07-05 21:29:40',NULL),(157,168,'new post','2021-07-05 21:40:38',NULL),(158,168,'again new','2021-07-05 21:43:13',NULL),(159,168,'wat','2021-07-05 21:43:18',NULL),(162,172,'same','2021-07-05 21:45:11',NULL),(163,172,'new','2021-07-06 00:14:05',NULL),(164,167,'only some tweest','2021-07-07 15:19:28',NULL),(165,167,'why','2021-07-07 15:19:30',NULL),(167,177,'first tweeeeest!','2021-07-08 17:28:47','new image url'),(168,177,'first tweeeeest!','2021-07-09 14:36:05','new image url'),(169,177,'first tweeeeest!','2021-07-09 14:36:20',NULL),(170,172,'new tweets','2021-07-10 01:46:08',NULL),(171,172,'new tweet','2021-07-10 01:46:25',NULL),(172,172,'new tweet','2021-07-10 01:48:08',NULL),(173,172,'new tweet','2021-07-10 02:03:33',NULL),(174,172,'new tewtnew tewtt','2021-07-10 02:07:17',NULL),(175,172,'new again','2021-07-10 02:07:31',NULL);
/*!40000 ALTER TABLE `tweets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_follows`
--

DROP TABLE IF EXISTS `user_follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_follows` (
  `user_id` int(10) unsigned NOT NULL COMMENT 'user who is following',
  `follow_id` int(10) unsigned NOT NULL COMMENT 'user who is followed',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_follows_un` (`follow_id`,`user_id`),
  KEY `user_follows_FK` (`user_id`),
  KEY `user_follows_FK_1` (`follow_id`),
  CONSTRAINT `user_follows_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_follows_FK_1` FOREIGN KEY (`follow_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_follows_check` CHECK (`user_id` <> `follow_id`)
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_follows`
--

LOCK TABLES `user_follows` WRITE;
/*!40000 ALTER TABLE `user_follows` DISABLE KEYS */;
INSERT INTO `user_follows` VALUES (167,168,100),(177,168,116),(177,172,113),(167,177,109);
/*!40000 ALTER TABLE `user_follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `login_token` varchar(80) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_session_UN` (`login_token`),
  UNIQUE KEY `user_session_un2` (`user_id`),
  KEY `user_session_FK` (`user_id`),
  CONSTRAINT `user_session_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
INSERT INTO `user_session` VALUES ('IngXLI2aoXHsnisI3QMt98XPyTvhTuki96aOohaAwoN8MaY5zkfXgXruS9dFvwc92xEY8iweozrS9-5r',172,172);
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(150) NOT NULL,
  `email` varchar(255) NOT NULL,
  `bio` varchar(200) NOT NULL,
  `birthdate` date NOT NULL,
  `image_url` text DEFAULT 'https://www.sibberhuuske.nl/wp-content/uploads/2016/10/default-avatar-300x300.png',
  `salt` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_UN` (`username`),
  UNIQUE KEY `users_un2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=178 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (167,'ZeroWasteCommunity','71b9b2a0399d3e7cc3fa0b6552dd1e13b0f63e100fda7e03cb160981ba93ac0ee9e001c4c11b9f6e59be8d87b7e3280d5688bba997030d88df4a73bb538f0b44','zerowaste@gmail.com','zero waste bio','1985-08-07','https://www.sibberhuuske.nl/wp-content/uploads/2016/10/default-avatar-300x300.png','JFBOQ6bv2j'),(168,'the.eco.warrior','a4d5acf02ad94159ca5f292e319a8aa38da0d5a664f805d7f55dccff6b2c6fa414604a151d53ae58311fd3e1d27c271d4bb71655292004a6ef5f498ed77801ba','ecowarrior1@earth.net','eco warrior bio','1993-08-07','https://www.sibberhuuske.nl/wp-content/uploads/2016/10/default-avatar-300x300.png','f7Kj439MeV'),(172,'MotherNeature','29bbe494a76021a18059f6932e2db3355053ed2e1bf710a888182320585c8c4d02152d0b08dfd71dce63dc8365c03a51ce132781cfaeef25b1b5b0e62211a7c9','motherneature1@gmail.com','mother neature bio','1985-08-07','https://www.sibberhuuske.nl/wp-content/uploads/2016/10/default-avatar-300x300.png','kKheXryfNF'),(177,'user5','09b48ab74b4a0af4f42862e8b4f794396a7e7405bb3e23d22d523d86061cbeff86da75a44401aba934370a028c0b51751425da9a228d9de38ba15082701cbb28','user5@gmail.com','new user 5 bio','1990-06-25','https://www.sibberhuuske.nl/wp-content/uploads/2016/10/default-avatar-300x300.png','PHmSgFmwvU');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'sustainappbility'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-09 20:14:23
