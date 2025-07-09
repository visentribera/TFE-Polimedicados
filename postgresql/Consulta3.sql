WITH conteo_medicamentos AS (
    SELECT id_ingreso, COUNT(DISTINCT id_medicamento) AS total_meds
    FROM public."Tratamientos"
    GROUP BY id_ingreso
),
ingresos_polimedicados AS (
    SELECT i.id_ingreso, p.rango_edad
    FROM public."Ingresos" i
    JOIN public."Pacientes" p ON i.id_paciente = p.id_paciente
    JOIN conteo_medicamentos cm ON i.id_ingreso = cm.id_ingreso
    WHERE cm.total_meds >= 5
),
ram_por_ingreso AS (
    SELECT DISTINCT id_ingreso FROM public."Ram_Ingreso"
),
resumen AS (
    SELECT ip.rango_edad,
           COUNT(*) AS total_ingresos,
           COUNT(r.id_ingreso) AS ingresos_con_ram
    FROM ingresos_polimedicados ip
    LEFT JOIN ram_por_ingreso r ON ip.id_ingreso = r.id_ingreso
    GROUP BY ip.rango_edad
)
SELECT 
    rango_edad,
    total_ingresos,
    ingresos_con_ram,
    ROUND(100.0 * ingresos_con_ram / total_ingresos, 2) AS porcentaje_con_ram
FROM resumen
ORDER BY rango_edad;


