SELECT="""SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   fw.created,
   GREATEST(fw.modified, g.modified, p.modified) as modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   array_agg(DISTINCT g.name) as genres
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
"""

ORDER = " GROUP BY fw.id,g.modified, p.modified ORDER BY modified ASC"

SELECT_ALL = SELECT + ORDER

SELECT_LAST_UPDATE = SELECT + ' WHERE fw.modified > %s or  g.modified > %s or p.modified > %s  or fw.created > %s '+ ORDER



