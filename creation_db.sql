-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema epicevents_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema epicevents_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `epicevents_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `epicevents_db` ;

-- -----------------------------------------------------
-- Table `epicevents_db`.`clients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `epicevents_db`.`clients` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(12) NOT NULL,
  `company_name` VARCHAR(255) NOT NULL,
  `created_date` DATE NOT NULL,
  `last_update` DATE NOT NULL,
  `contact_person` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `epicevents_db`.`departments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `epicevents_db`.`departments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `epicevents_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `epicevents_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_number` VARCHAR(20) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password_hash` VARCHAR(80) NOT NULL,
  `department_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `employee_number` (`employee_number` ASC) VISIBLE,
  UNIQUE INDEX `email` (`email` ASC) VISIBLE,
  INDEX `department_id` (`department_id` ASC) VISIBLE,
  CONSTRAINT `users_ibfk_1`
    FOREIGN KEY (`department_id`)
    REFERENCES `epicevents_db`.`departments` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `epicevents_db`.`contracts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `epicevents_db`.`contracts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT NULL,
  `total_amount` FLOAT NOT NULL,
  `commercial_contact_id` INT NULL DEFAULT NULL,
  `amount_due` FLOAT NOT NULL,
  `created_date` DATE NOT NULL,
  `is_signed` TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `client_id` (`client_id` ASC) VISIBLE,
  INDEX `commercial_contact_id` (`commercial_contact_id` ASC) VISIBLE,
  CONSTRAINT `contracts_ibfk_1`
    FOREIGN KEY (`client_id`)
    REFERENCES `epicevents_db`.`clients` (`id`),
  CONSTRAINT `contracts_ibfk_2`
    FOREIGN KEY (`commercial_contact_id`)
    REFERENCES `epicevents_db`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `epicevents_db`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `epicevents_db`.`events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `contract_id` INT NOT NULL,
  `client_id` INT NOT NULL,
  `event_name` VARCHAR(100) NOT NULL,
  `event_start_date` DATE NOT NULL,
  `event_end_date` DATE NOT NULL,
  `support_contact` VARCHAR(255) NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `attendees` INT NOT NULL,
  `notes` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `contract_id` (`contract_id` ASC) VISIBLE,
  INDEX `client_id` (`client_id` ASC) VISIBLE,
  CONSTRAINT `events_ibfk_1`
    FOREIGN KEY (`contract_id`)
    REFERENCES `epicevents_db`.`contracts` (`id`),
  CONSTRAINT `events_ibfk_2`
    FOREIGN KEY (`client_id`)
    REFERENCES `epicevents_db`.`clients` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
