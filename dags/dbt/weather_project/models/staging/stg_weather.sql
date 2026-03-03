with base as (
  select
      r.id,
      r.ingestion_timestamp,
      r.data.latitude as latitude,
      r.data.longitude as longitude,
      EXTRACT(DATE FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M', t)) as data,
      EXTRACT(TIME FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M', t)) as hora,
      PARSE_TIMESTAMP('%Y-%m-%dT%H:%M', t) as data_hora_completa, -- coluna original
      
      -- Temperatura explicitamente como FLOAT64
      CAST(r.data.hourly.temperature_2m[offset] AS FLOAT64) as temperatura,
      
      -- Humidade explicitamente como percentual (dividindo por 100)
      CAST(r.data.hourly.relativehumidity_2m[offset] AS FLOAT64) / 100.0 as humidade_percentual

  from {{source('data_weather', 'raw_weather')}} as r
  cross join unnest(r.data.hourly.time) as t with offset
),

ranking as (
  select *,
    row_number() over (
      partition by data, hora 
      order by ingestion_timestamp desc
    ) as rn
  from base
)

select 
  id,
  ingestion_timestamp,
  latitude,
  longitude,
  data,
  hora,
  data_hora_completa,
  
  -- Confirmando os tipos explicitamente
  temperatura,
  humidade_percentual as humidade

from ranking
where rn = 1