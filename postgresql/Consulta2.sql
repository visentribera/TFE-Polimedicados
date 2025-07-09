WITH ingresos_polimedicados AS (
    SELECT id_ingreso,
        CASE WHEN COUNT(DISTINCT id_medicamento) >= 5 THEN 'Polimedicado' ELSE 'No Polimedicado' END AS tipo_paciente
    FROM "Tratamientos"
    GROUP BY id_ingreso
),
ingresos_con_ram AS (
    SELECT DISTINCT id_ingreso
    FROM "Ram_Ingreso"
)
SELECT
    ip.tipo_paciente,
    COUNT(ip.id_ingreso) AS total_ingresos,
    COUNT(CASE WHEN icr.id_ingreso IS NOT NULL THEN 1 END) AS ingresos_con_ram,
    ROUND(100.0 * COUNT(CASE WHEN icr.id_ingreso IS NOT NULL THEN 1 END) / COUNT(ip.id_ingreso), 2) AS porcentaje_con_ram
FROM ingresos_polimedicados ip
LEFT JOIN ingresos_con_ram icr ON ip.id_ingreso = icr.id_ingreso
GROUP BY ip.tipo_paciente;
