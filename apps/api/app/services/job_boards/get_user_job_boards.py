from app.constants.plans import PLANS
from app.services.job_boards.list_active_job_boards import list_active_job_boards
from app.services.job_boards.select_boards_for_plan import select_boards_for_plan
from app.services.plans.find_plan import find_plan
from app.types.authenticated_user import AuthenticatedUser
from app.types.user_job_boards import UserJobBoards


def get_user_job_boards(user: AuthenticatedUser) -> UserJobBoards:
    plan = find_plan(user.subscription) or PLANS[0]
    boards = select_boards_for_plan(list_active_job_boards(), plan.id)
    return UserJobBoards(boards=boards, plan=plan.id)
