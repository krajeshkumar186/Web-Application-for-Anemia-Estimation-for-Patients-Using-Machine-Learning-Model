anemiahmg/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - anemia
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`anemia` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `anemia`;

/*Table structure for table `hmg` */

DROP TABLE IF EXISTS `hmg`;

CREATE TABLE `hmg` (
  `s.no` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`s.no`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `hmg` */

insert  into `hmg`(`s.no`,`name`,`email`,`password`) values (1,NULL,'q@q.com','123'),(2,'malli','malli@malli.com','123'),(3,'qqqq','p@q.com','11'),(4,'qqqq','qppp@q.com','11'),(5,'malli','malli@gmail.com','1111'),(6,'malleswar','malleswar@gmail.com','123'),(7,'vasudha','vasu@gmail.com','Vasu@123');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
