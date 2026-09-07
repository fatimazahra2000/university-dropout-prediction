with ranked_students as (

    select
        _dlt_id,
        gender,
        nationality,
        placeofbirth,
        stageid,
        gradeid,
        sectionid,
        topic,
        semester,
        relation,
        raisedhands,
        visitedresources,
        announcementsview,
        discussion,
        parentansweringsurvey,
        parentschoolsatisfaction,
        studentabsencedays,
        class,

        row_number() over (
            partition by
                gender,
                nationality,
                placeofbirth,
                stageid,
                gradeid,
                sectionid,
                topic,
                semester,
                relation,
                raisedhands,
                visitedresources,
                announcementsview,
                discussion,
                parentansweringsurvey,
                parentschoolsatisfaction,
                studentabsencedays,
                class
            order by _dlt_id
        ) as duplicate_rank

    from {{ ref('stg_students') }}

),

deduplicated_students as (

    select
        gender,
        nationality,
        placeofbirth,
        stageid,
        gradeid,
        sectionid,
        topic,
        semester,
        relation,
        raisedhands,
        visitedresources,
        announcementsview,
        discussion,
        parentansweringsurvey,
        parentschoolsatisfaction,
        studentabsencedays,

        case
            when studentabsencedays = 'Under-7' then 0
            when studentabsencedays = 'Above-7' then 1
            else null
        end as absence_risk,

        class,
        class as risk_class

    from ranked_students

    where duplicate_rank = 1

)

select *
from deduplicated_students