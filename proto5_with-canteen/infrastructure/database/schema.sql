-- Create Role Table
CREATE TABLE IF NOT EXISTS role (
    role_id INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL
);

-- Create Mesh Table
CREATE TABLE IF NOT EXISTS mesh (
    mesh_id INTEGER PRIMARY KEY,
    mesh_name TEXT NOT NULL -- it should be UNIQUE
);

-- Create Employee Table
CREATE TABLE IF NOT EXISTS employee (
    emp_id INTEGER PRIMARY KEY,
    client_emp_id TEXT NOT NULL,
    emp_name TEXT NOT NULL,
    emp_dob DATE,
    rf_id INTEGER,
    face_id TEXT,
    mesh_id INTEGER REFERENCES mesh(mesh_id),
    role_id INTEGER REFERENCES role(role_id),
    emp_image BLOB
);

-- Create Finger Point Scan Table
CREATE TABLE IF NOT EXISTS finger_point_scan (
    fp_id INTEGER PRIMARY KEY,
    emp_id INTEGER REFERENCES employee(emp_id) UNIQUE,
    LL INTEGER,
    LR INTEGER,
    LM INTEGER,
    LI INTEGER,
    LT INTEGER,
    RL INTEGER,
    RR INTEGER,
    RM INTEGER,
    RI INTEGER,
    RT INTEGER
);

CREATE TABLE IF NOT EXISTS device (
    dev_id INTEGER PRIMARY KEY,
    dev_name TEXT NOT NULL,
    sr_no TEXT,
    mac_id TEXT,
    ip_add TEXT,
    dir_flag INTEGER,
    def_mode TEXT,
    mesh_id INTEGER REFERENCES mesh(mesh_id)
);

CREATE TABLE IF NOT EXISTS attlog (
    log_id INTEGER PRIMARY KEY,
    emp_id INTEGER REFERENCES employee(emp_id),
    log_time DATETIME,
    dir_flag INTEGER,
    dev_id INTEGER REFERENCES device(dev_id)
);

CREATE TABLE IF NOT EXISTS shift (
    shift_id INTEGER PRIMARY KEY,
    shift_name TEXT NOT NULL,
    from_time TIME,
    to_time TIME
);

CREATE TABLE IF NOT EXISTS menugroup (
    menugrp_id INTEGER PRIMARY KEY,
    menugrp_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS menu (
    menu_id INTEGER PRIMARY KEY,
    menugrp_id INTEGER REFERENCES menugroup(menugrp_id),
    menu_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS timeslot (
    timeslot_id INTEGER PRIMARY KEY,
    timeslot_name TEXT NOT NULL,
    from_time TIME,
    to_time TIME,
    shift_id INTEGER REFERENCES shift(shift_id),
    menugrp_id INTEGER REFERENCES menugroup(menugrp_id)
);

CREATE TABLE IF NOT EXISTS canlog (
    log_id INTEGER PRIMARY KEY,
    emp_id INTEGER REFERENCES employee(emp_id),
    log_time DATETIME,
    dir_flag INTEGER,
    dev_id INTEGER REFERENCES device(dev_id),
    menu_id INTEGER REFERENCES menu(menu_id)
);
