PGDMP         #                {         
   db_colegio    15.2    15.3                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            	           1262    16739 
   db_colegio    DATABASE     }   CREATE DATABASE db_colegio WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE db_colegio;
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            
           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    16740    notas    TABLE     �   CREATE TABLE public.notas (
    notas integer NOT NULL,
    materia character varying NOT NULL,
    id_usuario integer NOT NULL
);
    DROP TABLE public.notas;
       public         heap    postgres    false    5            �            1259    16745    notas_id_usuario_seq    SEQUENCE     �   CREATE SEQUENCE public.notas_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.notas_id_usuario_seq;
       public          postgres    false    5    214                       0    0    notas_id_usuario_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.notas_id_usuario_seq OWNED BY public.notas.id_usuario;
          public          postgres    false    215            �            1259    16746    usuario    TABLE     �   CREATE TABLE public.usuario (
    nombre character varying NOT NULL,
    curso numeric DEFAULT 99 NOT NULL,
    tipo_usuario integer NOT NULL,
    password character varying NOT NULL,
    id integer NOT NULL
);
    DROP TABLE public.usuario;
       public         heap    postgres    false    5            �            1259    16752    usuario_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.usuario_id_seq;
       public          postgres    false    5    216                       0    0    usuario_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;
          public          postgres    false    217            j           2604    16753    notas id_usuario    DEFAULT     t   ALTER TABLE ONLY public.notas ALTER COLUMN id_usuario SET DEFAULT nextval('public.notas_id_usuario_seq'::regclass);
 ?   ALTER TABLE public.notas ALTER COLUMN id_usuario DROP DEFAULT;
       public          postgres    false    215    214            l           2604    16754 
   usuario id    DEFAULT     h   ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);
 9   ALTER TABLE public.usuario ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216                       0    16740    notas 
   TABLE DATA           ;   COPY public.notas (notas, materia, id_usuario) FROM stdin;
    public          postgres    false    214   )                 0    16746    usuario 
   TABLE DATA           L   COPY public.usuario (nombre, curso, tipo_usuario, password, id) FROM stdin;
    public          postgres    false    216   �                  0    0    notas_id_usuario_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.notas_id_usuario_seq', 1, false);
          public          postgres    false    215                       0    0    usuario_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.usuario_id_seq', 32, true);
          public          postgres    false    217            n           2606    16758    usuario pk_id 
   CONSTRAINT     K   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT pk_id PRIMARY KEY (id);
 7   ALTER TABLE ONLY public.usuario DROP CONSTRAINT pk_id;
       public            postgres    false    216            p           2606    16760    usuario u_id 
   CONSTRAINT     E   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT u_id UNIQUE (id);
 6   ALTER TABLE ONLY public.usuario DROP CONSTRAINT u_id;
       public            postgres    false    216            q           2606    16761    notas fk_us    FK CONSTRAINT     y   ALTER TABLE ONLY public.notas
    ADD CONSTRAINT fk_us FOREIGN KEY (id_usuario) REFERENCES public.usuario(id) NOT VALID;
 5   ALTER TABLE ONLY public.notas DROP CONSTRAINT fk_us;
       public          postgres    false    216    214    3182                l   x�3��M,I�M,�LN�4�2�t�,�1��KRsr��\#��1�	�cT� Y��ĢļL ��#4�9�Z n�mʙ�Phh
T����G5��I@>�\1z\\\ frA�            x�M�MO� ��3�b��@i�q�&�^�P�(F��C?�G^��g�s�(y��5��@�lF�Hi�������H
���M?�j%t�G�v�V���AUJ�27��K.����O;�`�;!;��ś��V��	>)�����Y�T�Ҙ�h�r�Vm��$��Wj�:�i3]�)ɟ��+�=�BS��:� ��3m\����t�[˥��ݦ���6�pL�y����8�Lxs��Ӏ�;�+yZ|{@�_�+g�     