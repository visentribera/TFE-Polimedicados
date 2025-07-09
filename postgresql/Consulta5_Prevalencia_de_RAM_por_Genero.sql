WITH ingresos_con_genero AS (
    SELECT 
        i.id_ingreso,
        p.genero
    FROM public."Ingresos" i
    JOIN public."Pacientes" p ON i.id_paciente = p.id_paciente
),
ingresos_con_ram AS (
    SELECT DISTINCT id_ingreso
    FROM public."Ram_Ingreso"
)
SELECT 
    g.genero,
    COUNT(*) AS total_ingresos,
    COUNT(r.id_ingreso) AS ingresos_con_ram,
    ROUND(100.0 * COUNT(r.id_ingreso) / COUNT(*), 2) AS prevalencia_ram_pct
FROM ingresos_con_genero g
LEFT JOIN ingresos_con_ram r ON g.id_ingreso = r.id_ingreso
GROUP BY g.genero
ORDER BY g.genero;
