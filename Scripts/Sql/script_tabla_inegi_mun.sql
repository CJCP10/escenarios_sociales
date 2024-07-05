USE psociales;

-- Crea tabla a nivel municipal con 
select cve_ent, cve_mun , min(cve_loc) as cve_loc
from inegi
group by cve_ent, cve_mun;
            
-- Crea tabal inegi a nivel municipal con la localidad minima
CREATE TABLE inegi_mun AS
select a.cve_ent, a.cve_mun, a.cve_loc, a.latitud, a.longitud
from inegi as a
INNER JOIN (select cve_ent, cve_mun, min(cve_loc) as cve_loc
		    from inegi
		    group by cve_ent, cve_mun) as b
ON a.cve_ent = b.cve_ent and a.cve_mun = b.cve_mun and a.cve_loc = b.cve_loc;