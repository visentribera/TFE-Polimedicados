\c Polimedicados  -- Cambia a la base de datos recién creada (Current database)


-- Table: public.Pacientes

-- DROP TABLE IF EXISTS public."Pacientes";

CREATE TABLE IF NOT EXISTS public."Pacientes"
(
    id_paciente integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    rango_edad smallint NOT NULL,
    genero "char" NOT NULL,
    CONSTRAINT "Pacientes_pkey" PRIMARY KEY (id_paciente),
    CONSTRAINT rango_edad_valido CHECK (rango_edad >= 1 AND rango_edad <= 3) NOT VALID,
    CONSTRAINT genero_valido CHECK (genero::text = ANY (ARRAY['M'::"char"::text, 'F'::"char"::text, 'O'::"char"::text])) NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Pacientes"
    OWNER to postgres;
-- Index: idx_pacientes_genero_edad

-- DROP INDEX IF EXISTS public.idx_pacientes_genero_edad;

CREATE INDEX IF NOT EXISTS idx_pacientes_genero_edad
    ON public."Pacientes" USING btree
    (genero ASC NULLS LAST, rango_edad ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;



-- Table: public.Medicamentos

-- DROP TABLE IF EXISTS public."Medicamentos";

CREATE TABLE IF NOT EXISTS public."Medicamentos"
(
    codigo_atc character varying(7) COLLATE pg_catalog."default" NOT NULL,
    principio_activo text COLLATE pg_catalog."default",
    id_medicamento integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT "Medicamentos_pkey" PRIMARY KEY (id_medicamento),
    CONSTRAINT "Medicamentos_codigo_atc_key" UNIQUE (codigo_atc),
    CONSTRAINT codigo_atc_valido CHECK (codigo_atc::text ~ '^[A-Z][0-9]{2}[A-Z]{2}[0-9]{2}$'::text)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Medicamentos"
    OWNER to postgres;



-- Table: public.Ram

-- DROP TABLE IF EXISTS public."Ram";

CREATE TABLE IF NOT EXISTS public."Ram"
(
    codigo_cie character varying(10) COLLATE pg_catalog."default" NOT NULL,
    reaccion_adversa text COLLATE pg_catalog."default",
    id_ram integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT "Ram_pkey" PRIMARY KEY (id_ram)
        INCLUDE(id_ram),
    CONSTRAINT "Ram_codigo_cie_key" UNIQUE (codigo_cie)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Ram"
    OWNER to postgres;



-- Table: public.Ingresos

-- DROP TABLE IF EXISTS public."Ingresos";

CREATE TABLE IF NOT EXISTS public."Ingresos"
(
    id_ingreso integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    fecha_ingreso date NOT NULL,
    fecha_alta date NOT NULL,
    id_paciente integer NOT NULL,
    CONSTRAINT "Ingresos_pkey" PRIMARY KEY (id_ingreso),
    CONSTRAINT "Ingresos_id_paciente_fkey" FOREIGN KEY (id_paciente)
        REFERENCES public."Pacientes" (id_paciente) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Ingresos"
    OWNER to postgres;
-- Index: idx_ingresos_fechas

-- DROP INDEX IF EXISTS public.idx_ingresos_fechas;

CREATE INDEX IF NOT EXISTS idx_ingresos_fechas
    ON public."Ingresos" USING btree
    (fecha_ingreso ASC NULLS LAST, fecha_alta ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_ingresos_id_paciente

-- DROP INDEX IF EXISTS public.idx_ingresos_id_paciente;

CREATE INDEX IF NOT EXISTS idx_ingresos_id_paciente
    ON public."Ingresos" USING btree
    (id_paciente ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;



-- Table: public.Tratamientos

-- DROP TABLE IF EXISTS public."Tratamientos";

CREATE TABLE IF NOT EXISTS public."Tratamientos"
(
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    dosis character varying(10) COLLATE pg_catalog."default" NOT NULL,
    id_ingreso integer NOT NULL,
    id_medicamento integer NOT NULL,
    CONSTRAINT "Tratamientos_pkey" PRIMARY KEY (id_ingreso, id_medicamento),
    CONSTRAINT "Tratamientos_id_ingreso_fkey" FOREIGN KEY (id_ingreso)
        REFERENCES public."Ingresos" (id_ingreso) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "Tratamientos_id_medicamento_fkey" FOREIGN KEY (id_medicamento)
        REFERENCES public."Medicamentos" (id_medicamento) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT dosis_valida CHECK (dosis::text = ANY (ARRAY['Baja'::character varying, 'Media'::character varying, 'Alta'::character varying]::text[])) NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Tratamientos"
    OWNER to postgres;
-- Index: idx_tratamientos_fechas

-- DROP INDEX IF EXISTS public.idx_tratamientos_fechas;

CREATE INDEX IF NOT EXISTS idx_tratamientos_fechas
    ON public."Tratamientos" USING btree
    (fecha_inicio ASC NULLS LAST, fecha_fin ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_tratamientos_id_medicamento

-- DROP INDEX IF EXISTS public.idx_tratamientos_id_medicamento;

CREATE INDEX IF NOT EXISTS idx_tratamientos_id_medicamento
    ON public."Tratamientos" USING btree
    (id_medicamento ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;



-- Table: public.Ram_Ingreso

-- DROP TABLE IF EXISTS public."Ram_Ingreso";

CREATE TABLE IF NOT EXISTS public."Ram_Ingreso"
(
    id_ingreso integer NOT NULL,
    gravedad character varying(10) COLLATE pg_catalog."default" NOT NULL,
    id_ram integer NOT NULL,
    CONSTRAINT "Ram_Ingreso_pkey" PRIMARY KEY (id_ingreso, id_ram)
        INCLUDE(id_ingreso, id_ram),
    CONSTRAINT "Ram_Ingreso_id_ingreso_fkey" FOREIGN KEY (id_ingreso)
        REFERENCES public."Ingresos" (id_ingreso) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "Ram_Ingreso_id_ram_fkey" FOREIGN KEY (id_ram)
        REFERENCES public."Ram" (id_ram) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT gravedad_valida CHECK (gravedad::text = ANY (ARRAY['Leve'::character varying::text, 'Moderada'::character varying::text, 'Grave'::character varying::text])) NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Ram_Ingreso"
    OWNER to postgres;
-- Index: idx_ram_ingreso_gravedad

-- DROP INDEX IF EXISTS public.idx_ram_ingreso_gravedad;

CREATE INDEX IF NOT EXISTS idx_ram_ingreso_gravedad
    ON public."Ram_Ingreso" USING btree
    (gravedad COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_ram_ingreso_id_ram

-- DROP INDEX IF EXISTS public.idx_ram_ingreso_id_ram;

CREATE INDEX IF NOT EXISTS idx_ram_ingreso_id_ram
    ON public."Ram_Ingreso" USING btree
    (id_ram ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;