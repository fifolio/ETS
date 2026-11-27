from pydantic import BaseModel, Field

from app.schemas.plan_out import PlanOut
from app.schemas.time_saved_config_out import TimeSavedConfigOut
from app.schemas.topup_config_out import TopupConfigOut


class PlansResponse(BaseModel):
    plans: list[PlanOut]
    topup: TopupConfigOut = Field(description="The credit top-up rules, the same for every plan")
    payments_enabled: bool = Field(
        description=(
            "Whether payments are enabled or not, if not, the front-end should hide "
            "the payment options"
        )
    )
    time_saved: TimeSavedConfigOut = Field(
        description="How much reading time a scan saves, on average"
    )
