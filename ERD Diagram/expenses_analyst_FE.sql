-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema expense_analyst_DB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema expense_analyst_DB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `expense_analyst_DB` DEFAULT CHARACTER SET utf8 ;
USE `expense_analyst_DB` ;

-- -----------------------------------------------------
-- Table `expense_analyst_DB`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `expense_analyst_DB`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `expense_analyst_DB`.`transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `expense_analyst_DB`.`transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `month` INT NULL,
  `year` YEAR NULL,
  `description` VARCHAR(255) NULL,
  `amount` DECIMAL(10,2) NULL,
  `category` VARCHAR(40) NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_transactions_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_transactions_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `expense_analyst_DB`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
