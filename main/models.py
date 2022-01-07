from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
from django.db import models

# --------------------------------------------------------------------------------------------------------------------------------

# User (کاربر) Model 
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have email")
        if not password:
            raise ValueError("Users must have password")
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password, **kwargs):
        user = self.model(email=email, staff=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, staff=True, superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='ایمیل',unique=True,db_index=True)
    first_name = models.CharField(verbose_name='نام',max_length=50,db_index=True)
    last_name = models.CharField(verbose_name='نام خانوادگی',max_length=150,db_index=True)
    address = models.TextField(verbose_name='آدرس',null=True,blank=True)
    zipcode = models.CharField(verbose_name='کد پستی',max_length=10,null=True,blank=True)
    superuser = models.BooleanField(verbose_name='وضعیت مدیرکل', default=False)
    staff = models.BooleanField(verbose_name='وضعیت کارمند', default=False)
    active = models.BooleanField(verbose_name='وضعیت فعالیت', default=True)
    create_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_staff(self):
        return self.staff

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_fullname(self):
        return ' '.join([self.first_name, self.last_name])

    class Meta:
        ordering = ('id', 'create_date')
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Icon(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=255,db_index=True)
    url = models.URLField(verbose_name='آدرس عکس')

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id',)
        verbose_name = 'آیکون'
        verbose_name_plural = 'آیکون ها'


class Category(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=255,db_index=True)
    fk_parent = models.ForeignKey('self',verbose_name='سر دسته',related_name='category_parent',on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id',)
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Tag(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=255,db_index=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id',)
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'


class Product(models.Model):
    title = models.CharField(verbose_name='عنوان',max_length=255,db_index=True)
    description = models.TextField(verbose_name='توضیحات',null=True,blank=True)
    weight = models.FloatField(verbose_name='وزن')
    unit = models.CharField(verbose_name='واحد',max_length=50)
    price = models.BigIntegerField(verbose_name='قیمت')
    category = models.ForeignKey(Category,verbose_name='دسته بندی',related_name='product_category',on_delete=models.SET_NULL, null=True)
    image = models.ImageField(verbose_name='عکس',upload_to='media/images/product/')
    icon = models.ForeignKey(Icon,verbose_name='آیکون',related_name='product_icon',on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag,verbose_name='تگ',related_name='product_tags',blank=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class OrderDetails(models.Model):
    product=models.ForeignKey(Product,verbose_name='محصول',related_name='order_product',on_delete=models.SET_NULL,null=True)
    count=models.PositiveIntegerField(verbose_name='تعداد',default=1)
    price=models.BigIntegerField(verbose_name='قیمت')

    def __str__(self):
        return "{} ({})".format(self.product,self.count)

    class Meta:
        ordering = ('id',)
        verbose_name = 'جزئیات سفارش'
        verbose_name_plural = "جزئیات سفارشات"


class Order(models.Model):
    user = models.ForeignKey(User,verbose_name='کاربر',related_name='order_user',on_delete=models.SET_NULL, null=True)
    email = models.EmailField(verbose_name='ایمیل')
    address = models.TextField(verbose_name='آدرس')
    zipcode = models.CharField(verbose_name='کد پستی',max_length=10)
    items = models.ManyToManyField(OrderDetails,verbose_name='جزئیات سفارش',related_name='order_details',blank=True)
    total_price=models.BigIntegerField(verbose_name='هزینه کل',default=0)
    PAYMENT_TYPE =(
        ('in-place','پرداخت در محل'),
        ('online','پرداخت آنلاین')
    )
    payment_type=models.CharField(verbose_name='نوع پرداخت', max_length=8,choices=PAYMENT_TYPE,default='online')
    status = models.BooleanField(verbose_name='وضعیت',default=False)
    order_date=models.DateField(verbose_name='تاریخ خرید',auto_now_add=True)

    def __str__(self):
        return "{} ({})".format(self.user, self.order_date)

    class Meta:
        ordering = ('id',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
