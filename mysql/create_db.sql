-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema mobilitydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mobilitydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mobilitydb` DEFAULT CHARACTER SET utf8mb4 ;
USE `mobilitydb` ;

-- -----------------------------------------------------
-- Table `mobilitydb`.`car_regist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mobilitydb`.`car_regist` (
  `reg_date` TEXT NULL DEFAULT NULL,
  `sido` TEXT NULL DEFAULT NULL,
  `sigungu` TEXT NULL DEFAULT NULL,
  `car_type` TEXT NULL DEFAULT NULL,
  `usage_type` TEXT NULL DEFAULT NULL,
  `count` BIGINT NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `mobilitydb`.`faq`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mobilitydb`.`faq` (
  `category` TEXT NULL DEFAULT NULL,
  `question` TEXT NULL DEFAULT NULL,
  `answer` TEXT NULL DEFAULT NULL,
  `source` BIGINT NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `mobilitydb`.`population`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mobilitydb`.`population` (
  `region` VARCHAR(10) NOT NULL,
  `popul` INT NOT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
