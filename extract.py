def extract_docs(cursor):
  query = """ 
    SELECT 
      p1.prestacion_id,
      p1.prestacion_alumno,
      CONCAT(p1.alumno_apellido, ", ", p1.alumno_nombre) as alumno_completo,
        p1.alumno_dni,
        o.os_nombre,
        CASE 
            WHEN EXISTS (
                SELECT 1 
                FROM v_prestaciones p2
                WHERE p2.prestacion_alumno = p1.prestacion_alumno
                  AND p2.prestipo_nombre_corto IN ('SAIE', 'MA-APOYO', 'AT')
                  AND p2.prestacion_estado IN (0,1)
                  AND p2.coordi_apellido IS NOT NULL
            ) THEN 1 ELSE 0
        END AS prest_saie,
        COUNT(DISTINCT CASE WHEN d.docalumnotipo_nombre = "DNI" 
        THEN d.docalumno_id END) AS cred_dni,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "CREDENCIAL_OS_ALUMNO" 
        THEN d.docalumno_id END) AS cred_os,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "CUD" 
        THEN d.docalumno_id END) AS cred_cud,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "AD" 
        AND d.docalumnoseccion_nombre = "TERAPIAS"
            AND d.docalumno_anio = "2025"
        THEN d.docalumno_id END) AS ad,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "ORDEN_MED" 
        AND d.docalumnoseccion_nombre = "TERAPIAS"
            AND d.docalumno_anio = "2025"
        THEN d.docalumno_id END) AS orden_med,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "RESUM_HIST_CLIN" 
        AND d.docalumnoseccion_nombre = "TERAPIAS"
            AND d.docalumno_anio = "2025"
        THEN d.docalumno_id END) AS rhc,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "PLAN_TRABAJO" 
        AND d.docalumnoseccion_nombre = "TERAPIAS"
            AND d.docalumno_anio = "2025"
        THEN d.docalumno_id END) AS plan_tr,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "PRESUPUESTO" 
        AND d.docalumnoseccion_nombre = "TERAPIAS"
            AND d.docalumno_anio = "2025"
        THEN d.docalumno_id END) AS presup,
      COUNT(DISTINCT CASE WHEN d.docalumnotipo_corto = "OTROS" 
        AND d.docalumnoseccion_nombre = "TERAPIAS"
            AND d.docalumno_anio = "2025"
        THEN d.docalumno_id END) AS otros,
      COUNT(DISTINCT CASE WHEN i.informecat_nombre = "Informe Inicial - ADMISIÓN" 
        THEN i.alumnoinforme_id END) AS inf_admision,
      COUNT(DISTINCT CASE WHEN i.informecat_nombre = "Informe Inicial - TERAPIAS" 
        THEN i.alumnoinforme_id END) AS inf_ini_ter,
      COUNT(DISTINCT CASE WHEN i.informecat_nombre = "⁠⁠⁠Informe Semestral - TERAPIAS" 
        THEN i.alumnoinforme_id END) AS inf_diag_ter,
      COUNT(DISTINCT CASE WHEN i.informecat_nombre = "⁠⁠Informe Final - TERAPIAS" 
        THEN i.alumnoinforme_id END) AS inf_final_ter
    FROM v_prestaciones p1
    JOIN v_os o 
      ON p1.prestacion_os = o.os_id
    LEFT JOIN v_docs_alumno d
      ON p1.prestacion_alumno = d.docalumno_alumno
    LEFT JOIN v_informes i 
      ON p1.prestacion_alumno = i.alumno_id
      AND i.alumnoinforme_anio = "2025"
    WHERE p1.prestipo_nombre_corto = 'TERAPIAS'
      AND p1.prestacion_estado_descrip = 'ACTIVA'
    GROUP BY p1.prestacion_alumno
    ORDER BY alumno_completo;
  """
  cursor.execute(query)
  return cursor.fetchall()

def extract_prest(cursor):

  query = """ 
    SELECT 
      anio,
        mes,
        SUM(altas) AS total_altas,
        SUM(bajas) AS total_bajas
    FROM (
      SELECT 
        YEAR(prestacion_fec_aut_OS) AS anio,
            MONTH(prestacion_fec_aut_OS) AS mes,
            1 AS altas,
                    0 AS bajas
      FROM v_prestaciones
        WHERE prestipo_nombre_corto = 'TERAPIAS'
      AND prestacion_fec_aut_OS IS NOT NULL
        
        UNION ALL
        
        SELECT
        YEAR(prestacion_fec_baja) AS anio,
            MONTH(prestacion_fec_baja) AS mes,
            0 AS altas,
            1 AS bajas
      FROM v_prestaciones
        WHERE prestipo_nombre_corto = 'TERAPIAS'
      AND prestacion_fec_baja IS NOT NULL 
        AND prestacion_fec_aut_OS IS NOT NULL
    ) t
    WHERE 
      anio != 2023
    GROUP BY anio, mes 
    ORDER BY anio, mes 
  """
  cursor.execute(query)

  return cursor.fetchall()
