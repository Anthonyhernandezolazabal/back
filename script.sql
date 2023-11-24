CREATE TABLE bd_usuario (
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

select * from bd_usuario

INSERT INTO bd_usuario(us_nombre,us_username,us_email,us_password,us_rol) VALUES('DevOps','Admin','admin@correo.com','123','Administrador')