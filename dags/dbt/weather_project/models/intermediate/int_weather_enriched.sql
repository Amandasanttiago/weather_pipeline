with base as (
    select * 
    from {{ ref('stg_weather') }}
)

select
    -- Gerar ID sequencial (não nulo)
    row_number() over (order by data, hora) as id_weather,
    
    *,
    
    extract(dayofweek from data) as dia_semana,

    case
        when hora between '06:00:00' and '11:59:59' then 'manha'
        when hora between '12:00:00' and '17:59:59' then 'tarde'
        when hora between '18:00:00' and '23:59:59' then 'noite'
        else 'madrugada'
    end as periodo_dia,

    case
        when temperatura >= 30 then 'muito_quente'
        when temperatura >= 25 then 'quente'
        when temperatura >= 18 then 'agradavel'
        else 'frio'
    end as classificacao_temperatura

from base