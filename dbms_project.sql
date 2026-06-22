create database project_dbms;
use  project_dbms;
CREATE TABLE user (
    user_id VARCHAR(5) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    mobile_no VARCHAR(20)
);
drop table user;
CREATE TABLE user (
    user_id VARCHAR(5) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    country_code VARCHAR(5),
    phone_number VARCHAR(15)
);
INSERT INTO user VALUES
('U01','Nishant Parwani','nishant.parwani@gmail.com','+91','9876543210'),
('U02','Carolina Frederick','carolina.frederick@gmail.com','+1','4155552671'),
('U03','Ellijah Smith','ellijah.smith@gmail.com','+44','7700900123'),
('U04','Aditya Patel','aditya.patel20@gmail.com','+91','9123456789'),
('U05','Lucian Lee','lucian.lee@gmail.com','+65','81234567'),
('U06','Priyanka Sharma','priyanka.sharma@gmail.com','+91','9988766554'),
('U07','Alexander Morse','alexander.morse@gmail.com','+1','6475559012'),
('U08','Mohit Rana','mohit.rana@gmail.com','+91','9090980808'),
('U09','Pooja Sharma','pooja.sharma@gmail.com','+91','9012345678'),
('U10','Aman Shukla','aman.shukla@gmail.com','+61','412345678'),
('U11','Riya Verma','riya.verma@gmail.com','+91','9876500001'),
('U12','Arjun Mehta','arjun.mehta@gmail.com','+91','9876500002'),
('U13','Sneha Kapoor','sneha.kapoor@gmail.com','+91','9876500003'),
('U14','Rahul Nair','rahul.nair@gmail.com','+91','9876500004'),
('U15','Neha Joshi','neha.joshi@gmail.com','+91','9876500005');
select * from user;
CREATE TABLE address (
    address_id VARCHAR(5) PRIMARY KEY,
    user_id VARCHAR(5),
    address_line1 VARCHAR(255),
    street VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    country VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
INSERT INTO address VALUES
('A01','U01','Flat 12A, Shanti Towers','MG Road','Mumbai','Maharashtra','400001','India'),
('A02','U02','Apt 56, Bay Heights','Market Street','San Francisco','California','94103','USA'),
('A03','U03','Flat 45B, Baker Apartments','Baker Street','London','England','NW1 6XE','UK'),
('A04','U04','House 18, Patel Residency','CG Road','Ahmedabad','Gujarat','380009','India'),
('A05','U05','Unit 09, Orchard Residences','Orchard Road','Singapore','Central Region','238841','Singapore'),
('A06','U06','Flat 302, Nehru Enclave','Nehru Nagar','Bhopal','Madhya Pradesh','462003','India'),
('A07','U07','Suite 77, Queen Plaza','Queen Street','Toronto','Ontario','M5H 2N2','Canada'),
('A08','U08','House 14, Model Homes','Model Town Road','Ludhiana','Punjab','141002','India'),
('A09','U09','Flat 56, Civil Court Homes','Civil Lines','Jaipur','Rajasthan','302006','India'),
('A10','U10','Apt 88, Harbour View','George Street','Sydney','New South Wales','2000','Australia'),
('A11','U11','Flat 22, Green Park','Ring Road','Delhi','Delhi','110016','India'),
('A12','U12','House 10, Lake View','Lake Road','Udaipur','Rajasthan','313001','India'),
('A13','U13','Flat 5B, Sunrise Apt','Link Road','Mumbai','Maharashtra','400050','India'),
('A14','U14','House 77, Tech Park','Phase 2','Bangalore','Karnataka','560100','India'),
('A15','U15','Flat 9C, River View','Gomti Nagar','Lucknow','Uttar Pradesh','226010','India');
select * from address;
drop table payment;
CREATE TABLE payment (
    payment_id VARCHAR(5) PRIMARY KEY,
    cart_id VARCHAR(5),
    method VARCHAR(50),
    payment_status VARCHAR(20)
);
INSERT INTO payment VALUES
('PY01','C01','UPI','Completed'),
('PY02','C01','COD','Completed'),
('PY03','C02','NetBanking','Failed'),
('PY04','C03','UPI','Completed'),
('PY05','C03','COD','Completed'),
('PY06','C04','UPI','Failed'),
('PY07','C05','NetBanking','Completed'),
('PY08','C06','UPI','Completed'),
('PY09','C07','COD','Completed'),
('PY10','C08','NetBanking','Completed');
select * from payment;
CREATE TABLE review (
    review_id VARCHAR(5) PRIMARY KEY,
    user_id VARCHAR(5),
    p_id VARCHAR(5),
    rating DECIMAL(2,1) CHECK (rating BETWEEN 1 AND 5),
    review_text VARCHAR(255),
    review_date DATE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
INSERT INTO review VALUES
('R01','U01','P01',5.0,'Jacket quality is excellent and fits perfectly.','2026-02-01'),
('R02','U01','P03',4.0,'Shirt material is comfortable for daily wear.','2026-02-01'),
('R03','U02','P02',4.0,'Kurti fabric is soft and stitching is neat.','2026-02-02'),
('R04','U03','P04',3.0,'Jeans fit well but color fades slightly.','2026-02-03'),
('R05','U03','P09',4.0,'Track pants are comfortable for workouts.','2026-02-03'),
('R06','U04','P05',5.0,'Hoodie is very warm and stylish.','2026-02-04'),
('R07','U05','P07',4.5,'T-shirt quality is good for the price.','2026-02-05'),
('R08','U06','P06',4.0,'Saree looks elegant and feels premium.','2026-02-06'),
('R09','U07','P10',3.5,'Scarf is lightweight and stylish.','2026-02-07'),
('R10','U08','P08',5.0,'Dress design is beautiful and fits well.','2026-02-08');
select * from review;
ALTER TABLE user
ADD COLUMN firebase_uid VARCHAR(128) UNIQUE;
ALTER TABLE user
ADD CONSTRAINT unique_email UNIQUE (email);
desc user;
CREATE TABLE product(
p_id VARCHAR(5) PRIMARY KEY,
p_name VARCHAR(50),
description VARCHAR(255),
price INT,
stock_qty INT
);
INSERT INTO product (p_id, p_name, description, price, stock_qty) VALUES
('P01','Men''s Denim Jacket','Stylish full-sleeve denim jacket designed for casual wear, offering comfort, durability, and a modern fit.',2499,50),
('P02','Women''s Kurti','Elegant cotton kurti suitable for daily wear and festive occasions, providing breathability and comfort.',1799,60),
('P03','Men''s Formal Shirt','Premium-quality formal shirt with a tailored fit, ideal for office wear and professional settings.',1999,45),
('P04','Women''s Jeans','Slim-fit denim jeans crafted for everyday comfort and long-lasting wear.',2199,40),
('P05','Unisex Hoodie','Soft fleece hoodie designed for warmth and casual styling, suitable for all genders.',2229,35),
('P06','Women''s Saree','Traditional saree made from lightweight fabric, perfect for cultural events and special occasions.',1499,30),
('P07','Men''s T-Shirt','Comfortable cotton t-shirt with a regular fit, ideal for casual and everyday wear.',3499,55),
('P08','Women''s Dress','Stylish western dress designed for parties and outings, offering a flattering silhouette.',999,70),
('P09','Men''s Track Pants','Athletic track pants made for workouts and relaxed daily use, ensuring flexibility and comfort.',2999,25),
('P10','Unisex Scarf','Lightweight fashion scarf suitable for all seasons, enhancing both comfort and style.',799,80),

('P11','Men''s Leather Jacket','Classic leather jacket with a sleek design, perfect for winter fashion and durability.',4599,20),
('P12','Women''s Cardigan','Warm knitted cardigan suitable for layering during colder weather.',1899,35),
('P13','Men''s Casual Shirt','Lightweight casual shirt designed for everyday comfort and relaxed style.',1599,50),
('P14','Women''s Leggings','Stretchable cotton leggings ideal for daily wear and active lifestyles.',899,65),
('P15','Unisex Sweatshirt','Cozy sweatshirt designed for comfort and casual winter fashion.',1999,40),
('P16','Women''s Skirt','Stylish knee-length skirt suitable for office and casual outings.',1299,45),
('P17','Men''s Polo T-Shirt','Smart polo t-shirt offering a balance between casual and semi-formal style.',1699,55),
('P18','Women''s Jacket','Trendy lightweight jacket perfect for travel and seasonal wear.',2799,30),
('P19','Men''s Shorts','Comfortable cotton shorts designed for sports and summer wear.',1199,60),
('P20','Unisex Cap','Adjustable fashion cap suitable for casual outdoor activities.',499,75);
select * from product;
 
CREATE TABLE COLOR (
    color_id VARCHAR(5) PRIMARY KEY,
    color_name VARCHAR(20)
);

INSERT INTO COLOR VALUES
('C1', 'Black'),
('C2', 'Blue'),
('C3', 'Red'),
('C4', 'White'),
('C5', 'Green'),
('C6', 'Pink');
INSERT INTO COLOR VALUES
('C7', 'Yellow'),
('C8', 'Purple'),
('C9', 'Orange'),
('C10', 'Brown'),
('C11', 'Grey');
CREATE TABLE CART (
    cart_id VARCHAR(5) PRIMARY KEY,
    user_id VARCHAR(5),
    created_at DATE
);

INSERT INTO CART VALUES
('C01', 'U01', '2026-01-10'),
('C02', 'U02', '2026-01-11'),
('C03', 'U03', '2026-01-12'),
('C04', 'U04', '2026-01-13'),
('C05', 'U05', '2026-01-14'),
('C06', 'U06', '2026-01-15'),
('C07', 'U07', '2026-01-16'),
('C08', 'U08', '2026-01-17'),
('C09', 'U09', '2026-01-18'),
('C10', 'U10', '2026-01-19'),
('C11', 'U11', '2026-01-20'),
('C12', 'U12', '2026-01-21'),
('C13', 'U13', '2026-01-22'),
('C14', 'U14', '2026-01-23'),
('C15', 'U15', '2026-01-24');

CREATE TABLE SIZE (
    size_id VARCHAR(5) PRIMARY KEY,
    size_label VARCHAR(10)
);

INSERT INTO SIZE VALUES
('S1', 'XS'),
('S2', 'S'),
('S3', 'M'),
('S4', 'L'),
('S5', 'XL'),
('S6', 'XXL');

CREATE TABLE CART_ITEMS (
    cart_id VARCHAR(5),
    p_id VARCHAR(5),
    quantity INT,
    PRIMARY KEY (cart_id, p_id),
    FOREIGN KEY (cart_id) REFERENCES CART(cart_id)
);

ALTER TABLE CART add column quantity INT;
UPDATE CART SET quantity = 2 WHERE cart_id = 'C01';
UPDATE CART SET quantity = 1 WHERE cart_id = 'C02';
UPDATE CART SET quantity = 3 WHERE cart_id = 'C03';
UPDATE CART SET quantity = 2 WHERE cart_id = 'C04';
UPDATE CART SET quantity = 5 WHERE cart_id = 'C05';
UPDATE CART SET quantity = 1 WHERE cart_id = 'C06';
UPDATE CART SET quantity = 4 WHERE cart_id = 'C07';
UPDATE CART SET quantity = 2 WHERE cart_id = 'C08';
UPDATE CART SET quantity = 3 WHERE cart_id = 'C09';
UPDATE CART SET quantity = 1 WHERE cart_id = 'C10';
UPDATE CART SET quantity = 2 WHERE cart_id = 'C11';
UPDATE CART SET quantity = 6 WHERE cart_id = 'C12';
UPDATE CART SET quantity = 3 WHERE cart_id = 'C13';
UPDATE CART SET quantity = 2 WHERE cart_id = 'C14';
UPDATE CART SET quantity = 4 WHERE cart_id = 'C15';
select * from CART;
select * from product;
INSERT INTO CART_ITEMS VALUES
('C01','P01',1),
('C01','P03',1),

('C02','P02',1),

('C03','P05',2),
('C03','P01',1),

('C04','P03',1),
('C04','P06',1),

('C05','P03',1),
('C05','P02',1),
('C05','P07',3),

('C06','P04',1),

('C07','P08',1),
('C07','P05',1),
('C07','P09',2),

('C08','P01',1),
('C08','P10',1),

('C09','P03',1),
('C09','P06',2),

('C10','P02',1),



('C11','P07',2),

('C12','P05',3),
('C12','P09',1),
('C12','P04',1),
('C12','P11',1),

('C13','P06',2),
('C13','P01',1),


('C14','P10',2),

('C15','P02',1),
('C15','P03',1),
('C15','P08',2);
select * from cart_items;
select * from product;

CREATE TABLE PRODUCT_VARIANT (
    variant_id VARCHAR(6) PRIMARY KEY,
    p_id VARCHAR(5),
    size_id VARCHAR(5),
    color_id VARCHAR(5),
    stock_qty INT,
    FOREIGN KEY (p_id) REFERENCES PRODUCT(p_id),
    FOREIGN KEY (size_id) REFERENCES SIZE(size_id),
    FOREIGN KEY (color_id) REFERENCES COLOR(color_id)
);

INSERT INTO PRODUCT_VARIANT VALUES
('PV001','P01','S1','C1',10),
('PV002','P01','S2','C2',12),
('PV003','P01','S3','C3',8),
('PV004','P01','S4','C4',9),
('PV005','P01','S5','C5',7),
('PV006','P01','S6','C6',6),

('PV007','P02','S1','C2',11),
('PV008','P02','S2','C3',10),
('PV009','P02','S3','C4',12),
('PV010','P02','S4','C5',8),
('PV011','P02','S5','C6',9),
('PV012','P02','S6','C1',7),

('PV013','P03','S1','C3',14),
('PV014','P03','S2','C4',10),
('PV015','P03','S3','C5',12),
('PV016','P03','S4','C6',8),
('PV017','P03','S5','C1',6),
('PV018','P03','S6','C2',7),

('PV019','P04','S1','C4',13),
('PV020','P04','S2','C5',11),
('PV021','P04','S3','C6',9),
('PV022','P04','S4','C1',10),
('PV023','P04','S5','C2',8),
('PV024','P04','S6','C3',7),

('PV025','P05','S1','C5',15),
('PV026','P05','S2','C6',12),
('PV027','P05','S3','C1',11),
('PV028','P05','S4','C2',9),
('PV029','P05','S5','C3',8),
('PV030','P05','S6','C4',7),

('PV031','P06','S1','C6',14),
('PV032','P06','S2','C1',12),
('PV033','P06','S3','C2',10),
('PV034','P06','S4','C3',9),
('PV035','P06','S5','C4',8),
('PV036','P06','S6','C5',7),

('PV037','P07','S1','C1',16),
('PV038','P07','S2','C2',13),
('PV039','P07','S3','C3',12),
('PV040','P07','S4','C4',10),
('PV041','P07','S5','C5',9),
('PV042','P07','S6','C6',8),

('PV043','P08','S1','C2',15),
('PV044','P08','S2','C3',13),
('PV045','P08','S3','C4',12),
('PV046','P08','S4','C5',11),
('PV047','P08','S5','C6',9),
('PV048','P08','S6','C1',8),

('PV049','P09','S1','C3',14),
('PV050','P09','S2','C4',12),
('PV051','P09','S3','C5',10),
('PV052','P09','S4','C6',9),
('PV053','P09','S5','C1',8),
('PV054','P09','S6','C2',7),

('PV055','P10','S1','C4',13),
('PV056','P10','S2','C5',12),
('PV057','P10','S3','C6',10),
('PV058','P10','S4','C1',9),
('PV059','P10','S5','C2',8),
('PV060','P10','S6','C3',7),

('PV061','P11','S1','C5',15),
('PV062','P11','S2','C6',13),
('PV063','P11','S3','C1',12),
('PV064','P11','S4','C2',11),
('PV065','P11','S5','C3',9),
('PV066','P11','S6','C4',8),

('PV067','P12','S1','C6',14),
('PV068','P12','S2','C1',12),
('PV069','P12','S3','C2',11),
('PV070','P12','S4','C3',10),
('PV071','P12','S5','C4',9),
('PV072','P12','S6','C5',8),

('PV073','P13','S1','C1',16),
('PV074','P13','S2','C2',14),
('PV075','P13','S3','C3',12),
('PV076','P13','S4','C4',11),
('PV077','P13','S5','C5',9),
('PV078','P13','S6','C6',8),

('PV079','P14','S1','C2',15),
('PV080','P14','S2','C3',13),
('PV081','P14','S3','C4',12),
('PV082','P14','S4','C5',10),
('PV083','P14','S5','C6',9),
('PV084','P14','S6','C1',8),

('PV085','P15','S1','C3',14),
('PV086','P15','S2','C4',12),
('PV087','P15','S3','C5',11),
('PV088','P15','S4','C6',10),
('PV089','P15','S5','C1',9),
('PV090','P15','S6','C2',8),

('PV091','P16','S1','C4',13),
('PV092','P16','S2','C5',12),
('PV093','P16','S3','C6',11),
('PV094','P16','S4','C1',10),
('PV095','P16','S5','C2',9),
('PV096','P16','S6','C3',8),

('PV097','P17','S1','C5',15),
('PV098','P17','S2','C6',13),
('PV099','P17','S3','C1',12),
('PV100','P17','S4','C2',11),
('PV101','P17','S5','C3',10),
('PV102','P17','S6','C4',9),

('PV103','P18','S1','C6',14),
('PV104','P18','S2','C1',13),
('PV105','P18','S3','C2',12),
('PV106','P18','S4','C3',11),
('PV107','P18','S5','C4',10),
('PV108','P18','S6','C5',9),

('PV109','P19','S1','C1',16),
('PV110','P19','S2','C2',14),
('PV111','P19','S3','C3',13),
('PV112','P19','S4','C4',12),
('PV113','P19','S5','C5',10),
('PV114','P19','S6','C6',9),

('PV115','P20','S1','C2',15),
('PV116','P20','S2','C3',14),
('PV117','P20','S3','C4',13),
('PV118','P20','S4','C5',12),
('PV119','P20','S5','C6',11),
('PV120','P20','S6','C1',10);

ALTER TABLE user
DROP COLUMN new_user_id;

ALTER TABLE user
ADD COLUMN new_user_id INT AUTO_INCREMENT UNIQUE;

ALTER TABLE address ADD COLUMN new_user_id INT;

SET SQL_SAFE_UPDATES = 0;
UPDATE address a
JOIN user u ON a.user_id = u.user_id
SET a.new_user_id = u.new_user_id;
ALTER TABLE address DROP FOREIGN KEY address_ibfk_1;
ALTER TABLE address DROP COLUMN user_id;
ALTER TABLE address CHANGE new_user_id user_id INT;
ALTER TABLE address
ADD CONSTRAINT fk_address_user
FOREIGN KEY (user_id) REFERENCES user(new_user_id);

ALTER TABLE cart ADD COLUMN new_user_id INT;

UPDATE cart c
JOIN user u ON c.user_id = u.user_id
SET c.new_user_id = u.new_user_id;

SHOW CREATE TABLE cart;
ALTER TABLE cart DROP COLUMN user_id;
ALTER TABLE cart CHANGE new_user_id user_id INT;
ALTER TABLE cart
ADD CONSTRAINT fk_cart_user
FOREIGN KEY (user_id) REFERENCES user(new_user_id);

ALTER TABLE review ADD COLUMN new_user_id INT;
SET SQL_SAFE_UPDATES = 0;

UPDATE review r
JOIN user u ON r.user_id = u.user_id
SET r.new_user_id = u.new_user_id;
ALTER TABLE review DROP FOREIGN KEY review_ibfk_1;

ALTER TABLE review DROP COLUMN user_id;

ALTER TABLE review CHANGE new_user_id user_id INT;

ALTER TABLE review
ADD CONSTRAINT fk_review_user
FOREIGN KEY (user_id) REFERENCES user(new_user_id);

ALTER TABLE user DROP PRIMARY KEY;

ALTER TABLE user DROP COLUMN user_id;

ALTER TABLE user CHANGE new_user_id user_id INT AUTO_INCREMENT PRIMARY KEY;

SELECT * FROM address;
SELECT * FROM product;
desc product_variant;

ALTER TABLE product
ADD COLUMN category VARCHAR(50);

UPDATE product SET category = 'Men' WHERE p_id IN (
'P01','P03','P07','P09','P11','P13','P17','P19'
);
UPDATE product SET category = 'Women' WHERE p_id IN (
'P02','P04','P06','P08','P12','P14','P16','P18'
);
UPDATE product SET category = 'Unisex' WHERE p_id IN (
'P05','P10','P15','P20'
);

SHOW CREATE TABLE cart_items;

CREATE INDEX idx_product_name ON product(p_name);
CREATE INDEX idx_product_category ON product(category);

ALTER TABLE cart
ADD COLUMN total_price INT DEFAULT 0;

ALTER TABLE cart_items
ADD COLUMN variant_id INT NOT NULL;

SET SQL_SAFE_UPDATES = 0;
ALTER TABLE cart_items
MODIFY variant_id VARCHAR(20)  NOT NULL;
ALTER TABLE cart_items
DROP FOREIGN KEY cart_items_ibfk_1;
ALTER TABLE cart_items
DROP PRIMARY KEY;
ALTER TABLE cart_items
DROP COLUMN p_id;
ALTER TABLE cart_items
ADD PRIMARY KEY (cart_id, variant_id);

ALTER TABLE cart_items
ADD CONSTRAINT fk_cart_items_variant
FOREIGN KEY (variant_id)
REFERENCES product_variant(variant_id);

SELECT * FROM user;
SHOW CREATE TABLE address;

SHOW INDEX FROM product;
SHOW INDEX FROM product_variant;
SHOW INDEX FROM cart_items;
SHOW INDEX FROM review;
CREATE INDEX idx_review_pid ON review(p_id);
select * from cart_items;



