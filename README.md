<div dir="rtl">
<h1> مسار تطوير منصة تعليمية باستخدام جانغو Django </h1>
<p>الشيفرة المصدرية الخاصة بمسار تطوير منصة تعليمية باستخدام جانغو Django</p>

<h2> منصة تعليمية </h2>
<p>منصة تعليمية إلكترونية كاملة، توفر إمكانية إدارة الكورسات، والدروس، وتكامل آمن مع بوابة الدفع Stripe. </p>
<h2>المتطلبات</h2>
<ul>
  <li>Python >= 3.9</li>
  <li>pip 21.1.1</li>
  <li>pipenv</li>
</ul>
<h2> طريقة التثبيت </h2>
<ul>
  <li>نسخ المستودع <code>git clone https://github.com/PolaDevX/Educational-platform</code></li>
  <li>الانتقال إلى المجلد <code>cd Educational-platform</code></li>
  <li>تثبيت التطبيق <code>pip install -r requirements.txt</code></li>
  <li>تشغيل ملفات التهجير <code>python manage.py migrate</code></li>
  <li>تشغيل المشروع <code>python manage.py runserver</code></li>
</ul>

<h2>⚙️ إعداد متغيرات البيئة (.env)</h2>
<p>أنشئ ملف <code>.env</code> في جذر المشروع وأضف الآتي:</p>
<pre><code>
DEBUG=True
SECRET_KEY= your_secret_key
STRIPE_PUBLISHABLE_KEY= your_stripe_publishable_key
STRIPE_SECRET_KEY= your_stripe_secret_key
STRIPE_WEBHOOK_SECRET= your_webhook_secret
GOOGLE_CLIENT_ID = your_google_client_id
GOOGLE_CLIENT_SECRET = your_google_client_secret
</code></pre>

<h2> لوحة التحكم (Django Admin) </h2>
<p>للدخول إلى لوحة التحكم عبر الرابط <code>/admin/</code>، استخدم البيانات التالية:</p>
<h2> إنشاء حساب المدير (Superuser)</h2>
<p>بدلاً من الاعتماد على حساب ثابت، أنشئ حسابك عبر التيرمنال مباشرة:</p>
<code>python manage.py createsuperuser</code>
<p>(ثم أدخل اسم المستخدم، البريد، وكلمة المرور - ملاحظة: لن تظهر النجوم أثناء كتابة كلمة المرور لأسباب أمنية).</p>
<h2> لوحة التحكم (Django Admin) </h2>
<p>للدخول إلى لوحة التحكم عبر الرابط <code>/admin/</code>، سجل الدخول بحساب الـ Superuser الذي أنشأته.</p>

<h2>🔗 روابط هامة</h2>
<ul>
  <li><strong>النسخة الحية (Live Demo):</strong> <a href="https://pola2010.pythonanywhere.com/" target="_blank">https://pola2010.pythonanywhere.com/</a></li>
</ul>

<h2> الميزات الرئيسية (Features)</h2>
<ul>
  <li><strong>إدارة الكورسات والدروس:</strong> إدارة شاملة للكورسات، الأقسام، ومعاينة الدروس (<code>is_preview</code>).</li>
  <li><strong>الدفع والاشتراكات:</strong> تكامل آمن مع بوابة <strong>Stripe</strong> وتحديث حالة المشتركين تلقائياً.</li>
  <li><strong>تعدد اللغات (i18n):</strong> دعم كامل للغة العربية واللغات الأخرى.</li>
  <li><strong>المدونة والتعليقات:</strong> نظام مقالات وتفاعل عبر التعليقات للطلاب.</li>
</ul>

<h2>بنية المشروع والتطبيقات الأساسية</h2>
<ul>
  <li><code>core/</code>: التطبيق الرئيسي للصفحات العامة.</li>
  <li><code>courses/</code>: إدارة الكورسات، الأقسام، والدروس.</li>
  <li><code>payments/</code>: معالجة المدفوعات والـ Webhooks.</li>
  <li><code>blog/</code>: إدارة المقالات والتدوين.</li>
  <li><code>comments/</code>: نظام التعليقات.</li>
</ul>

<h2>💳 إعداد Webhook الخاص بـ Stripe</h2>
<ul>
  <li><strong>محلياً:</strong> استخدم أداة Stripe CLI لتوجيه الأحداث:
    <code>stripe listen --forward-to localhost:8000/payments/webhook/</code>
    وخذ كود الـ secret (الذي يبدأ بـ <code>whsec_...</code>) وضعه في متغير <code>STRIPE_WEBHOOK_SECRET</code>.
  </li>
  <li><strong>على الإنتاج:</strong> اربط رابط الـ Webhook الخاص بموقعك المنشور بلوحة تحكم Stripe مع تفعيل الحدث <code>checkout.session.completed</code>.</li>
</ul>
</div>
