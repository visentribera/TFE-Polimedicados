-- Deshabilitar las restricciones de clave foránea temporalmente para evitar errores
SET session_replication_role = replica;

-- Comenzar la eliminación de datos desde las tablas más dependientes (hijas) hacia las independientes (padre)

-- 1. Eliminar datos de Ram_Ingreso (tabla más dependiente)
TRUNCATE TABLE public."Ram_Ingreso" RESTART IDENTITY CASCADE;

-- 2. Eliminar datos de Tratamientos
TRUNCATE TABLE public."Tratamientos" RESTART IDENTITY CASCADE;

-- 3. Eliminar datos de Ingresos
TRUNCATE TABLE public."Ingresos" RESTART IDENTITY CASCADE;

-- 4. Eliminar datos de Ram
TRUNCATE TABLE public."Ram" RESTART IDENTITY CASCADE;

-- 5. Eliminar datos de Medicamentos
TRUNCATE TABLE public."Medicamentos" RESTART IDENTITY CASCADE;

-- 6. Eliminar datos de Pacientes (tabla más independiente)
TRUNCATE TABLE public."Pacientes" RESTART IDENTITY CASCADE;

-- Volver a habilitar las restricciones de clave foránea
SET session_replication_role = DEFAULT;

-- Reiniciar manualmente las secuencias IDENTITY por si acaso
ALTER SEQUENCE public."Pacientes_id_paciente_seq" RESTART WITH 1;
ALTER SEQUENCE public."Medicamentos_id_medicamento_seq" RESTART WITH 1;
ALTER SEQUENCE public."Ram_id_ram_seq" RESTART WITH 1;
ALTER SEQUENCE public."Ingresos_id_ingreso_seq" RESTART WITH 1;