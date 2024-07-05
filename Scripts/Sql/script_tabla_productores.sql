USE psociales;

SELECT * FROM inegi order by cve_ent;
SELECT * FROM productores order by cve_ent;


-- Observamos primeras líneas
SELECT cve_ent, cve_mun, min(cve_loc) as cve_loc
from inegi
group by cve_ent, cve_mun;


-- INEGI A NIVEL MUNICIPAL
create table inegi_mun as
select a.cve_ent, entidad, a.cve_mun, a.municipio,  a.latitud, a.longitud
FROM inegi as a
inner join (
	SELECT cve_ent, cve_mun, min(cve_loc) as cve_loc
	from inegi
	group by cve_ent, cve_mun
) as b
ON a.cve_ent = b.cve_ent and a.cve_mun = b.cve_mun and a.cve_loc= b.cve_loc; 

-- Tabla productores completa INGI + CONAPO 
CREATE TABLE productores_mun AS
SELECT a.cultivo, a.cve_ent, b.entidad,  a.cve_mun, b.municipio, a.productores, a.escenario_marginacion, a.escenario_precio, b.latitud, b.longitud, c.im, c.gm, c.imn
FROM productores as a
LEFT JOIN inegi_mun as b
ON a.cve_ent = b.cve_ent and a.cve_mun = b.cve_mun
LEFT JOIN (
	select *
	FROM conapo_imm
	where year = 2020
) as c
ON a.cve_ent = c.cve_ent and a.cve_mun = c.cve_mun;


-- visualizamos primeros registros
SELECT *
FROM productores_mun;




 