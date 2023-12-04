CREATE TABLE in_usuario (
    us_id SERIAL PRIMARY KEY,
    us_nombre VARCHAR(100),
    us_username VARCHAR(50) UNIQUE,
    us_email VARCHAR(100) UNIQUE,
    us_password VARCHAR(100),
    us_codigo VARCHAR(100),
    us_rol VARCHAR(50)
);

CREATE TABLE in_categoria (
    cat_id SERIAL PRIMARY KEY,
    cat_nombre VARCHAR(255),
    cat_descripcion VARCHAR(255),
    cat_estado integer
);

CREATE TABLE in_producto (
    prod_id SERIAL PRIMARY KEY,
    prod_codigo VARCHAR(255),
    prod_nombre VARCHAR(255),
    prod_precio NUMERIC,
    prod_cantidad integer,
    prod_cat_id INTEGER,
    prod_estado integer,
    prod_fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prod_cat_id) REFERENCES in_categoria(cat_id)
);

CREATE TABLE in_proveedor (
    prov_id SERIAL PRIMARY KEY,
    prov_nombre VARCHAR(255),
    prov_telefono VARCHAR(20),
    prov_ruc VARCHAR(20),
    prov_correo VARCHAR(20),
    prov_estado integer
);

CREATE TABLE parametroadmin (
    para_id SERIAL PRIMARY KEY,
    para_cadena1 VARCHAR(255),
    para_cadena2 VARCHAR(255),
    para_fecha1 TIMESTAMP,
    para_fecha2 TIMESTAMP,
    para_int1 INTEGER,
    para_int2 INTEGER,
    para_correlativo INTEGER DEFAULT 0,
    para_prefijo INTEGER DEFAULT 0,
    para_estado INTEGER DEFAULT 0
);

select * from parametroadmin

insert into parametroadmin (para_prefijo,para_correlativo,para_cadena1) values(1,1,'AZUL');
insert into parametroadmin (para_prefijo,para_correlativo,para_cadena1) values(1,2,'BLANCO');
insert into parametroadmin (para_prefijo,para_correlativo,para_cadena1) values(1,3,'AMARILLO');
insert into parametroadmin (para_prefijo,para_correlativo,para_cadena1) values(1,4,'VERDE');
insert into parametroadmin (para_prefijo,para_correlativo,para_cadena1) values(1,5,'NEGRO');
insert into parametroadmin (para_prefijo,para_correlativo,para_cadena1) values(1,6,'ROSADO');
insert into parametroadmin (para_prefijo,para_correlativo,para_cadena1) values(1,7,'ROJO');


CREATE TABLE in_venta (
    vent_id SERIAL PRIMARY KEY,
    vent_usuario INTEGER NOT NULL,
    vent_cliente INTEGER NOT NULL,
    vent_direccion VARCHAR(255) NOT NULL,
    vent_fecha DATE NOT NULL,
    vent_total NUMERIC(10, 2) NOT NULL,
    vent_igv NUMERIC(10, 2) NOT NULL,
    vent_subtotal NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (vent_usuario) REFERENCES in_usuario(us_id)
);


CREATE TABLE in_ventadetalle (
    vent_det_id SERIAL PRIMARY KEY,
    vent_det_vent_id INTEGER NOT NULL,
    FOREIGN KEY (vent_det_vent_id) REFERENCES in_venta(vent_id),
    vent_item NUMERIC(10, 2) NOT NULL,
    vent_cantidad NUMERIC(10, 2) NOT NULL,
    vent_unidad VARCHAR(255) NOT NULL,
    vent_producto VARCHAR(255) NOT NULL,
    vent_valor NUMERIC(10, 2) NOT NULL,
    vent_subtotal NUMERIC(10, 2) NOT NULL
);

CREATE TABLE in_clientes (
    cl_id SERIAL PRIMARY KEY,
    cl_nombre VARCHAR(255) NOT NULL,
    cl_doc VARCHAR(20) NOT NULL,
    cl_email VARCHAR(255) NULL,
    cl_telefono VARCHAR(20) NULL,
    cl_fnacimiento DATE NULL,
    cl_direccion VARCHAR(255) NULL,
);

INSERT INTO bd_usuario(us_nombre,us_username,us_email,us_password,us_rol) VALUES('DevOps','Admin','admin@correo.com','123','Administrador')