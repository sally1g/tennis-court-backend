-- Tennis Court Finder - Initial Database Schema
-- Run this SQL in Supabase SQL Editor

-- Create regions table
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE INDEX ix_regions_name ON regions(name);

-- Create courts table
CREATE TABLE courts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    address VARCHAR(300) NOT NULL,
    phone VARCHAR(20),
    description TEXT,
    url VARCHAR(500),
    region_id UUID NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE INDEX ix_courts_name ON courts(name);
CREATE INDEX ix_courts_region_id ON courts(region_id);

-- Create availability_status enum
CREATE TYPE availability_status AS ENUM ('available', 'reserved', 'unavailable');

-- Create availability table
CREATE TABLE availability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    court_id UUID NOT NULL REFERENCES courts(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    status availability_status NOT NULL,
    price INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    CONSTRAINT uq_court_date_time UNIQUE (court_id, date, time_slot)
);

CREATE INDEX ix_availability_court_id ON availability(court_id);
CREATE INDEX ix_availability_date ON availability(date);

-- Create alembic_version table for migration tracking
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INSERT INTO alembic_version VALUES ('cf232274005e');
