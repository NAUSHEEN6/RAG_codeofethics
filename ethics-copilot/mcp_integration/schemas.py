from pydantic import BaseModel


class EthicsCase(BaseModel):

    case_id: str
    employee_question: str
    policy_section: str
    policy_page: int
    assessment: str
    status: str