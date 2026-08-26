from pydantic import BaseModel

class StudentData(BaseModel):
    gender: str                     # "M" ou "F"
    NationalITy: str                # ex: "Morocco", "Jordan", "KW"...
    PlaceofBirth: str               # ex: "Morocco", "Jordan"...
    StageID: str                    # "lowerlevel", "MiddleSchool", "HighSchool"
    GradeID: str                    # ex: "G-04", "G-08"...
    SectionID: str                  # "A", "B", "C"
    Topic: str                      # ex: "Math", "Biology", "IT"...
    Semester: str                   # "F" (First) ou "S" (Second)
    Relation: str                   # "Father" ou "Mum"
    raisedhands: int                # nombre de fois où l'étudiant a levé la main
    VisITedResources: int           # nombre de ressources visitées
    AnnouncementsView: int          # nombre d'annonces consultées
    Discussion: int                 # participation aux discussions
    ParentAnsweringSurvey: str      # "Yes" ou "No"
    ParentschoolSatisfaction: str   # "Good" ou "Bad"
    StudentAbsenceDays: str         # "Under-7" ou "Above-7"

class PredictionResponse(BaseModel):
    prediction: str        # "L", "M" ou "H"
    risk_label: str         # "Low Risk", "Medium Risk", "High Risk"