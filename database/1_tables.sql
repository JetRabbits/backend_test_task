--
-- tables
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

CREATE TABLE public.dual (
    dual integer
);
ALTER TABLE public.dual OWNER TO local_storage_admin;

CREATE TABLE public.grants (
    role bigint,
    url text,
    post boolean NOT NULL,
    remove boolean NOT NULL,
    get_all boolean NOT NULL,
    get_by_id boolean NOT NULL
);
ALTER TABLE public.grants OWNER TO local_storage_admin;

CREATE TABLE public.roles (
    id bigint NOT NULL,
    name text NOT NULL,
    sub_role_id bigint
);
ALTER TABLE public.roles OWNER TO local_storage_admin;

CREATE TABLE public.sessions (
    id uuid DEFAULT public.uuid_generate_v1() NOT NULL,
    person_id uuid DEFAULT public.uuid_generate_v1() NOT NULL,
    role bigint,
    token text,
    ip text,
    created_when timestamp with time zone,
    mobile_version text,
    platform character varying(100)
);
ALTER TABLE public.sessions OWNER TO local_storage_admin;

CREATE TABLE public.settings (
    key character varying(100),
    value text
);
ALTER TABLE public.settings OWNER TO local_storage_admin;

CREATE TABLE public.node_types (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);
ALTER TABLE public.node_types OWNER TO local_storage_admin;

CREATE TABLE public.node_providers (
    id integer NOT NULL,
    name character varying(100)
);
ALTER TABLE public.node_providers OWNER TO local_storage_admin;

CREATE TABLE public.nodes(
    id uuid NOT NULL,
    node_type integer NOT NULL,
    parent_id uuid,
    provider_id integer NOT NULL,
    size_in_bytes bigint,
    name character varying(100) NOT NULL,
    description text,
    owner_id uuid NOT NULL,
    created_by uuid NOT NULL,
    created_when timestamp with time zone NOT NULL,
    modified_by uuid,
    modified_when timestamp with time zone
);
ALTER TABLE public.nodes OWNER TO local_storage_admin;

CREATE TABLE public.node_readers (
    node_id uuid NOT NULL,
    reader_id uuid NOT NULL
);
ALTER TABLE public.node_readers OWNER TO local_storage_admin;

CREATE TABLE public.node_writers (
    node_id uuid NOT NULL,
    writer_id uuid NOT NULL
);
ALTER TABLE public.node_writers OWNER TO local_storage_admin;

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (key);

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.node_types
    ADD CONSTRAINT node_types_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.node_providers
    ADD CONSTRAINT node_providers_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.nodes
    ADD CONSTRAINT nodes_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.node_readers
    ADD CONSTRAINT node_readers_pkey PRIMARY KEY (node_id, reader_id);

ALTER TABLE ONLY public.node_writers
    ADD CONSTRAINT node_writers_pkey PRIMARY KEY (node_id, writer_id);

ALTER TABLE ONLY public.nodes
    ADD CONSTRAINT nodes_node_type_fk FOREIGN KEY (node_type) REFERENCES public.node_types(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.nodes
    ADD CONSTRAINT nodes_parent_id_fk FOREIGN KEY (parent_id) REFERENCES public.nodes(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.nodes
    ADD CONSTRAINT nodes_provider_id_fk FOREIGN KEY (provider_id) REFERENCES public.node_providers(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.node_readers
    ADD CONSTRAINT node_readers_node_id_fk FOREIGN KEY (node_id) REFERENCES public.nodes(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.node_writers
    ADD CONSTRAINT node_writers_node_id_fk FOREIGN KEY (node_id) REFERENCES public.nodes(id) ON UPDATE CASCADE ON DELETE CASCADE;

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM local_storage_admin;
GRANT ALL ON SCHEMA public TO local_storage_admin;
GRANT ALL ON SCHEMA public TO PUBLIC;

--
-- tables
--