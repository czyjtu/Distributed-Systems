from pydantic import BaseModel


class JobOffer(BaseModel):
    description: str 
    salary_lb: int 
    salary_ub: int 
    title: str 