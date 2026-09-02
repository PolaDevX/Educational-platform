from checkout.models import Transaction, TransactionStatus
from courses.models import Course


def user_purchased_courses(request):
    user_email = request.session.get('purchaser_email')

    if not user_email and request.user.is_authenticated:
        user_email = request.user.email

    if not user_email:
        return {
            'my_courses': Course.objects.none()
        }

    transactions = Transaction.objects.filter(
        customer__email=user_email,
        status=TransactionStatus.Completed
    )

    course_ids = set()

    for tx in transactions:
        if tx.items:
            for item in tx.items:
                if isinstance(item, dict):
                    c_id = item.get('course_id') or item.get('id')
                    if c_id:
                        course_ids.add(c_id)
                elif item:
                    course_ids.add(item)

    if not course_ids:
        return {
            'my_courses': Course.objects.none()
        }

    purchased_courses = Course.objects.filter(
        pk__in=course_ids
    ).select_related(
        'teacher',
        'category'
    ).distinct()

    return {
        'my_courses': purchased_courses
    }