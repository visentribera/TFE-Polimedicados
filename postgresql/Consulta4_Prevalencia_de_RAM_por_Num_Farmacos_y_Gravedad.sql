WITH conteo_medicamentos AS (
    SELECT 
        id_ingreso, 
        COUNT(DISTINCT id_medicamento) AS total_meds
    FROM public."Tratamientos"
    GROUP BY id_ingreso
    HAVING COUNT(DISTINCT id_medicamento) >= 5
),
ram_por_ingreso AS (
    SELECT
        id_ingreso,
        -- Consideramos la gravedad máxima en caso de varias RAM
        MAX(
            CASE 
                WHEN gravedad = 'Leve' THEN 1
                WHEN gravedad = 'Moderada' THEN 2
                WHEN gravedad = 'Grave' THEN 3
                ELSE 0
            END
        ) AS gravedad_num
    FROM public."Ram_Ingreso"
    GROUP BY id_ingreso
),
ingresos_y_ram AS (
    SELECT
        cm.id_ingreso,
        cm.total_meds,
        COALESCE(rpi.gravedad_num, 0) AS gravedad_num
    FROM conteo_medicamentos cm
    LEFT JOIN ram_por_ingreso rpi ON cm.id_ingreso = rpi.id_ingreso
)
SELECT
    total_meds,
    COUNT(*) AS total_ingresos,
    SUM(CASE WHEN gravedad_num > 0 THEN 1 ELSE 0 END) AS ingresos_con_ram,
    ROUND(100.0 * SUM(CASE WHEN gravedad_num > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS prevalencia_ram_pct,
    SUM(CASE WHEN gravedad_num = 1 THEN 1 ELSE 0 END) AS ram_leve,
    SUM(CASE WHEN gravedad_num = 2 THEN 1 ELSE 0 END) AS ram_moderada,
    SUM(CASE WHEN gravedad_num = 3 THEN 1 ELSE 0 END) AS ram_grave
FROM ingresos_y_ram
GROUP BY total_meds
ORDER BY total_meds;


