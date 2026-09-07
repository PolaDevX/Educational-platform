from django.db import models
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.translation import gettext as _
import stripe

from checkout.webhooks import make_order
from django_ecommerce import settings
from .models import AboutPageContent, Course, Category, Cart, Lesson, LessonComment, Order, OrderProduct, StudentReview
from checkout.models import Transaction, TransactionStatus
from django.contrib.auth.decorators import login_required

def index(request):
    courses = Course.objects.select_related('teacher', 'category').filter(featured=True)
    return render(request, 'index.html', {'courses': courses})


def course_detail(request, pid):
    course = get_object_or_404(Course.objects.select_related('teacher', 'category'), pk=pid)

    has_bought = False
    if request.user.is_authenticated:
        has_bought = Order.objects.filter(
            user=request.user, 
            orderproduct__course=course, 
            status='completed'
        ).exists()

    return render(
        request, 'course_details.html', {'course': course,
                 'has_bought': has_bought}
    )

@login_required
def buy_now(request, pid):
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key
    cart_model = Cart.objects.filter(session_id=session_id).last()
    course = get_object_or_404(Course, pk=pid)

    has_bought = Order.objects.filter(
        user=request.user, 
        orderproduct__course=course, 
        status='completed'
    ).exists()

    if has_bought:
        return redirect('course_learn', pk=course.id)

    if cart_model is None:
        Cart.objects.create(session_id=session_id, items=[pid])
    elif pid not in cart_model.items:
        cart_model.items.append(pid)
        cart_model.save()

    return redirect('checkout')


def category(request, cid=None):
    cat = None
    query = request.GET.get('query')
    where = {}

    if cid:
        cat = get_object_or_404(Category, pk=cid)
        where['category_id'] = cid

    if query:
        where['name__icontains'] = query
        
    # بنفلتر الكورسات
    courses = Course.objects.filter(**where).select_related('teacher', 'category')
    categories = Category.objects.all()

    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(
        request, 'category.html', {
            'page_obj': page_obj, 
            'category': cat,  
            'categories': categories
        }
    )


def cart(request):
    return render(
        request, 'cart.html'
    )

@login_required
def checkout(request):
    return render(
        request, 'checkout.html'
    )

@login_required
def checkout_complete(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    payment_intent_id = request.GET.get('payment_intent')
    
    if payment_intent_id:
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                transaction_id = intent.metadata.get('transaction')
                if transaction_id:
                    make_order(transaction_id)
        except Exception as e:
            print(f"Stripe verification error: {e}")

    session_transaction_id = request.session.get('current_transaction_id')
    context = {}
    
    if session_transaction_id:
        try:
            order = Order.objects.get(transaction=session_transaction_id, user=request.user)
            context['order'] = order
        except Order.DoesNotExist:
            pass
            
    return render(request, 'thank-you.html', context)

def lesson_detail_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course = lesson.section.course

    has_bought = False

    if request.user.is_authenticated:
        has_bought = Order.objects.filter(
            user=request.user,
            orderproduct__course=course,
            status='completed'
        ).exists()

    if not (has_bought or lesson.is_preview):
        return redirect('course_detail', pid=course.id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login')

        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')

        if text:
            parent_comment = None

            if parent_id:
                parent_comment = LessonComment.objects.filter(
                    pk=parent_id
                ).first()

            LessonComment.objects.create(
                lesson=lesson,
                user=request.user,
                text=text,
                parent=parent_comment
            )

            return redirect('lesson_detail', pk=lesson.pk)

    comments = lesson.comments.filter(
        parent=None
    ).select_related('user').prefetch_related('replies__user')

    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'comments': comments
    })

@login_required
def course_learn_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    has_bought = Order.objects.filter(
        user=request.user, 
        orderproduct__course=course, 
        status='completed'
    ).exists()

    if not has_bought:
        return redirect('course_detail', pid=course.id)

    lessons = course.lessons.all() if hasattr(course, 'lessons') else []
    sections = course.sections.all() if hasattr(course, 'sections') else []
    
    context = {
        'course': course,
        'lessons': lessons,
        'sections': sections,
    }
    return render(request, 'course_learn.html', context)

def cart_add(request, pid):
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key
    cart_model = Cart.objects.filter(session_id=session_id).last()

    if cart_model is None:
        cart_model = Cart.objects.create(session_id=session_id, items=[pid])
    elif pid not in cart_model.items:
        cart_model.items.append(pid)
        cart_model.save()

    return JsonResponse({
        'message': _('The course has been added to your cart'),
        'items_count': len(cart_model.items)
    })


def cart_remove(request, pid):
    session = request.session.session_key

    if not session:
        return JsonResponse({})
    
    cart_model = Cart.objects.filter(session_id=session).last()

    if not cart_model:
        return JsonResponse({})
    
    if pid in cart_model.items:
        cart_model.items.remove(pid)
        cart_model.save()

    return JsonResponse({
        'message': _('The course has been removed from your cart')
    })

def about_view(request):
    about_info = AboutPageContent.objects.first()
    reviews = StudentReview.objects.all()
    context = {
        'about_info': about_info,
        'reviews': reviews,
    }
    return render(request, 'about.html', context)