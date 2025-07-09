WITH tratamientos_solapados AS (
    SELECT t1.id_ingreso, t1.id_medicamento AS med1, t2.id_medicamento AS med2
    FROM "Tratamientos" t1
    JOIN "Tratamientos" t2 ON t1.id_ingreso = t2.id_ingreso
        AND t1.id_medicamento < t2.id_medicamento
        AND t1.fecha_inicio <= t2.fecha_fin
        AND t2.fecha_inicio <= t1.fecha_fin
),
pacientes_polimedicados AS (
    SELECT id_ingreso
    FROM "Tratamientos"
    GROUP BY id_ingreso
    HAVING COUNT(DISTINCT id_medicamento) >= 5
),
ram_por_ingreso AS (
    SELECT ri.id_ingreso, r.codigo_cie, r.reaccion_adversa
    FROM "Ram_Ingreso" ri
    JOIN "Ram" r ON ri.id_ram = r.id_ram
),
principios_activos_por_medicamento AS (
    SELECT id_medicamento, principio_activo
    FROM "Medicamentos"
),
combinaciones_riesgo AS (
    SELECT 
        t.id_ingreso,
        pa1.principio_activo AS principio_1,
        pa2.principio_activo AS principio_2,
        COUNT(DISTINCT ri.id_ingreso) AS num_rams
    FROM tratamientos_solapados t
    JOIN pacientes_polimedicados pp ON t.id_ingreso = pp.id_ingreso
    JOIN ram_por_ingreso ri ON t.id_ingreso = ri.id_ingreso
    JOIN principios_activos_por_medicamento pa1 ON t.med1 = pa1.id_medicamento
    JOIN principios_activos_por_medicamento pa2 ON t.med2 = pa2.id_medicamento
    GROUP BY t.id_ingreso, pa1.principio_activo, pa2.principio_activo
)
SELECT principio_1, principio_2, SUM(num_rams) AS total_rams
FROM combinaciones_riesgo
GROUP BY principio_1, principio_2
ORDER BY total_rams DESC
LIMIT 10;
