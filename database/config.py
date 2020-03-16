#!/usr/bin/env python3
'''
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-02-14
@note    0.0.1 (2020-02-14) : Init file
'''


class Config:
    # Et la docstring ?

    TABLES = {}

    TABLES['product'] = (
        # pourquoi avoir fait ligne par ligne et pas avec """...""" ?
        # SQL s'en fout des espaces
        """CREATE TABLE `product` (
          `id` bigint NOT NULL,
          `product_name` varchar(255) NOT NULL,
          `url` varchar(255) NOT NULL,
          `nutriscore_grade` varchar(1) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE = InnoDB; """
        # Engine InnoDB est le défaut désormais, pas la peine de le mettre
        # Attention à la collation, par contre. Opter pour utf8mb4
    )

    TABLES['category'] = (  # idem
        "CREATE TABLE `category` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `category_name` varchar(400) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"
    )

    TABLES['store'] = (  # idem
        "CREATE TABLE `store` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `store_name` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"
    )

    TABLES['substituted_product'] = (  # idem
        "  CREATE TABLE `substituted_product` ("
        "  `substitution_product_id` bigint NOT NULL,"
        "  `product_id` BIGINT NOT NULL,"
        "  INDEX `fk_substituted_product_product_idx` (`product_id` ASC),"
        "  INDEX `fk_substituted_product_product1_idx` (`substitution_product_id` ASC),"
        "  CONSTRAINT `fk_substituted_product_product`"
        "     FOREIGN KEY (`product_id`)"
        "     REFERENCES `product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        "  CONSTRAINT `fk_substituted_product_product1`"
        "     FOREIGN KEY (`substitution_product_id`)"
        "     REFERENCES `product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        "  CONSTRAINT PK_favorite"
        "     PRIMARY KEY (`substitution_product_id`, `product_id`)"
        ") ENGINE=InnoDB"
    )

    TABLES['category_has_product'] = (  # idem
        "  CREATE TABLE `category_has_product` ("
        "  `category_id` int NOT NULL,"
        "  `product_id` bigint NOT NULL,"
        "  PRIMARY KEY (`category_id`, `product_id`),"
        "  INDEX `fk_category_has_product_product1_idx` (`product_id` ASC),"
        "  INDEX `fk_category_has_product_category1_idx` (`category_id` ASC),"
        "  CONSTRAINT `fk_category_has_product_category1`"
        "     FOREIGN KEY (`category_id`)"
        "     REFERENCES `category` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        "  CONSTRAINT `fk_category_has_product_product1`"
        "     FOREIGN KEY (`product_id`)"
        "     REFERENCES `product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION"
        ") ENGINE=InnoDB"
    )

    TABLES['store_has_product'] = (  # idem
        "  CREATE TABLE `store_has_product` ("
        "  `store_id` int NOT NULL,"
        "  `product_id` bigint NOT NULL,"
        "  PRIMARY KEY (`store_id`, `product_id`),"
        "  INDEX `fk_store_has_product_product1_idx` (`product_id` ASC),"
        "  INDEX `fk_store_has_product_store1_idx` (`store_id` ASC),"
        "  CONSTRAINT `fk_store_has_product_store1`"
        "     FOREIGN KEY (`store_id`)"
        "     REFERENCES `store` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION,"
        "  CONSTRAINT `fk_store_has_product_product1`"
        "     FOREIGN KEY (`product_id`)"
        "     REFERENCES `product` (`id`)"
        "     ON DELETE NO ACTION"
        "     ON UPDATE NO ACTION"
        ") ENGINE=InnoDB"
    )
