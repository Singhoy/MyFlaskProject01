/*
 Navicat Premium Data Transfer

 Source Server         : hi
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost:3306
 Source Schema         : news1

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : 65001

 Date: 25/07/2018 23:32:56
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for info_category
-- ----------------------------
DROP TABLE IF EXISTS `info_category`;
CREATE TABLE `info_category`  (
  `create_time` datetime(0) DEFAULT NULL,
  `update_time` datetime(0) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of info_category
-- ----------------------------
INSERT INTO `info_category` VALUES ('2018-01-17 20:55:48', '2018-04-01 21:45:12', 1, '最新');
INSERT INTO `info_category` VALUES ('2018-01-17 20:55:49', '2018-01-17 20:55:50', 2, '股市');
INSERT INTO `info_category` VALUES ('2018-01-17 20:56:04', '2018-01-17 20:56:06', 3, '债市');
INSERT INTO `info_category` VALUES ('2018-01-17 20:56:18', '2018-01-17 20:56:20', 4, '商品');
INSERT INTO `info_category` VALUES ('2018-01-17 20:56:26', '2018-01-17 20:56:28', 5, '外汇');
INSERT INTO `info_category` VALUES ('2018-04-01 21:45:16', '2018-04-01 21:45:16', 6, '公司');

SET FOREIGN_KEY_CHECKS = 1;
