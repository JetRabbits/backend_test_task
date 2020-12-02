--
-- views
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

CREATE OR REPLACE VIEW public.node_paths AS
with recursive n(id, path) as (
    select id, text(id) as path from public.nodes where parent_id is null
    union all
    select t.id, concat(path, '/', text(t.id)) from public.nodes t join n on t.parent_id = n.id
)
select id, '/'||path as path from n;

ALTER TABLE public.node_paths OWNER TO local_storage_admin;

--
-- views
--