from sqlalchemy.orm import Session
from app.models.activity import Activity


def get_activity_depth(db: Session, activity: Activity) -> int:
    depth = 1
    current = activity
    while current.parent is not None:
        depth += 1
        current = current.parent
    return depth


def collect_descendant_ids(activity: Activity) -> list[int]:
    result = [activity.id]

    def dfs(node: Activity):
        for child in node.children:
            result.append(child.id)
            dfs(child)

    dfs(activity)
    return result