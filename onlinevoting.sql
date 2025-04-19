-- Modified onlinevoting.sql for a fresh application
-- Only the admin account is inserted into the login table.

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Database: `onlinevoting`

-- --------------------------------------------------------
-- Table structure for table `candidates`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `candidates`;
CREATE TABLE IF NOT EXISTS `candidates` (
  `candidateid` int NOT NULL AUTO_INCREMENT,
  `cid` int NOT NULL,
  `admno` varchar(30) NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT '1',
  `symbol` varchar(100) DEFAULT NULL,
  `std_un` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`candidateid`),
  UNIQUE KEY `symbol` (`symbol`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------
-- Table structure for table `complaints`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `complaints`;
CREATE TABLE IF NOT EXISTS `complaints` (
  `cmpid` int NOT NULL AUTO_INCREMENT,
  `time` timestamp(5) NOT NULL DEFAULT CURRENT_TIMESTAMP(5),
  `email` varchar(20) NOT NULL,
  `title` varchar(20) NOT NULL,
  `content` varchar(10) NOT NULL,
  `status` varchar(1) NOT NULL DEFAULT '0',
  `reply` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT '0',
  PRIMARY KEY (`cmpid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------
-- Table structure for table `contest`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `contest`;
CREATE TABLE IF NOT EXISTS `contest` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `starttime` varchar(10) NOT NULL,
  `endtime` varchar(10) NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT '1',
  `designation` varchar(30) NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for table `electoralroll`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `electoralroll`;
CREATE TABLE IF NOT EXISTS `electoralroll` (
  `er_id` int NOT NULL AUTO_INCREMENT,
  `admno` varchar(10) NOT NULL,
  `cid` int NOT NULL,
  `candidateid` int DEFAULT '0',
  `votingtime` time(5) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`er_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------
-- Table structure for table `login`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `email` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `status` varchar(2) DEFAULT NULL,
  `usertype` varchar(2) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- Insert only the admin account into the login table.
INSERT INTO `login` (`email`, `password`, `status`, `usertype`) VALUES
('admin@stcet.org', 'admin123', '1', '0');

-- --------------------------------------------------------
-- Table structure for table `registration`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `registration`;
CREATE TABLE IF NOT EXISTS `registration` (
  `stdid` int NOT NULL AUTO_INCREMENT,
  `email` varchar(30) NOT NULL,
  `admno` varchar(10) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `lname` varchar(30) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(7) NOT NULL,
  `rollno` int NOT NULL,
  `semester` varchar(5) NOT NULL,
  `branch` varchar(10) NOT NULL,
  `course` varchar(10) NOT NULL,
  `phn` varchar(10) NOT NULL,
  `address` varchar(30) NOT NULL,
  `state` varchar(20) NOT NULL,
  `district` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL,
  `pincode` int NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `admno` (`admno`),
  UNIQUE KEY `stdid` (`stdid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------
-- Table structure for table `time`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `time`;
CREATE TABLE IF NOT EXISTS `time` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
