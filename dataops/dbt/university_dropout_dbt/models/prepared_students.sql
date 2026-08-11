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
    class as risk_class
from {{ ref('stg_students') }}