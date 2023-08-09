-- Script selects origin column, and SUM fans column as nb_fans, grouped in descending order

SELECT origin, SUM(fans) as nb_fans
	FROM metal_bands
	GROUP BY origin
	ORDER BY nb_fans DESC;

