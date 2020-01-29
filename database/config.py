from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

class Config:
    DB_NAME = 'OpenFoodFacts'

    TABLES = {}
    TABLES['product'] = (
        "CREATE TABLE IF NOT EXISTS `product` ("
        "  `id` INT NOT NULL AUTO_INCREMENT,"
        "  `product_name` VARCHAR(45) NOT NULL,"
        "  `url` VARCHAR(45) NULL,"
        "  `nutriscore_grade` VARCHAR(45) NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE = InnoDB)"

    TABLES['category'] = (
        "CREATE TABLE IF NOT EXISTS `category` ("
        "  `id` INT NOT NULL AUTO_INCREMENT,"
        "  `category_name` VARCHAR(45) NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['store'] = (
        "CREATE TABLE IF NOT EXISTS `store` ("
        "  `id` INT NOT NULL AUTO_INCREMENT,"
        "  `store_name` VARCHAR(255) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['substituted_product'] = (
        "CREATE TABLE IF NOT EXISTS `substituted_product` ("
        "  `id` INT NOT NULL AUTO_INCREMENT,"
        "  `substitution_product_id` INT NOT NULL,"
        "  PRIMARY KEY (`id`),"
        "  INDEX `fk_substituted_product_product_idx` (`product_id` ASC),"
        "  INDEX `fk_substituted_product_product1_idx` (`substitution_product_id` ASC),"
        "  CONSTRAINT `fk_substituted_product_product`"
        "     FOREIGN KEY (`product_id`)"
        "     REFERENCES `OpenFoodFacts`.`product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        "  CONSTRAINT `fk_substituted_product_product1`"
        "     FOREIGN KEY (`substitution_product_id`)"
        "     REFERENCES `OpenFoodFacts`.`product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        ") ENGINE=InnoDB")

    TABLES['category_has_product'] = (
        "CREATE TABLE IF NOT EXISTS `category_has_product` ("
        "  `category_id` INT NOT NULL,"
        "  `product_id` INT NOT NULL,"
        "  PRIMARY KEY (`category_id`, `product_id`),"
        "  INDEX `fk_category_has_product_product1_idx` (`product_id` ASC),"
        "  INDEX `fk_category_has_product_category1_idx` (`category_id` ASC),"
        "  CONSTRAINT `fk_category_has_product_category1`"
        "     FOREIGN KEY (`category_id`)"
        "     REFERENCES `OpenFoodFacts`.`category` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        "  CONSTRAINT `fk_category_has_product_product1`"
        "     FOREIGN KEY (`product_id`)"
        "     REFERENCES `OpenFoodFacts`.`product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        ") ENGINE=InnoDB")

    TABLES['store_has_product'] = (
        "CREATE TABLE IF NOT EXISTS `store_has_product` ("
        "  `store_id` INT NOT NULL,"
        "  `product_id` INT NOT NULL,"
        "  PRIMARY KEY (`store_id`, `product_id`),"
        "  INDEX `fk_store_has_product_product1_idx` (`product_id` ASC),"
        "  INDEX `fk_store_has_product_store1_idx` (`store_id` ASC),"
        "  CONSTRAINT `fk_store_has_product_store1`"
        "     FOREIGN KEY (`store_id`)"
        "     REFERENCES `OpenFoodFacts`.`store` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        "  CONSTRAINT `fk_store_has_product_product1`"
        "     FOREIGN KEY (`product_id`)"
        "     REFERENCES `OpenFoodFacts`.`product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        ") ENGINE=InnoDB")