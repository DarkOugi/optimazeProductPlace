import datetime
from typing import Annotated
from pydantic import BaseModel, AfterValidator

ml_models = {
    'generic', 'apriori'
}


def check_date(dates: list[datetime.date]) -> list[datetime.date]:
    if len(dates) != 2:
        raise ValueError('Error size, need 2 date: start and end')
    if dates[0] > dates[1]:
        raise ValueError('Error dates : start > end')
    return dates


def check_modal(model: str = None) -> str | None:
    if model:
        if model in ml_models:
            return model
        raise ValueError('Error model, unknown ml model')
    return None


class Place(BaseModel):
    dates: Annotated[list[datetime.date], AfterValidator(check_date)]
    model: Annotated[str, AfterValidator(check_modal)] = None
