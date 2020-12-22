--
-- base data
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

COPY public.grants (role, url, post, remove, get_all, get_by_id) FROM stdin;
0	/	t	t	t	t
0	/rest/v1/resources	t	t	t	t
0	/rest/v1/sessions	t	t	t	t
0	/rest/v1/settings	t	t	t	t
0	/rest/v1/nodes	t	t	t	t
1	/rest/v1/nodes	t	t	t	t
3	/rest/v1/nodes	t	t	t	t
4	/rest/v1/nodes	f	f	t	t
5	/rest/v1/nodes	f	f	t	t
\.

COPY public.roles (id, name, sub_role_id) FROM stdin;
-1	Guest	-1
0	Admin	-1
4	Recepient Group	-1
5	Relative Group	4
6	Main Relative Group	4
3	Employee Group	4
2	Manager Group	1
1	Curator Group	3
\.

COPY public.node_types (id, name) FROM stdin;
1	directory
2	file
3	part-of-file
4	link
5	public-directory
\.

COPY public.node_providers (id, name) FROM stdin;
1	server
\.

COPY public.nodes (id, node_type, provider_id, name, owner_id, created_by, created_when) FROM stdin;
1948933c-136f-11eb-8307-0242ac120010	1	1	Новый год	00000000-0000-0000-0000-000000000000	6e44fb2e-2502-4b0c-b349-8eba55701cb9	2020-10-23 08:45:31+00
194b0400-136f-11eb-8307-0242ac120010	1	1	День победы	00000000-0000-0000-0000-000000000000	6e44fb2e-2502-4b0c-b349-8eba55701cb9	2020-10-23 08:45:31+00
194d39b4-136f-11eb-8307-0242ac120010	1	1	Масленица	00000000-0000-0000-0000-000000000000	6e44fb2e-2502-4b0c-b349-8eba55701cb9	2020-10-23 08:45:31+00
\.

COPY public.dual (dual) FROM stdin;
0
\.

--
-- base data
--
