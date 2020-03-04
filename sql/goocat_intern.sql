/*
 Navicat MySQL Data Transfer

 Source Server         : goocat_intern
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost:3306
 Source Schema         : goocat_intern

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : 65001

 Date: 04/03/2020 10:01:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_answer
-- ----------------------------
DROP TABLE IF EXISTS `user_answer`;
CREATE TABLE `user_answer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `QuestionID` int NOT NULL,
  `AnswerTitle` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `AnswerContent` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `AnswerTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_QuestionID` (`QuestionID`) USING BTREE,
  KEY `fk_UserID` (`UserID`) USING BTREE,
  CONSTRAINT `user_answer_ibfk_1` FOREIGN KEY (`QuestionID`) REFERENCES `user_question` (`id`),
  CONSTRAINT `user_id_ibfk` FOREIGN KEY (`UserID`) REFERENCES `user_info` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_answer
-- ----------------------------
BEGIN;
INSERT INTO `user_answer` VALUES (1, 1, 103, NULL, '这是第一个回答', '2020-03-04 09:27:15');
INSERT INTO `user_answer` VALUES (2, 1, 103, NULL, '这是第二个回答', '2020-03-04 09:27:20');
INSERT INTO `user_answer` VALUES (3, 3, 103, NULL, '这是第三个回答', '2020-03-04 09:27:38');
INSERT INTO `user_answer` VALUES (4, 4, 102, NULL, '这是第四个回答', '2020-03-04 09:29:45');
COMMIT;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `UserEmail` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `UserSchool` varchar(45) DEFAULT NULL,
  `UserPassword` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `UserGender` enum('Male','Female') DEFAULT NULL,
  `UserStatus` enum('0','1','2','3') DEFAULT NULL,
  `UserMute` enum('0','1') DEFAULT NULL,
  `UserFollow` varchar(45) DEFAULT NULL,
  `UserCollect` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_info
-- ----------------------------
BEGIN;
INSERT INTO `user_info` VALUES (1, '小蓝', 'test1', NULL, '123', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `user_info` VALUES (2, '小红', 'test2', NULL, '123', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `user_info` VALUES (3, '小明', 'test3', NULL, '123', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `user_info` VALUES (4, '小杨', 'test4', NULL, '123', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `user_info` VALUES (5, '小南', 'test5', NULL, '123', NULL, NULL, NULL, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for user_question
-- ----------------------------
DROP TABLE IF EXISTS `user_question`;
CREATE TABLE `user_question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `AnwserID` int DEFAULT NULL,
  `AnwserIDs` varchar(45) DEFAULT NULL,
  `QuestionTitle` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `QuestionContent` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `QuestionTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `QuestionStatus` enum('0','1','2','3') DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_AnwserID` (`AnwserID`) USING BTREE,
  KEY `fk_UserID1` (`UserID`) USING BTREE,
  CONSTRAINT `user_id_ib` FOREIGN KEY (`UserID`) REFERENCES `user_info` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of user_question
-- ----------------------------
BEGIN;
INSERT INTO `user_question` VALUES (100, 1, NULL, NULL, '这是第一个问题', 'balabala', '2020-03-04 08:55:09', NULL);
INSERT INTO `user_question` VALUES (101, 1, NULL, NULL, '这是第二个问题', 'balabala', '2020-03-04 08:55:38', NULL);
INSERT INTO `user_question` VALUES (102, 1, NULL, NULL, '这是第三个问题', 'balabala', '2020-03-04 08:55:46', NULL);
INSERT INTO `user_question` VALUES (103, 2, NULL, NULL, '这是第四个问题', 'balabala', '2020-03-04 08:56:11', NULL);
INSERT INTO `user_question` VALUES (104, 4, NULL, NULL, '这是第五个问题', 'ba la ba la', '2020-03-04 09:29:58', NULL);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
