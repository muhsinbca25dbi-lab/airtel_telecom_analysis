CREATE  INDEX IF NOT EXISTS ix_orders_custtomer
        on shop_orders(customer_id);