--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: User
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO "User";

--
-- Name: customer; Type: TABLE; Schema: public; Owner: User
--

CREATE TABLE public.customer (
    id integer NOT NULL,
    name character varying(25),
    email character varying(50),
    join_date timestamp without time zone
);


ALTER TABLE public.customer OWNER TO "User";

--
-- Name: customer_id_seq; Type: SEQUENCE; Schema: public; Owner: User
--

CREATE SEQUENCE public.customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customer_id_seq OWNER TO "User";

--
-- Name: customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: User
--

ALTER SEQUENCE public.customer_id_seq OWNED BY public.customer.id;


--
-- Name: item; Type: TABLE; Schema: public; Owner: User
--

CREATE TABLE public.item (
    id integer NOT NULL,
    name character varying(30),
    brand character varying(30),
    price integer,
    available boolean
);


ALTER TABLE public.item OWNER TO "User";

--
-- Name: item_id_seq; Type: SEQUENCE; Schema: public; Owner: User
--

CREATE SEQUENCE public.item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.item_id_seq OWNER TO "User";

--
-- Name: item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: User
--

ALTER SEQUENCE public.item_id_seq OWNED BY public.item.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: User
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    customer_id integer,
    item_id integer,
    quantity integer,
    amount_due integer,
    amount_paid integer,
    order_date timestamp without time zone
);


ALTER TABLE public.orders OWNER TO "User";

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: User
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO "User";

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: User
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: customer id; Type: DEFAULT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.customer ALTER COLUMN id SET DEFAULT nextval('public.customer_id_seq'::regclass);


--
-- Name: item id; Type: DEFAULT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.item ALTER COLUMN id SET DEFAULT nextval('public.item_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: User
--

COPY public.alembic_version (version_num) FROM stdin;
d6d2a68d3e15
\.


--
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: User
--

COPY public.customer (id, name, email, join_date) FROM stdin;
1	Walmart	\N	\N
2	Costco	\N	\N
3	Zara	zara@zara.com	2021-01-05 00:00:00
4	Pizza	info@pizza.com	2021-01-06 00:00:00
8	Pizza	info@pizza.com	2021-01-06 00:00:00
9	Pizza	info@pizza.com	2021-01-06 00:00:00
10	PC World	info@pcworld.com	2021-01-06 00:00:00
11	H & M		2021-01-06 00:00:00
12	Macy's	None	2021-01-06 00:00:00
13	JC Penny	email@JCPenny.com	2021-01-06 00:00:00
14	Amazing Savings	info@amazingsavings.com	2021-01-06 00:00:00
15	Yamaha	info@yamaha.com	2021-01-07 00:00:00
\.


--
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: User
--

COPY public.item (id, name, brand, price, available) FROM stdin;
1	keyboard	Fuji	23	t
2	speakers	Sony	85	t
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: User
--

COPY public.orders (id, customer_id, item_id, quantity, amount_due, amount_paid, order_date) FROM stdin;
2	2	2	10	850	\N	2021-01-06 00:00:00
3	3	2	8	680	\N	2021-01-06 00:00:00
4	3	1	8	184	\N	2021-01-06 00:00:00
\.


--
-- Name: customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: User
--

SELECT pg_catalog.setval('public.customer_id_seq', 15, true);


--
-- Name: item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: User
--

SELECT pg_catalog.setval('public.item_id_seq', 2, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: User
--

SELECT pg_catalog.setval('public.orders_id_seq', 4, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- Name: item item_name_key; Type: CONSTRAINT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_name_key UNIQUE (name);


--
-- Name: item item_pkey; Type: CONSTRAINT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(id);


--
-- Name: orders orders_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: User
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id);


--
-- PostgreSQL database dump complete
--

