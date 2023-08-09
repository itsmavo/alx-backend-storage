-- Script creates trigger that reduces quantity after a new order
CREATE TRIGGER decrease_quan AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name=NEW.item_name;
